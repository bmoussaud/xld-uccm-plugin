{
  "kind": "Ingress",
  "apiVersion": "v1",
  "metadata": {
    "name": "${deployed.name}-${ci.name}-ingress",
    "labels": {
      "application": "${application}",
      "version": "${version}",
      "production": "production"
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