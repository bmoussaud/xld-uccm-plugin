
for securedRegistry in deployed.container.container.securedRegistries:
    context.addStep(
        steps.os_script(**{
            'script': 'uccm/kubernetes/secret/applySecuredRegistry.sh.ftl',
            'order': 55,
            'description': "Create a secret associated to the '{0}' secured registry".format(securedRegistry.name),
            'freemarker-context': {'registry': securedRegistry,
                                   'resourceName': "{0}-{1}-secret".format(deployed.name, securedRegistry.name)},
            'target-host': deployed.container.container.kubectlHost}))
