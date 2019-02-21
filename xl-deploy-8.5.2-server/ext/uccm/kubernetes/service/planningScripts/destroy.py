
def step_parameters(port,deployed):
    data = { 'description': 'Delete Service {1}/{0} on {2}'.format(port.name,deployed.name, deployed.container.name),
            'order': 43}
    return data

def wait_parameters(port,deployed):
    data = { 'description': 'Wait for Service {1}/{0} deleted on {2}'.format(port.name,deployed.name, deployed.container.name),
            'order': 44}
    return data

for port in previousDeployed.ports:
    if port.exposeAsService:
        context.addStepWithCheckpoint(steps.noop(**step_parameters(port, previousDeployed)), delta)
        context.addStep(steps.noop(**wait_parameters(port, previousDeployed)))
