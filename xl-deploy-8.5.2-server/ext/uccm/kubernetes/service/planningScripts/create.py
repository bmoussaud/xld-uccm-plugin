
def step_parameters(port,deployed):
    return { 'resource':'service', 'order': 63, 'ci': port, 'profile':  port.serviceProfileName}

def wait_parameters(port,deployed):
    return { 'resource': 'service', 'resourceName':'{0}-{1}-service'.format(deployed.name,port.name), 'ci':port, 'order': 64}

for port in deployed.ports:
    if port.exposeAsService:
        context.addStepWithCheckpoint(steps.kubectlApply(**step_parameters(port, deployed)), delta)
        context.addStep(steps.waitResourceUp(**wait_parameters(port, deployed)))
