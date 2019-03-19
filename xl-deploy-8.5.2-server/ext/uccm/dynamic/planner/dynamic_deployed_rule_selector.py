import json
from .planner import DynamicPlanner

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

    @staticmethod
    def process_profile_template(planner_vars):
        def process(profile, **context):
            return DynamicPlanner(planner_vars).process_profile_template(profile, **context)
        return process


