import json
import yaml
from com.xebialabs.deployit.plugin.api.reflect import Type
from uccm.utils.cfyaml_loader import CfnYamlLoader

class GenerateDeployables(object):
    def __init__(self, ci_id, task_vars):
        self.ci_id = ci_id
        self.repository_service = task_vars['repositoryService']
        self.template_path = self.repository_service.read(ci_id).file.path
        self.cf_description_descriptor = Type.valueOf("uccm.CloudformationDescriptionSpec").descriptor
        self.cf_resource_descriptor = Type.valueOf("uccm.CloudformationResourceSpec").descriptor
        self.cf_mapping_descriptor = Type.valueOf("uccm.CloudformationMappingSpec").descriptor
        self.cf_parameter_descriptor = Type.valueOf("uccm.CloudformationParameterSpec").descriptor
        self.cf_output_descriptor = Type.valueOf("uccm.CloudformationOutputSpec").descriptor

    @staticmethod
    def formatted_json_string(obj):
        return json.dumps(obj, indent=4, sort_keys=True)

    def read_template(self):
        with open(self.template_path, 'r') as f:
            data = f.read()
        if self.template_path.endswith('yaml'):
            json_data = yaml.load(data, Loader=CfnYamlLoader)
        else:
            json_data = json.loads(data)
        return json_data

    def set_prop_and_create(self, descriptor, ci, values):
        for k, v in values.items():
            descriptor.getPropertyDescriptor(k).set(ci, v)
        self.repository_service.update([ci])

    def process_description(self, template):
        print "Processing template version and description..."
        descriptor = self.cf_description_descriptor
        ci = descriptor.newInstance("%s/Description" % self.ci_id)
        self.set_prop_and_create(descriptor, ci, {
            "templateFormatVersion":  template["AWSTemplateFormatVersion"],
            "description": template['Description']
        })

    def process_definition(self, template, definition_name, descriptor):
        print "Processing %s..." % definition_name
        singular_definition_name = definition_name[:-1]
        if definition_name not in template.keys():
            return
        parameters = template[definition_name]
        for param_name in parameters.keys():
            print "    processing %s %s" % (singular_definition_name, param_name)
            ci = descriptor.newInstance("%s/%s-%s" % (self.ci_id, singular_definition_name, param_name))
            self.set_prop_and_create(descriptor, ci, {
                "definition":  self.formatted_json_string(parameters[param_name]),
                "resourceName": param_name
            })

    def process_resources(self, template):
        print "Processing Resources..."
        if "Resources" not in template.keys():
            return
        descriptor = self.cf_resource_descriptor
        resources = template['Resources']
        for resource_name in resources.keys():
            print "    processing resource %s" % resource_name
            ci = descriptor.newInstance("%s/Resource-%s" % (self.ci_id, resource_name))
            resource = resources[resource_name]
            self.set_prop_and_create(descriptor, ci, {
                "definition":  self.formatted_json_string(resource['Properties']),
                "resourceName": resource_name,
                "awsResourceType": resource['Type']
            })

    def process(self):
        template = self.read_template()
        self.process_description(template)
        self.process_resources(template)
        self.process_definition(template, "Parameters", self.cf_parameter_descriptor)
        self.process_definition(template, "Mappings", self.cf_mapping_descriptor)
        self.process_definition(template, "Outputs", self.cf_output_descriptor)
        print "Done"


GenerateDeployables(thisCi.id, locals()).process()