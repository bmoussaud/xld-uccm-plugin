
{
  "kind": "Ingress",
  "apiVersion": "extensions/v1beta1",
  "metadata": {
    "name": "${resourceName}",
    "labels": {
      "application": "${application}",
      "version": "${version}",
      "component": "${deployed.name}"
    },
    "annotations": {
      "nginx.ingress.kubernetes.io/ssl-redirect": "false"
    }
  },
  "spec": {
          "rules": [
              {
                  "host": "${environment?lower_case}.${application?lower_case}.xebialabs.gke",
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
