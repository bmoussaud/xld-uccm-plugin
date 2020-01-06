import traceback

try:
    include_version = True

    if include_version:
        resource_name = "{0}-deployment-{1}".format(deployed.name, deployedApplication.version.name)
    else:
        resource_name = "{0}-deployment".format(deployed.name)

    deployed.resourceName = resource_name
except:
    raise Exception(str(traceback.format_exc()))
