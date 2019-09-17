{
  "kind": "Deployment",
  "apiVersion": "apps/v1",
  "metadata": {
    "name": "${resourceName}",
    "labels": {
      "application": "${application}",
      "component": "${deployed.name}"
    },
    "annotations": {
      "xldeploy.com/version": "${version}",
      "xldeploy.com/environment": "${environment}"
    }
  },
  "spec": {
    "replicas": ${deployed.replicas},
    "strategy": {
      "type":"RollingUpdate",
      "rollingUpdate": {
        "maxSurge": 1,
        "maxUnavailable": 0
      }
    },
    "selector": {
      "matchLabels": {
        "application": "${application}",
        "component": "${deployed.name}"
      }
    },
    "template": {
      "metadata": {
        "name": "${resourceName}",
        "labels": {
          "application": "${application}",
          "component": "${deployed.name}",
          "version": "${version}"
        }
      },
      "spec": {
        "volumes": [
        <#list deployed.mountedVolumes + deployed.mountedFiles as vol>
          <#if vol.isSensitive>
          {
            "name": "${vol.resourceName}-v",
            "secret": {
              "secretName": "${vol.resourceName }"
            }
          }
          <#else>
          {
            "name": "${vol.resourceName}-v",
            "configMap": {
              "name": "${vol.resourceName}",
              "defaultMode": 420
            }
          }
          </#if>
          <#sep>,
        </#list>
        ],
        "imagePullSecrets": [
        <#list deployed.container.container.securedRegistries as securedRegistry>
          {
            "name":"${deployed.name}-${securedRegistry.name}-secret"
          }
        <#sep>,
        </#list>
        ],
        "containers": [
          {
            "name": "${deployed.name}",
            "image": "${deployed.image}",
            "ports": [
              <#list deployed.ports as port>
              {
                "containerPort": ${port.containerPort},
                "protocol": "TCP"
              }
              <#sep>,
              </#list>
            ],
             "env": [
               <#list deployed.env?keys as k>{
                    "name": "${k}",
                    "value": "${deployed.env[k]}"
                 }
               <#sep>,
               </#list>
               <#if (deployed.securedEnv?size > 0)>,</#if>
                   <#list deployed.securedEnv?keys as k>{
                   "name": "${k}",
                   "valueFrom": {
                       "secretKeyRef" :{
                         "name":"${deployed.resourceName}-securedenv",
                         "key": "${k}"
                       }
                   }
                }
               <#sep>,
               </#list>
             ],
            "volumeMounts": [
            <#list deployed.mountedVolumes + deployed.mountedFiles as vol>
              {
                  "name": "${vol.resourceName}-v",
                  "readOnly": true,
                  "mountPath": "${vol.path}"
              }
              <#sep>,
             </#list>
             ],
            "terminationMessagePath": "/dev/termination-log",
            "terminationMessagePolicy": "File",
            "imagePullPolicy": "IfNotPresent",
            "resources": {
                "requests": {
                    "memory":"512Mi",
                    "cpu": "500m"
                },
                "limits": {
                    "memory":"GMi",
                    "cpu": "1"
                }

            },
            "readinessProbe": {
              "httpGet": {
                "path": "/management/health",
                "port": "http"
              },
              "initialDelaySeconds": 20,
              "periodSeconds": 15,
              "failureThreshold": 6
            },
            "livenessProbe": {
              "httpGet": {
                "path": "/management/health",
                "port": "http"
              },
              "initialDelaySeconds": 120
            }
          }
        ],
        "restartPolicy": "Always",
        "terminationGracePeriodSeconds": 30
      }
    }
  }
}



