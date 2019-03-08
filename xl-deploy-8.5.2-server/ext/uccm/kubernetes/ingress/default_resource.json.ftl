
{
  "kind": "Ingress",
  "apiVersion": "extensions/v1beta1",
  "metadata": {
    "name": "${deployed.name}-${ci.name}-ingress",
    "labels": {
      "application": "${application}",
      "version": "${version}"
    },
    "annotations": {
      "ingress.kubernetes.io/rewrite-target": "/${deployed.name}",
      "nginx.ingress.kubernetes.io/ssl-redirect": "false"
    }
  },
  "spec": {
    "rules": [
        {
          "http": {
            "paths": [
              {
                "path": "/${deployed.name}",
                "backend": {
                  "serviceName": "${deployed.name}-${ci.name}-service",
                  "servicePort": <#if ci.servicePort??>${ci.servicePort}<#else>${ci.containerPort}</#if>
                }
              }
            ]
          }
        }
      ]
    }
}
