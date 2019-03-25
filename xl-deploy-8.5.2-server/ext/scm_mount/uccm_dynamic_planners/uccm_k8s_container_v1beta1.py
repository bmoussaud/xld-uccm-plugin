import uccm.dynamic.planner.planner
import uccm.kubernetes.dynamic.stepmacros.steps
reload(uccm.dynamic.planner.planner)
reload(uccm.kubernetes.dynamic.stepmacros.steps)

from uccm.kubernetes.dynamic.stepmacros.steps import kubectl_delete, kubectl_apply, wait_resource_up
from uccm.dynamic.planner.planner import DynamicPlanner

NOOP = 'noop'


def create_modify(planner):
    dynamic_type = planner.deployed.apiVersion
    profile = dynamic_type.replace("/", "-")
    planner.add_step_with_check_point(kubectl_apply(planner, resource="deployment", order=planner.CREATE_RESOURCES,
                                                    ci=planner.dynamic_deployed, profile=profile))
    planner.add_step(wait_resource_up(planner, resource="deployment", order=planner.CREATE_RESOURCES + 2,
                                      ci=planner.dynamic_deployed, resource_name="{0}-depl".format(planner.deployed.name)
                                      ))

    def add_create_steps(port, order_offset, resource_type):
        resource_profile = "%s-%s" % (profile, resource_type)
        resource_name = '{0}-{1}-{2}'.format(planner.deployed.name,port['name'], resource_type)
        planner.add_step_with_check_point(kubectl_apply(planner, resource=resource_type,
                                                        order=planner.CREATE_RESOURCES + order_offset, ci=port,
                                                        profile=resource_profile))
        resource_order = planner.CREATE_RESOURCES + order_offset + 1
        planner.add_step(wait_resource_up(planner, resource=resource_type, order=resource_order, ci=port,
                                          resource_name=resource_name))

    for p in planner.dynamic_deployed['ports']:
        if p['exposeAsService']:
            add_create_steps(p, 3, "service")
            if p['exposeAsIngress']:
                add_create_steps(p, 5, "ingress")


def destroy(planner):
    planner.add_step_with_check_point(kubectl_delete(planner, resource="deployment", order=planner.DESTROY_RESOURCES,
                                                     resource_name="{0}-depl".format(planner.previous_deployed.name)))

    def add_delete_steps(port, resource_type):
        resource_name = '{0}-{1}-{2}'.format(planner.previous_deployed.name, port['name'], resource_type)
        planner.add_step_with_check_point(kubectl_delete(planner, resource=resource_type, order=planner.DESTROY_RESOURCES + 3,
                                                         resource_name=resource_name))
        planner.add_step(NOOP, {
            "description": 'Wait for {4} {1}/{0} deleted on {2}'.format(port['name'],
                                                                        planner.previous_deployed.name,
                                                                        planner.previous_deployed.container.name,
                                                                        resource_type),
            "order": planner.DESTROY_RESOURCES + 4,
            "ci": port,
            "resourceName": '{0}-{1}-service'.format(planner.deployed.name, port['name'])
        })

    for p in planner.previous_dynamic_deployed['ports']:
        if p['exposeAsService']:
            add_delete_steps(p, "service")
            if p['exposeAsService']:
                add_delete_steps(p, "ingress")


DynamicPlanner(locals()).handle(create_modify=create_modify, destroy=destroy)
