for securedRegistry in previousDeployed.container.container.securedRegistries:
    context.addStep(
        steps.os_script(**{
            'script': 'uccm/kubernetes/secret/destroySecuredRegistry.sh.ftl',
            'order': 48,
            'description': "Delete a secret associated to '{0}' secured registry".format(securedRegistry.name),
            'freemarker-context': {'registry': securedRegistry,'resourceName': "{0}-{1}-secret".format(previousDeployed.name,securedRegistry.name)},
            'target-host': previousDeployed.container.container.kubectlHost}))
