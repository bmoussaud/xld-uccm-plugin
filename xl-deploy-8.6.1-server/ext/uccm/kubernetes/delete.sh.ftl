echo 'kubectl delete <#if (deployed.container.container.kubeConfigContext??)>--context="${deployed.container.container.kubeConfigContext}"</#if> ${resource} ${resourceName} -n ${previousDeployed.container.name}''
kubectl delete <#if (deployed.container.container.kubeConfigContext??)>--context="${deployed.container.container.kubeConfigContext}"</#if> ${resource} ${resourceName} -n ${previousDeployed.container.name}


