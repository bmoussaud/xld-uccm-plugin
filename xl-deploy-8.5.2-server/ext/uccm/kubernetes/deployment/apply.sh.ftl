echo '
<#include '/uccm/kubernetes/deployment/default_resource.json.ftl'>
' > resource.json
cat -n resource.json
kubectl apply -f resource.json --validate=true -n ${deployed.container.name}
