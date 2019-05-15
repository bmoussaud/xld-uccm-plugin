#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import json
from overtherepy import OverthereHostSession


def get_associated_pods(ci):
    pods = []
    session = OverthereHostSession(target_host)
    command_line = "{1} get {2} -l=application=PetPortal  --namespace={0}  -o json".format(ci.container.name,
                                                                                           'kubectl',
                                                                                           'pods')
    response = session.execute(command_line)
    if response.rc == 0:
        data = json.loads(" ".join(response.stdout))
        for item in data['items']:
            pods.append(item['metadata']['name'])
    return pods


def get_pod_events(ci, pod_name):
    events = []
    session = OverthereHostSession(target_host)
    command_line = "{1} get {2} --field-selector involvedObject.name={3} --namespace={0}  -o json".format(
        ci.container.name,
        'kubectl',
        'event', pod_name)
    response = session.execute(command_line)
    if response.rc == 0:
        data = json.loads(" ".join(response.stdout))
        for item in data['items']:
            events.append("{type} {message}".format(**item))
    return events


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


command_line = "{2} get {3} {0} --namespace={1} -o=json".format(resourceName, ci.container.name, 'kubectl', resource)
print command_line

session = OverthereHostSession(target_host)


def dump_events():
    for pod in get_associated_pods(ci):
        print "Pod {0}".format(pod)
        print "-------------------"
        for event in get_pod_events(ci, pod):
            print event


try:
    response = session.execute(command_line)
    rc = response.rc
    if rc != 0:
        print "Non zero Exit Code {0}".format(rc)
        result = "RETRY"
    else:
        data = json.loads(" ".join(response.stdout))
        condition = data['status']['conditions'][0]
        print "Status {status} {reason}: {message}".format(**condition)
        availableReplicas = get_available_replicas(data)
        print "availableReplicas {0}/ replicas {1}".format(availableReplicas, ci.replicas)

        if availableReplicas >= ci.replicas:
            print "DONE replicas"
            dump_events()
        else:
            inc_context(deployment_name)
            cpt = get_value_context(deployment_name)
            print "WAIT....{0}/{1}".format(cpt, attempts)
            if cpt < int(attempts):
                result = "RETRY"
            else:
                print "Too many attempts {0}".format(attempts)
                dump_events()
                result = int(attempts)

finally:
    session.close_conn()
