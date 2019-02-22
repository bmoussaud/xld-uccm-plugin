<#import "/uccm/ftl/dictionary.ftl" as dict>
{
    "kind": "Deployment",
    "apiVersion": "extensions/v1beta1",
    "metadata": {
    "name": "${deployed.name}-depl",
    "labels": {
        "application": "${application}",
        "version": "${version}"
        "environment": "${dict.resolve('env', 'test2')}"
    }
}