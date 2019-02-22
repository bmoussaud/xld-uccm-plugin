
def step_parameters(port,deployed):
    return { 'resource':'ingress', 'order': 65, 'ci': port, 'blueprint': port.ingressBlueprintName}

def wait_parameters(port,deployed):
    return { 'resource': 'ingress', 'resourceName':'{0}-{1}-ingress'.format(deployed.name,port.name), 'ci':port, 'order': 65}

for port in deployed.ports:
    if port.exposeAsService and port.exposeAsIngress:
        context.addStepWithCheckpoint(steps.kubectlApply(**step_parameters(port, deployed)), delta)
        context.addStep(steps.waitResourceUp(**wait_parameters(port, deployed)))
