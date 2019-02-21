
def step_parameters(port,deployed):
    data = { 'description': 'Configure Service {1}/{0} on {2}'.format(port.name,deployed.name, deployed.container.name),
            'order': 63}
    return data

def wait_parameters(port,deployed):
    data = { 'description': 'Wait for Service {1}/{0} ready on {2}'.format(port.name,deployed.name, deployed.container.name),
            'order': 64}
    return data

for port in deployed.ports:
    if port.exposeAsService:
        context.addStepWithCheckpoint(steps.noop(**step_parameters(port, deployed)), delta)
        context.addStep(steps.noop(**wait_parameters(port, deployed)))
