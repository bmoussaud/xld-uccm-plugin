<#function resolve key, default="">
    <#list dictionaries as dict>
        <#assign this=dict.getProperty('entries')>
        <#if this[key]?? >
            <#assign template_value=this[key]>
            <#assign inlineTemplate = template_value?interpret>
            <#assign resolved_value><@inlineTemplate /></#assign>
            <#return resolved_value>
        </#if>
        <#assign encryptedEntries=dict.getProperty('encryptedEntries')>
        <#if encryptedEntries[key]?? >
            <#return encryptedEntries[key]>
        </#if>
    </#list>
    <#if default?has_content>
        <#return default>
    </#if>
    <#stop  "Dictionary key '${key}' is not resolved!!!!!">
</#function>