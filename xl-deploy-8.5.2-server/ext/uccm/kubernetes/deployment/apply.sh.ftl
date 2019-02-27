echo '
{
  "kind": "Deployment",
  "apiVersion": "extensions/v1beta1",
  "metadata": {
    "name": "${deployed.name}-depl",
    "labels": {
      "application": "${application}",
      "version": "${version}"
    }
  },
  "spec": {
    "replicas": 1,
    "selector": {
      "matchLabels": {
        "application": "${application}",
        "version": "${version}"
      }
    },
    "template": {
      "metadata": {
        "name": "${deployed.name}-depl",
        "labels": {
          "application": "${application}",
          "version": "${version}"
        }
      },
      "spec": {
        "volumes": [
        <#list deployed.mountedVolumes as vol>
          {
            "name": "${vol.name}-volume",
            "configMap": {
              "name": "${vol.name}",
              "defaultMode": 420
            }
          }
        ],
        </#list>
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
              </#list>
            ],
            "volumeMounts": [
            <#list deployed.mountedVolumes as vol>
               {
                  "name": "${vol.name}-volume",
                  "mountPath": "${vol.path}"
              }
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
}' > deployment.json
cat -n deployment.json
kubectl apply -f deployment.json --validate=true -n ${deployed.container.name}


