echo '
<#include '/uccm/kubernetes/${resource}/${profile}_resource.json.ftl'>
' > resource.json
cat -n resource.json
cp resource.json /tmp/${deployed.name}-${ci.name}-${resourceName}.json
json2yaml /tmp/${deployed.name}-${ci.name}-${resourceName}.json > /tmp/${deployed.name}-${ci.name}-${resourceName}.yaml
echo 'kubectl apply <#if (deployed.container.container.kubeConfigContext??)>--context="${deployed.container.container.kubeConfigContext}"</#if> -f resource.json --validate=true -n ${deployed.container.name}'
kubectl apply <#if (deployed.container.container.kubeConfigContext??)>--context="${deployed.container.container.kubeConfigContext}"</#if> -f resource.json --validate=true -n ${deployed.container.name}
