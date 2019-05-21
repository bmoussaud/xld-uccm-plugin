echo 'kubectl scale <#if (deployed.container.container.kubeConfigContext??)>--context="${deployed.container.container.kubeConfigContext}"</#if> --replicas=${nbreplicas} deployment/${resourceName} -n ${previousDeployed.container.name}''
kubectl scale <#if (deployed.container.container.kubeConfigContext??)>--context="${deployed.container.container.kubeConfigContext}"</#if> --replicas=${nbreplicas} deployment/${resourceName} -n ${previousDeployed.container.name}


