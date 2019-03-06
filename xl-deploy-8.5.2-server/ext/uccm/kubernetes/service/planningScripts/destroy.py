
def step_parameters(port,deployed):
    return {'resource':'service', 'resourceName':'{0}-{1}-service'.format(deployed.name,port.name), 'order': 43}

def wait_parameters(port,deployed):
    data = { 'description': 'Wait for Service {1}/{0} deleted on {2}'.format(port.name,deployed.name, deployed.container.name),
            'order': 44}
    return data

def get_modified_properties(deployed, previous):
    #[(propertyname, value, previousvalue)]
    modified_properties = []
    if deployed == None or previous == None:
        return modified_properties

    ci_type = deployed.type
    ci_descriptor = metadataService.findDescriptor(Type.valueOf(str(ci_type)))
    for pd in ci_descriptor.getPropertyDescriptors():
        result = (pd, pd.get(deployed), pd.get(previous))
        value = pd.get(deployed)
        old_value = pd.get(previous)
        print("%s:%s<->%s" % (result))
        if "deployable" == pd.getName() or "container" == pd.getName() or pd.isHidden() or pd.isTransient():
            continue
        if not(pd.areEqual(deployed,previous)):
            print(" add %s:%s<->%s" % (result))
            modified_properties.append(result)
    return modified_properties

def filter_modified_cis(deployeds, previous_deployeds):
    modifieds = {}
    for idx, deployed in enumerate(deployeds):
        try:
            previous = next(p for p in previous_deployeds if deployed.id == p.id)
        except:
            previous = None
        modified = get_modified_properties(deployed, previous)
        if len(modified) > 0 :
            modifieds[deployed]=modified
    return modifieds

print("D_SERVICE")
if delta.operation == "MODIFY":
    list_of_deployeds = filter_modified_cis(deployed.ports, previousDeployed.ports)
else:
    list_of_deployeds = previousDeployed.ports
print list_of_deployeds
print("/D_SERVICE")



for port in list_of_deployeds:
     if port.exposeAsService:
        context.addStepWithCheckpoint(steps.kubectlDelete(**step_parameters(port, previousDeployed)), delta)
        context.addStep(steps.noop(**wait_parameters(port, previousDeployed)))
