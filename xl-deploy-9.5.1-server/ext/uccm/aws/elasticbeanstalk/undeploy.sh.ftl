aws cloudformation delete-stack --stack-name ${previousDeployed.name}-${deployedApplication.version.application.name}-${deployedApplication.environment.name} --region ${previousDeployed.container.region}