echo "kubectl describe ${resource} ${resourceName} -n ${deployed.container.name}"
kubectl describe <#if (deployed.container.container.kubeConfigContext??)>--context="${deployed.container.container.kubeConfigContext}"</#if> ${resource} ${resourceName} -n ${deployed.container.name}


