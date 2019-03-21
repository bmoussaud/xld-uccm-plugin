import uccm.deltas.compute

reload(uccm.deltas.compute)
from uccm.deltas.compute import DeltasBuilder, StepGenerator


class IngresStepGenerator(StepGenerator):

    def create(self, delta, deployed, port):
        if port.exposeAsIngress:
            context.addStepWithCheckpoint(steps.kubectlApply(**{'resource': 'ingress', 'order': 65, 'ci': port}), delta)
            context.addStep(steps.waitResourceUp(
                **{'resource': 'ingress', 'resourceName': '{0}-{1}-ingress'.format(deployed.name, port.name),
                   'ci': port,
                   'order': 66}))

    def destroy(self, delta, deployed, port):
        if port.exposeAsIngress:
            data = {'target': deployed, 'resource': 'ingress',
                    'resourceName': '{0}-{1}-ingress'.format(deployed.name, port.name), 'order': 43}
            context.addStep(steps.noop(**{
                'description': 'Wait for Ingress {1}/{0} deleted on {2}'.format(port.name, deployed.name,
                                                                                deployed.container.name), 'order': 44}))
            context.addStepWithCheckpoint(steps.kubectlDelete(**data), delta)


import traceback


try:
    builder = DeltasBuilder()
    list_of_deltas = builder.build2(delta.operation, deployed, previousDeployed, "ports")
    print "ingress %s" % list_of_deltas
    IngresStepGenerator(delta, list_of_deltas).generate()
except:
    raise Exception(str(traceback.format_exc()))

