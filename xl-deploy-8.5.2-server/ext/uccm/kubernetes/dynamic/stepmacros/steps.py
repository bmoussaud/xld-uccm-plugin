
def kubectl_apply(planner, resource=None, order=0, ci=None, profile=None):
    deployed = planner.deployed
    description = "Deploy {0} as kubernetes {2} to {1} namespace".format(deployed.name, deployed.container.name,resource)
    json_template = planner.process_profile_template(profile, application=planner.deployed_application.name,
                                                     version=planner.deployed_application.version.name, ci=ci,
                                                     containername=deployed.name, dynamic_deployed=planner.dynamic_deployed)
    return planner.steps.os_script(
        order=order,
        description=description,
        target_host=deployed.container.container.kubectlHost,
        script="uccm/kubernetes/dynamic/kubectl/apply",
        freemarker_context={
            "json": json_template
        })


def kubectl_delete(planner, resource=None, resource_name=None, order=0):
    deployed = planner.previous_deployed
    description = "Delete {0} kubernetes {2} from {1} namespace".format(deployed.name, deployed.container.name, resource)
    return planner.steps.os_script(
        order=order,
        description=description,
        target_host=deployed.container.container.kubectlHost,
        script="uccm/kubernetes/dynamic/kubectl/delete",
        freemarker_context={
            "resource": resource,
            "resourceName": resource_name,
            "deployed": deployed
        })


def wait_resource_up(planner, resource=None, resource_name=None, order=0, ci=None):
    deployed = planner.deployed
    description = "Wait for {2} {0} to be deployed on {1}".format(deployed.name, deployed.container.name, resource)
    return planner.steps.jython(
        order=order,
        description=description,
        script="uccm/kubernetes/{0}/wait_for_up.py".format(resource),
        jython_context={
            "target_host": deployed.container.container.kubectlHost,
            "resource": resource,
            "resourceName": resource_name,
            "ci": ci,
            "attempts": 10
        })


def kubectl_cmd(planner, resource=None, order=0, deployed=None, dynamic_deployed=None, profile_template=None):
    description = "Deploy {0} as kubernetes {2} to {1} namespace".format(deployed.name, deployed.container.name,resource)
    return planner.steps.os_script(
        order=order,
        description=description,
        target_host=deployed.container.container.kubectlHost,
        script="uccm/kubernetes/dynamic/kubectl/general_cmd",
        freemarker_context={
            "dynamic_deployed": dynamic_deployed,
            "profileTemplate": profile_template,
            "dictionaries": planner.deployed_application.environment.profileDictionaries,
            "dynamic_deployed": planner.dynamic_deployed
        })
