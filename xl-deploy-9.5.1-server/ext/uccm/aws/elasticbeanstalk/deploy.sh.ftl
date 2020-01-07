echo '
<#include '/uccm/aws/elasticbeanstalk/${deployed.profile}_resource.json.ftl'>
' > resource.json
cat -n resource.json
cp resource.json /tmp/cf.json

<#if operation == "CREATE">
<#assign command>create-stack</#assign>
<#else>
<#assign command>update-stack</#assign>
</#if>
echo "aws cloudformation ${command} --stack-name ${stack_name} --template-body file://resource.json --region ${deployed.container.region}"
aws cloudformation ${command} --stack-name ${stack_name} --template-body file://resource.json --region ${deployed.container.region}