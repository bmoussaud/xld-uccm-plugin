import uccm.deltas.compute

reload(uccm.deltas.compute)
from uccm.deltas.compute import DeltasBuilder, StepGenerator

import hashlib
import json


class ServiceStepGenerator(StepGenerator):

    def create(self, delta, deployed, config):
        #https://blog.questionable.services/article/kubernetes-deployments-configmap-change/
        h = hashlib.md5(json.dumps(config.placeholders, sort_keys=True))
        short_h = str(int(h.hexdigest(), 16) % (10 ** 8))
        checksum = str(config.deployable.checksum)
        data_md5 = "d-{0}-f-{1}".format(short_h, checksum[0:10])
        config.data_hash = data_md5

        resourceName = '{0}-{1}-configmap'.format(deployed.name, config.name)
        context.addStepWithCheckpoint(
            steps.kubectlCreate(**{'resource': 'configmap', 'resourceName': resourceName, 'order': 59, 'ci': config}),
            delta
        )
        # context.addStep(steps.waitResourceUp(
        #    **{'resource': 'configmap', 'resourceName': '{0}-{1}-configmap'.format(deployed.name, port.name),
        #       'ci': port,
        #       'order': 59}))

    def destroy(self, delta, deployed, config):
        data = {'target': deployed, 'resource': 'configmap',
                'resourceName': '{0}-{1}-configmap'.format(deployed.name, config.name), 'order': 43}
        context.addStep(steps.noop(**{
            'description': 'Wait for ConfigMap {1}/{0} deleted on {2}'.format(config.name, deployed.name,
                                                                              deployed.container.name), 'order': 44}))
        context.addStepWithCheckpoint(steps.kubectlDelete(**data), delta)


import traceback

try:
    builder = DeltasBuilder()
    list_of_deltas = builder.build2(delta.operation, deployed, previousDeployed, "mountedFiles")
    print "configmap %s" % list_of_deltas
    ServiceStepGenerator(delta, list_of_deltas).generate()
except:
    raise Exception(str(traceback.format_exc()))
