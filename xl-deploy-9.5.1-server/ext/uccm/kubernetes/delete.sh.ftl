echo '${previousDeployed.container.container.kubectlPath}/kubectl delete <#if (previousDeployed.container.container.kubeConfigContext??)>--context="${previousDeployed.container.container.kubeConfigContext}"</#if> ${resource} ${resourceName} -n ${previousDeployed.container.name}'
${previousDeployed.container.container.kubectlPath}/kubectl delete <#if (previousDeployed.container.container.kubeConfigContext??)>--context="${previousDeployed.container.container.kubeConfigContext}"</#if> ${resource} ${resourceName} -n ${previousDeployed.container.name}

    
