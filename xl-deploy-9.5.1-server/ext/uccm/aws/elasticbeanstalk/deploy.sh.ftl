echo '
<#include '/uccm/aws/elasticbeanstalk/${deployed.profile}_resource.json.ftl'>
' > resource.json
cat -n resource.json
aws cloudformation update-stack --stack-name ${stack_name} --template-body file://resource.json