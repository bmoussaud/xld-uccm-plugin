## Installation v0.0.1

* Copy the [overtherepy jar file](https://github.com/xebialabs-community/overthere-pylib/releases/download/v0.0.4/overtherepy-0.0.4.jar) into the `XL_DEPLOY_SERVER/plugins/` directory.

* Copy the [xld-smoke-test-plugin](https://github.com/xebialabs-community/xld-smoke-test-plugin/releases/download/v1.0.6/xld-smoke-test-plugin-1.0.6.xldp) into the `XL_DEPLOY_SERVER/plugins/` directory.

* Copy the latest file from the [releases page](https://github.com/bmoussaud/xld-uccm-plugin/releases) into the `XL_DEPLOY_SERVER/plugins` directory.

* Create directories in the ext directory  :  ``mkdir ext/uccm_templates ext/uccm_processors  ext/uccm_profiles``

* Restart the XL Deploy server.



# Sample Content

````
xl apply --xl-deploy-url http://localhost:4537 -f xebialabs.yaml
[1/5] Applying configuration.yaml (imported by xebialabs.yaml)
    Updated CI Configuration/defaultMailServer
    Updated CI Configuration/defaultSmtpServer
    Updated CI Configuration/defaultMyXLR

[2/5] Applying infrastructure.yaml (imported by xebialabs.yaml)
    Updated CI Infrastructure/xl-demo/xl-demo-kube/xl-demo-staging
    Updated CI Infrastructure/xl-demo/xl-demo-kube/xl-demo-production
    Updated CI Infrastructure/xl-demo/xl-demo-kube
    Updated CI Infrastructure/xl-demo/localhost/test-runner-production
    Updated CI Infrastructure/xl-demo/localhost/test-runner-staging
    Updated CI Infrastructure/xl-demo/localhost
    Updated CI Infrastructure/xl-demo

[3/5] Applying environment.yaml (imported by xebialabs.yaml)
    Updated CI Environments/xl-demo/staging.conf
    Updated CI Environments/xl-demo/canary.conf
    Updated CI Environments/xl-demo/xl-demo-production
    Updated CI Environments/xl-demo/production.conf
    Updated CI Environments/xl-demo/xl-demo-staging
    Updated CI Environments/xl-demo

[4/5] Applying applications.yaml (imported by xebialabs.yaml)
    Updated CI Applications/xl-front-back-app/1.0.83/front/config
    Updated CI Applications/xl-front-back-app/1.0.83/front/sensitive-config
    Updated CI Applications/xl-front-back-app/1.0.83/front/web
    Updated CI Applications/xl-front-back-app/1.0.83/front
    Updated CI Applications/xl-front-back-app/1.0.83/back/web
    Updated CI Applications/xl-front-back-app/1.0.83/back
    Updated CI Applications/xl-front-back-app/1.0.83/uccm test application availability
    Updated CI Applications/xl-front-back-app/1.0.83
    Updated CI Applications/xl-front-back-app/1.0.82/front/config
    Updated CI Applications/xl-front-back-app/1.0.82/front/sensitive-config
    Updated CI Applications/xl-front-back-app/1.0.82/front/web
    Updated CI Applications/xl-front-back-app/1.0.82/front
    Updated CI Applications/xl-front-back-app/1.0.82/back/web
    Updated CI Applications/xl-front-back-app/1.0.82/back
    Updated CI Applications/xl-front-back-app/1.0.82/uccm test application availability
    Updated CI Applications/xl-front-back-app/1.0.82
    Updated CI Applications/xl-front-back-app/1.0.81/uccm test application availability
    Updated CI Applications/xl-front-back-app/1.0.81/front/config
    Updated CI Applications/xl-front-back-app/1.0.81/front/sensitive-config
    Updated CI Applications/xl-front-back-app/1.0.81/front/web
    Updated CI Applications/xl-front-back-app/1.0.81/front
    Updated CI Applications/xl-front-back-app/1.0.81/back/web
    Updated CI Applications/xl-front-back-app/1.0.81/back
    Updated CI Applications/xl-front-back-app/1.0.81
    Updated CI Applications/xl-front-back-app

[5/5] Applying xebialabs.yaml
Done
````


