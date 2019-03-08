import json


class DynamicDeployedSelector(object):

    @staticmethod
    def spec(deployed):
        return json.loads(deployed.jsonSpec)

    @staticmethod
    def match_api_version(delta, version):
        if delta.deployed:
            return delta.deployed.apiVersion == version

        if delta.previousDeployed:
            return delta.previousDeployed.apiVersion == version
        return False


