<#function resolve key, default="">
    <#list dictionaries as dict>
        <#assign entries=dict.getProperty('entries')>
        <#if entries[key]?? >
            <#return entries[key]>
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