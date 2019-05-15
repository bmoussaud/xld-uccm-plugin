{
  "kind": "Deployment",
  "apiVersion": "extensions/v1beta1",
  "metadata": {
    "name": "${resourceName}",
    "labels": {
      "application": "${application}",
      "component": "${deployed.name}",
      "canary": "true"
    },
    "annotations": {
      "xldeploy.com/version": "${version}",
      "xldeploy.com/environment": "${environment}"
    }
  },
  "spec": {
    "replicas": 1,
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
        "component": "${deployed.name}",
        "canary": "true"
      }
    },
    "template": {
      "metadata": {
        "name": "${resourceName}",
        "labels": {
          "application": "${application}",
          "component": "${deployed.name}",
          "version": "${version}",
          "canary": "true"
        }
      },
      "spec": {
        "volumes": [
        <#list deployed.mountedVolumes as vol>
          <#if vol.isSensitive>
          {
            "name": "${vol.name}-volume",
            "secret": {
              "secretName": "${vol.name}"
            }
          }
          <#else>
          {
            "name": "${vol.name}-volume",
            "configMap": {
              "name": "${vol.name}",
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
            "name": "${deployed.name}-canary",
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
             ],
            "volumeMounts": [
            <#list deployed.mountedVolumes as vol>
              {
                  "name": "${vol.name}-volume",
                  "readOnly": true,
                  "mountPath": "${vol.path}"
              }
              <#sep>,
             </#list>
             ],
            "terminationMessagePath": "/dev/termination-log",
            "terminationMessagePolicy": "File",
            "imagePullPolicy": "IfNotPresent"
          }
        ],
        "restartPolicy": "Always",
        "terminationGracePeriodSeconds": 30
      }
    }
  }
}



