{
  "kind": "Secret",
  "apiVersion": "v1",
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
  "type": "Opaque",
  "data": {
     <#list deployed.securedEnv?keys as k>
        "${k}": "${deployed.securedEnv[k]}"<#sep>,
     </#list>
  }
}

