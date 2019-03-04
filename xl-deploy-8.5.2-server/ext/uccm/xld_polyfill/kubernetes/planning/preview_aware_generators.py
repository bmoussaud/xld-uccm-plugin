from xld.kubernetes.resource.planningScripts.generator import StepsGenerator
from xld.kubernetes.resource.helper import ResourceHelper
from uccm.utils.profile import ProfileProcessor


class PreviewAwareStepsGenerator(StepsGenerator):
    def __init__(self, context, steps, delta):
        super(PreviewAwareStepsGenerator, self).__init__(context, steps, delta)

    def generate(self, action, order, data, wait_details, checkpoint_name, operation):
        super(PreviewAwareStepsGenerator, self).generate(action, order, data, wait_details, checkpoint_name, operation)
        if "_StepsGenerator__last_step" in self.__dict__:
            self.__dict__['_StepsGenerator__last_step'].setPreviewScript('uccm/xld_polyfill/kubernetes/planning/preview_resource.py')
        else:
            raise Exception("__last_step not found!")


class ProfileResourceHelper(ResourceHelper):
    def __init__(self, deployed, environment):
        super(ProfileResourceHelper, self).__init__(deployed)
        self.environment = environment

    def parse(self):
        json_data = super(ProfileResourceHelper, self).parse()
        processor = ProfileProcessor(self.deployed, self.environment)
        return processor.process(template=json_data)


