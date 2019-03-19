import re
import json
import yaml
import jsonpatch
from jsonpointer import resolve_pointer, JsonPointerException
from uccm.utils.cfyaml_loader import CfnYamlLoader


class ProcessorChain(object):
    def __init__(self, processors, deployed, deployed_application):
        self.deployed = deployed
        self.deployed_application = deployed_application
        self.profile_dictionary = ProfileDictionary(deployed_application.environment.profileDictionaries)
        self.processors = processors

    def process(self, template):
        fcn_to_call = 'process'
        for p in self.processors:
            mod_name = "scm_mount.uccm_processors.%s" % p
            try:
                mod = __import__(mod_name, fromlist=["process"])
            except ImportError, e:
                logger.error("Processor %s not found." % mod_name)
                continue
            func = getattr(mod, fcn_to_call)
            template = func(template, self.profile_dictionary, self.deployed, self.deployed_application)
        return template


class ProfileProcessor(object):

    def __init__(self, deployed, deployed_application):
        self.deployed_application = deployed_application
        self.deployed = deployed
        self.environment = deployed_application.environment

    @staticmethod
    def formatted_json_string(obj):
        return json.dumps(obj, indent=4, sort_keys=True)

    def read_template(self):
        template_path = self.deployed.file.path
        with open(template_path, 'r') as f:
            raw_data = f.read()
        if template_path.endswith('yaml'):
            data = yaml.load(raw_data, Loader=CfnYamlLoader)
        else:
            data = json.loads(raw_data)
        return data

    def process(self, template=None, profile=None):
        profile_name = profile if profile is not None else self.deployed.profileName
        if not template:
            template = self.read_template()
        chain = ProcessorChain([profile_name], self.deployed, self.deployed_application)
        processed_template = chain.process(template)
        return ProfilePatchDictionary(self.environment.profilePatchDictionaries).apply(processed_template)


class ProfilePatchDictionary(object):
    def __init__(self, source_dictionaries):
        self.source_dictionaries = source_dictionaries

    @staticmethod
    def path_exists(json_path, obj):
        try:
            target = resolve_pointer(obj, json_path)
            return target is not None
        except JsonPointerException:
            return False

    @staticmethod
    def from_json(json_value):
        try:
            return json.loads(json_value)
        except ValueError:
            return json_value

    @staticmethod
    def apply_patches(patches, obj, fail_on_error=True):
        if not patches:
            return obj
        try:
            patch = jsonpatch.JsonPatch(patches)
            return patch.apply(obj)
        except jsonpatch.JsonPatchTestFailed, e:
            if fail_on_error:
                raise e
        return False

    def test_path(self, json_path, value, obj):
        patch = [{'op': 'test', 'path': json_path, 'value': self.from_json(value)}]
        return self.apply_patches(patch, obj,  False)

    def apply_modify_patch(self, paths_and_patchs_map, patch_op, obj, fail_on_error=True):
        all_patches = [{'op': patch_op, 'path': json_path, 'value': self.from_json(value)}
                       for json_path, value in paths_and_patchs_map.items()]
        return self.apply_patches(all_patches, obj, fail_on_error)

    def apply_delete_patch(self, paths, patch_op, obj, fail_on_error=True):
        all_patches = [{'op': patch_op, 'path': json_path} for json_path in paths]
        return self.apply_patches(all_patches, obj, fail_on_error)

    def is_active(self, sd, obj):
        if not sd.enabled:
            return False
        active_path = True
        active_matches = True
        if sd.pathActivation:
            active_path = any([self.path_exists(path, obj) for path in sd.pathActivation])

        if sd.matchActivation.keys():
            active_matches = all([self.test_path(path, value, obj) for path, value in sd.matchActivation.items()])
        return active_path and active_matches

    def apply(self, obj):
        for sd in self.source_dictionaries:
            if self.is_active(sd, obj):
                obj = self.apply_modify_patch(sd.add, "add", obj, sd.failOnNotFound)
                obj = self.apply_modify_patch(sd.replace, "replace", obj, sd.failOnNotFound)
                obj = self.apply_delete_patch(sd.remove, "remove", obj, sd.failOnNotFound)
        return obj


class ProfileDictionary(object):

    def __init__(self, source_dictionaries):
        self.source_dictionaries = source_dictionaries
        self.key_pattern = re.compile("\\$\\{this\\.([a-zA-Z0-9]+)\\}")

    def find_keys_with_prefix(self, prefix):
        return set([k for k in [sd.entries.keys() for sd in self.source_dictionaries] if k.startswith(prefix)])

    def resolve(self, key, default=None):
        unresolved_value = None
        for sd in self.source_dictionaries:
            if key in sd.entries.keys():
                unresolved_value = sd.entries[key]
                break
            elif key in sd.encryptedEntries.keys():
                unresolved_value = sd.encryptedEntries[key]
                break
        if unresolved_value:
            final_value = unresolved_value
            match = self.key_pattern.match(unresolved_value)
            if match:
                unresolved_keys = match.groups()[1:]
                for k in unresolved_keys:
                    resolved_key_value = self.resolve(k)
                    final_value.replace("${this.%s}" % k, resolved_key_value)
            return final_value
        else:
            if default:
                return default
            else:
                raise Exception("Cannot resolve profile dictionaries. Key'%s'" % key)
