import re
import json
import yaml
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
            mod_name = "uccm_processors.%s" % p
            mod = __import__(mod_name, fromlist=["process"])
            func = getattr(mod, fcn_to_call)
            template = func(template, self.profile_dictionary, self.deployed, self.deployed_application)
        return template


class ProfileProcessor(object):

    def __init__(self, deployed, deployed_application):
        self.deployed_application = deployed_application
        self.deployed = deployed

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

    def process(self, template=None):
        profile_name = self.deployed.profileName
        if not template:
            template = self.read_template()
        return ProcessorChain([profile_name], self.deployed, self.deployed_application).process(template)


class ProfileDictionary(object):

    def __init__(self, source_dictionaries):
        self.source_dictionaries = source_dictionaries
        self.key_pattern = re.compile("\\$\\{this\\.([a-zA-Z0-9]+)\\}")

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
