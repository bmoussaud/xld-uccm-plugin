<#assign application>${deployedApplication.version.application.name?lower_case}</#assign>
<#assign environment>${deployedApplication.environment.name?lower_case}</#assign>

{
  "AWSTemplateFormatVersion": "2010-09-09",
  "Resources": {
    "${application}": {
      "Type": "AWS::ElasticBeanstalk::Application",
      "Properties": {
        "Description": "${application} Application"
      }
    },
    "${application}Version": {
      "Type": "AWS::ElasticBeanstalk::ApplicationVersion",
      "Properties": {
        "ApplicationName": {
          "Ref": "${application}"
        },
        "Description": "${application}/${deployedApplication.version.name} Application Version",
        "SourceBundle": {
          "S3Bucket": "xld-elasticbeanstalk-${deployed.container.region}",
          "S3Key": "${deployed.file.name}"
        }
      }
    },
    "${application}ConfigurationTemplate": {
      "Type": "AWS::ElasticBeanstalk::ConfigurationTemplate",
      "Properties": {
        "ApplicationName": {
          "Ref": "${application}"
        },
        "Description": "${application} Configuration Template",
        "SolutionStackName": "${deployed.solutionStackName}"
      }
    },
    "${application}Env": {
      "Type": "AWS::ElasticBeanstalk::Environment",
      "Properties": {
        "ApplicationName": {
          "Ref": "${application}"
        },
        "TemplateName": {
          "Ref": "${application}ConfigurationTemplate"
        },
        "VersionLabel": {
          "Ref": "${application}Version"
        },
        "CNAMEPrefix": "${application}-${deployed.container.region}-${environment}",
        "EnvironmentName": "${application}-${environment}",
        "OptionSettings" : [
          {
            "Namespace": "aws:autoscaling:launchconfiguration",
            "OptionName": "IamInstanceProfile",
            "Value": "aws-elasticbeanstalk-ec2-role"
          },
          {
            "Namespace": "aws:autoscaling:asg",
            "OptionName": "MinSize",
            "Value": "2"
          },
          {
            "Namespace": "aws:autoscaling:asg",
            "OptionName": "MaxSize",
            "Value": "6"
          },
          {
            "Namespace": "aws:elasticbeanstalk:environment",
            "OptionName": "EnvironmentType",
            "Value": "LoadBalanced"
          }
          ]
      }
    }
  },
  "Outputs": {
    "URL": {
      "Description": "URL",
      "Value": {
        "Fn::GetAtt": ["${application}Env","EndpointURL"]
      }
    }
  }


}