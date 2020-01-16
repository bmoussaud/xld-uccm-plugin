echo '
<#include '/uccm/aws/elasticbeanstalk/${deployed.profile}_resource.json.ftl'>
' > resource.json
cat -n resource.json
cp resource.json /tmp/cf.json
####
# https://github.com/jhipster/generator-jhipster/blob/4ce38d7d992a1f519fb6e579b7377409b978c80e/generators/aws/lib/eb.js
#  "ApplicationName": "${application}",
####

<#if operation == "CREATE">
<#assign command>create-stack</#assign>
<#else>
<#assign command>update-stack</#assign>
</#if>
echo "aws cloudformation ${command} --stack-name ${stack_name} --template-body file://resource.json --region ${deployed.container.region}"
aws cloudformation ${command} --stack-name ${stack_name} --template-body file://resource.json --region ${deployed.container.region}