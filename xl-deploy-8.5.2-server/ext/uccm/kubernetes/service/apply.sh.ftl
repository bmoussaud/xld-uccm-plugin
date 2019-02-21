echo '
{
  "kind": "Service",
  "apiVersion": "v1",
  "metadata": {
    "name": "${deployed.name}-${ci.name}-service",
    "labels": {
      "application": "${application}",
      "version": "${version}"
    }
  },
  "spec": {
    "ports": [
      {
        "port": ${ci.containerPort},
        "targetPort": <#if ci.servicePort??>${ci.servicePort}<#else>${ci.containerPort}</#if>,
        "protocol": "TCP",
        "name": "${ci.name}"
      }
    ],
    "selector": {
      "application": "${application}",
      "version": "${version}"
    },
    "type":"ClusterIP"
    }
  }
' > service.json
cat -n service.json
kubectl apply -f service.json --validate=true -n ${deployed.container.name}


