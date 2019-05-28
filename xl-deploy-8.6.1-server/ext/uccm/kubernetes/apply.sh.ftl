echo '
<#include '/uccm/kubernetes/${resource}/${profile}_resource.json.ftl'>
' > resource.json
cat -n resource.json
echo 'kubectl apply <#if (deployed.container.container.kubeConfigContext??)>--context="${deployed.container.container.kubeConfigContext}"</#if> -f resource.json --validate=true -n ${deployed.container.name}'
kubectl apply <#if (deployed.container.container.kubeConfigContext??)>--context="${deployed.container.container.kubeConfigContext}"</#if> -f resource.json --validate=true -n ${deployed.container.name}
