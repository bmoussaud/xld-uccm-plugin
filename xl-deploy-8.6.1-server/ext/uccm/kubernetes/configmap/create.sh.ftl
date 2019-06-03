<#assign commandline = ["kubectl", "--namespace='${deployed.container.name}'"] />
<#if (deployed.container.container.kubeConfigContext??)>
    <#assign commandline = commandline + ["--context='${deployed.container.container.kubeConfigContext}'"]/>
</#if>

<#assign commandline = commandline + ["create","${resource}","${resourceName}"]/>

<#list deployed.data?keys as key>
    <#assign commandline = commandline + ["--from-literal=${key}=${deployed.data[key]}"]/>
</#list>

<#list deployed.propertyFiles as pf>
    <#assign commandline = commandline + ["--from-file=${(pf.file)!pf.name}"]/>
</#list>

echo Executing <#list commandline as item>${item} </#list>
<#list commandline as item>${item} </#list>


    
