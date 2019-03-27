#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import json
from overtherepy import OverthereHostSession


def inc_context(name):
    key = "wait_replicates_{0}".format(name)
    if context.getAttribute(key) is None:
        context.setAttribute(key, int(0))
    value = context.getAttribute(key)
    value = value + 1
    context.setAttribute(key, value)


def get_value_context(name):
    key = "wait_replicates_{0}".format(name)
    return context.getAttribute(key)


def get_available_replicas(data):
    try:
        return int(data['status']['availableReplicas'])
    except:
        return -1


deployment_name = "{0}-depl".format(ci.name)
command_line = "{2} get {3} {0} --namespace={1} -o=json".format(deployment_name, ci.container.name, 'kubectl', resource)
print command_line

session = OverthereHostSession(target_host)
try:
    response = session.execute(command_line)
    rc = response.rc
    if rc != 0:
        print "Non zero Exit Code {0}".format(rc)
        result="RETRY"
    else:
        data = json.loads(" ".join(response.stdout))

        condition = data['status']['conditions'][0]
        print "Status {status} {reason}: {message}".format(**condition)
        availableReplicas = get_available_replicas(data)
        print "availableReplicas {0}/{1}".format(availableReplicas, ci.replicas)

        if condition['status'] == "True":
            print "Status Ok"
        elif availableReplicas == ci.replicas:
            print "DONE replicas"
        else:
            inc_context(deployment_name)
            cpt = get_value_context(deployment_name)
            print "WAIT....{0}/{1}".format(cpt, attempts)
            if cpt < int(attempts):
                result = "RETRY"
            else:
                print "Too many attempts {0}".format(attempts)
                result = int(attempts)

finally:
    session.close_conn()
