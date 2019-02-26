echo '
<#include profile>
' > ingress.json
cat -n ingress.json
kubectl apply -f ingress.json --validate=true -n ${deployed.container.name}


