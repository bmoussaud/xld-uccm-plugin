set -x
aws s3 mb s3://xld-elasticbeanstalk-${deployed.container.region} --region ${deployed.container.region}
aws s3 cp ${deployed.file.path} s3://xld-elasticbeanstalk-${deployed.container.region}/${deployed.file.name} --region ${deployed.container.region} --acl public-read
