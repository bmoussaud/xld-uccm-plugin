import uccm.dynamic.planner.planner
import uccm.kubernetes.dynamic.stepmacros.steps

reload(uccm.dynamic.planner.planner)
reload(uccm.kubernetes.dynamic.stepmacros.steps)

from uccm.kubernetes.dynamic.stepmacros.steps import kubectl_cmd
from uccm.dynamic.planner.planner import DynamicPlanner


def create(planner):
    dynamic_type = planner.deployed.apiVersion
    template = "%s-create" % dynamic_type.replace("/", "-")
    planner.add_step_with_check_point(kubectl_cmd(planner, resource="configmap", order=planner.CREATE_RESOURCES,
                                                    deployed=planner.deployed, dynamic_deployed=planner.dynamic_deployed,
                                                    profile_template=planner.active_profile_template_path(template)))

def modify(planner):
    planner.destroy(planner)
    planner.create(planner)

def destroy(planner):
    dynamic_type = planner.deployed.apiVersion
    template = "%s-destroy" % dynamic_type.replace("/", "-")
    planner.add_step_with_check_point(kubectl_cmd(planner, resource="configmap", order=planner.DESTROY_RESOURCES,
                                                  deployed=planner.previous_deployed, dynamic_deployed=planner.previous_dynamic_deployed,
                                                  profile_template=planner.active_profile_template_path(template)))

DynamicPlanner(locals()).handle(create=create, modify=modify, destroy=destroy)
