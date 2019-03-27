echo '
<#include '/uccm/aws/elasticbeanstalk/default_resource.json.ftl'>
' > resource.json
cat -n resource.json
aws cloudformation create-stack --stack-name ${stack_name} --template-body file://resource.json