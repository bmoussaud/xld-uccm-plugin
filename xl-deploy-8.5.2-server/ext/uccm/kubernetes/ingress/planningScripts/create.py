
def step_parameters(port,deployed):
    return { 'resource':'ingress', 'order': 65, 'ci': port}


def wait_parameters(port,deployed):
    data = { 'description': 'Wait for Ingress {1}/{0} ready on {2}'.format(port.name,deployed.name, deployed.container.name),
            'order': 66}
    return data

for port in deployed.ports:
    if port.exposeAsService and port.exposeAsIngress:
        context.addStepWithCheckpoint(steps.kubectlApply(**step_parameters(port, deployed)), delta)
        context.addStep(steps.noop(**wait_parameters(port, deployed)))
