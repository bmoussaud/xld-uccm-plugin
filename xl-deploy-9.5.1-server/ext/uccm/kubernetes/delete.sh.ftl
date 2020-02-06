echo '${deployed.container.container.kubectlPath}/kubectl delete <#if (previousDeployed.container.container.kubeConfigContext??)>--context="${previousDeployed.container.container.kubeConfigContext}"</#if> ${resource} ${resourceName} -n ${previousDeployed.container.name}'
${deployed.container.container.kubectlPath}/skubectl delete <#if (previousDeployed.container.container.kubeConfigContext??)>--context="${previousDeployed.container.container.kubeConfigContext}"</#if> ${resource} ${resourceName} -n ${previousDeployed.container.name}


    
