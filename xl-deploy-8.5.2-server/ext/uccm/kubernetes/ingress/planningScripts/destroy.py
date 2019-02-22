
def step_parameters(port,deployed):
    return {'resource':'ingress', 'resourceName':'{0}-{1}-ingress'.format(deployed.name,port.name), 'order': 43}

def wait_parameters(port,deployed):
    data = { 'description': 'Wait for Ingress {1}/{0} deleted on {2}'.format(port.name,deployed.name, deployed.container.name),
            'order': 44}
    return data

for port in previousDeployed.ports:
    if port.exposeAsService:
        context.addStepWithCheckpoint(steps.kubectlDelete(**step_parameters(port, previousDeployed)), delta)
        context.addStep(steps.noop(**wait_parameters(port, previousDeployed)))
