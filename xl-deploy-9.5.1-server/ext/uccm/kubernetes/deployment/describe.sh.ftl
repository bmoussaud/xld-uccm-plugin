echo "${deployed.container.container.kubectlPath}/kubectl describe ${resource} ${resourceName} -n ${deployed.container.name}"
${deployed.container.container.kubectlPath}/kubectl describe <#if (deployed.container.container.kubeConfigContext??)>--context="${deployed.container.container.kubeConfigContext}"</#if> ${resource} ${resourceName} -n ${deployed.container.name}


