
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
      "nginx.ingress.kubernetes.io/ssl-redirect": "false"
    }
  },
  "spec": {
          "rules": [
              {
                  "host": "${environment?lower_case}.${application?lower_case}.xebialabs.demo",
                  "http": {
                      "paths": [
                          {
                              "backend": {
                                  "serviceName": "${deployed.name}-${ci.name}-service",
                                  "servicePort": <#if ci.servicePort??>${ci.servicePort}<#else>${ci.containerPort}</#if>
                              },
                              "path": "/"
                          }
                      ]
                  }
              }
          ]
      }
}
