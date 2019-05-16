echo "kubectl scale --replicas=${nbreplicas} deployment/${resourceName} -n ${previousDeployed.container.name}"
kubectl scale --replicas=${nbreplicas} deployment/${resourceName} -n ${previousDeployed.container.name}


