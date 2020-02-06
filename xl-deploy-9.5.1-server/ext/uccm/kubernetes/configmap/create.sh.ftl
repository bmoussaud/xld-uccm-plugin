<#assign commandline = ["${deployed.container.container.kubectlPath}/kubectl", "--namespace='${deployed.container.name}'"] />
<#if (deployed.container.container.kubeConfigContext??)>
    <#assign commandline = commandline + ["--context='${deployed.container.container.kubeConfigContext}'"]/>
</#if>

<#assign commandline = commandline + ["create","${resource}","${resourceName}"]/>
<#assign commandline = commandline + ["--from-file=${ci.file.path}"]/>

echo Executing <#list commandline as item>${item} </#list>
<#list commandline as item>${item} </#list>


    
