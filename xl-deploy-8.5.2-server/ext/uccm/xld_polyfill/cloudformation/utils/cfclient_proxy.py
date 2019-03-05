from uccm.utils.profile import ProfileProcessor
from botocore.exceptions import ClientError
from cloudformation.utils.cf_client import CFClient
import json


class CFClientUccmProxy(object):
    def __init__(self, deployed, deployed_application):
        self.deployed_application = deployed_application
        self.environment = deployed_application.environment
        self.deployed = deployed
        self.client = CFClient.new_instance(deployed.container)
        self.cf_client = self.client.cf_client

    def validate_template(self):
        try:
            _, template = self.read_stack_file()
            return self.cf_client.validate_template(TemplateBody=template)
        except ClientError as err:
            print("Validation failed for stack [%s]. %s" % (self.deployed.name, err.message))
            raise

    def create_stack(self):
        stackname = self.client._sanatize_name(self.deployed.name)
        capabilities = self.deployed.capabilities
        if not self.client._stack_exists(stackname):
            parameters, template = self.read_stack_file()
            self.cf_client.create_stack(StackName=stackname, TemplateBody=template, Parameters=parameters,
                                        Capabilities=capabilities, DisableRollback=self.deployed.disableRollback)
            self.deployed.stackId = self.client._stack_exists(stackname)
            return True
        return False

    def update_stack(self):
        stackname = self.client._sanatize_name(self.deployed.name)
        capabilities = self.deployed.capabilities
        if not self.client._stack_exists(stackname):
            raise Exception("Stack '%s' does not exist." % self.deployed.name)

        parameters, template = self.read_stack_file()
        self.cf_client.update_stack(StackName=stackname, TemplateBody=template, Parameters=parameters, Capabilities=capabilities)

    def read_stack_file(self):
        processor = ProfileProcessor(self.deployed, self.deployed_application)
        template = processor.process()
        parameters = []
        for k in self.deployed.inputVariables:
            param = dict()
            param['ParameterKey'] = k
            param['ParameterValue'] = self.deployed.inputVariables[k]
            parameters.append(param)
        return parameters, template

    def preview(self):
        _, template = self.read_stack_file()
        return json.dumps(template, sort_keys=True, indent=4)