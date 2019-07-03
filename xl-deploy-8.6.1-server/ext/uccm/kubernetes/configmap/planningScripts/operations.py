import uccm.deltas.compute

reload(uccm.deltas.compute)
from uccm.deltas.compute import DeltasBuilder, StepGenerator

import hashlib
import json


class ServiceStepGenerator(StepGenerator):

    def create(self, delta, deployed, config):
        # the resourceName has been computed by the resolve.py
        context.addStepWithCheckpoint(
            steps.kubectlCreate(
                **{'resource': self.get_resource(config), 'resourceName': config.resourceName, 'order': 59,
                   'ci': config}),
            delta
        )

    @staticmethod
    def get_resource(config):
        resource = 'configmap'
        if config.isSensitive:
            resource = 'secret'
        return resource

    def destroy(self, delta, deployed, config):
        data = {'target': deployed, 'resource': self.get_resource(config),
                'resourceName': config.resourceName, 'order': 78}
        context.addStep(steps.noop(**{
            'description': 'Wait for ConfigMap {1}/{0} deleted on {2}'.format(config.name, deployed.name,
                                                                              deployed.container.name), 'order': 79}))
        context.addStepWithCheckpoint(steps.kubectlDelete(**data), delta)


import traceback

try:
    builder = DeltasBuilder()
    list_of_deltas = builder.build2(delta.operation, deployed, previousDeployed, "mountedFiles")
    print "configmap %s" % list_of_deltas
    ServiceStepGenerator(delta, list_of_deltas).generate()
except:
    raise Exception(str(traceback.format_exc()))
