{
  "kind": "Service",
  "apiVersion": "v1",
  "metadata": {
    "name": "${deployed.name}-${ci.name}-service",
    "labels": {
      "application": "${application}",
      "component": "${deployed.name}"
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
      "component": "${deployed.name}"
    },
    "type":"ClusterIP"
    }
  }
