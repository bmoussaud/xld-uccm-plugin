#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import json
from overtherepy import OverthereHostSession


def inc_context():
    key = "wait_replicates_{0}".format(podname)
    if context.getAttribute(key) is None:
        context.setAttribute(key, int(0))
    value = context.getAttribute(key)
    value = value + 1
    context.setAttribute(key, value)


def get_value_context():
    key = "wait_replicates_{0}".format(podname)
    return context.getAttribute(key)


def get_available_replicas(data):
    try:
        return int(data['status']['availableReplicas'])
    except:
        return -1


#attempts = 10
def get_kubectl_command(container):
    kubectl = '{1}/kubectl --namespace={0}'.format(container.name,deployed.container.container.kubectlPath)
    if container.container.kubeConfigContext is not None:
        kubectl = kubectl + ' --context={0}'.format(deployed.container.container.kubeConfigContext)
    return kubectl

command_line = "{0} get {1} {2} -o=json".format(get_kubectl_command(deployed.container), resource, resourceName)
if get_value_context() == 0:
    print command_line

session = OverthereHostSession(target_host)
try:
    response = session.execute(command_line)
    data = json.loads(" ".join(response.stdout))

    condition = data['status']['conditions'][0]
    print "Status {status} {reason}: {message}".format(**condition)
    availableReplicas = get_available_replicas(data)
    print "availableReplicas {0}/{1}".format(availableReplicas, deployed.replicas)

    if condition['status'] == "True":
        print "Status Ok"
    elif availableReplicas == deployed.replicas:
        print "DONE replicas"
    else:
        inc_context()
        cpt = get_value_context()
        print "WAIT....{0}/{1}".format(cpt, attempts)
        if cpt < int(attempts):
            result = "RETRY"
        else:
            print "Too many attempts {0}".format(attempts)
            result = int(attempts)

finally:
    session.close_conn()
