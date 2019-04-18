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
        "port": <#if ci.servicePort??>${ci.servicePort}<#else>${ci.containerPort}</#if>,
        "targetPort": ${ci.containerPort},
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
