echo '
${json}
' > service.json
cat -n service.json
kubectl apply -f service.json --validate=true -n ${deployed.container.name}


