echo 'kubectl delete <#if (previousDeployed.container.container.kubeConfigContext??)>--context="${previousDeployed.container.container.kubeConfigContext}"</#if> ${resource} ${resourceName} -n ${previousDeployed.container.name}'
kubectl delete <#if (previousDeployed.container.container.kubeConfigContext??)>--context="${previousDeployed.container.container.kubeConfigContext}"</#if> ${resource} ${resourceName} -n ${previousDeployed.container.name}


    
