from xld.kubernetes.resource.planningScripts.generator import StepsGenerator
from xld.kubernetes.resource.helper import ResourceHelper
from uccm.utils.profile import ProfileProcessor


class PreviewAwareStepsGenerator(StepsGenerator):
    def __init__(self, context, steps, delta, deployed, deployed_application):
        super(PreviewAwareStepsGenerator, self).__init__(context, steps, delta)
        self.deployed_application = deployed_application
        self.deployed = deployed

    def generate(self, action, order, data, wait_details, checkpoint_name, operation):
        super(PreviewAwareStepsGenerator, self).generate(action, order, data, wait_details, checkpoint_name, operation)
        if "_StepsGenerator__last_step" in self.__dict__:
            jython_step = self.__dict__['_StepsGenerator__last_step']
            jython_step.setPreviewScript('uccm/xld_polyfill/kubernetes/planning/preview_resource.py')
            jython_step.getJythonContext()["deployedApplication"] = self.deployed_application
            jython_step.getJythonContext()["deployed"] = self.deployed
        else:
            raise Exception("__last_step not found!")


class ProfileResourceHelper(ResourceHelper):
    def __init__(self, deployed, deployed_application):
        super(ProfileResourceHelper, self).__init__(deployed)
        self.deployed_application = deployed_application

    def parse(self):
        json_data = super(ProfileResourceHelper, self).parse()
        processor = ProfileProcessor(self.deployed, self.deployed_application)
        return processor.process(template=json_data)


