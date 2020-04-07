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
    command_line = "{0} get {1} -l=component={2} -o json".format(get_kubectl_command(ci.container), 'pods', ci.name)
    print command_line
    response = session.execute(command_line)
    if response.rc == 0:
        data = json.loads(" ".join(response.stdout))
        for item in data['items']:
            pods.append(item['metadata']['name'])
    return pods


def get_pod_events(ci, pod_name):
    events = []
    session = OverthereHostSession(target_host)
    command_line = "{0} get {1} --field-selector involvedObject.name={2} -o json".format(
        get_kubectl_command(ci.container), 'event',
        pod_name)
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


def get_kubectl_command(container):
    kubectl = '{1}/kubectl --namespace={0}'.format(container.name,deployed.container.container.kubectlPath)
    if container.container.kubeConfigContext is not None:
        kubectl = kubectl + ' --context={0}'.format(deployed.container.container.kubeConfigContext)
    return kubectl


def dump_events():
    for pod in get_associated_pods(ci):
        print "Pod {0}".format(pod)
        print "-------------------"
        for event in get_pod_events(ci, pod):
            print event


command_line = "{0} get {1} {2} -o=json".format(get_kubectl_command(ci.container), resource, resourceName)
print command_line
session = OverthereHostSession(target_host)

try:
    response = session.execute(command_line, suppress_streaming_output=True)
    rc = response.rc
    if rc != 0:
        print "Non zero Exit Code {0}".format(rc)
        result = "RETRY"
    else:
        data = json.loads(" ".join(response.stdout))
        if not 'condition' in data['status']:
            print data['status']
            result = "RETRY"
        else:
            for condition in data['status']:
                print "Status {status} {reason}: {message}".format(**condition)

            availableReplicas = get_available_replicas(data)
            print "availableReplicas {0}/ replicas {1}".format(availableReplicas, ci.replicas)

            if availableReplicas >= ci.replicas:
                print "DONE replicas"
                dump_events()
            else:
                inc_context(resourceName)
                cpt = get_value_context(resourceName)
                print "WAIT....{0}/{1}".format(cpt, attempts)
                if cpt < int(attempts):
                    result = "RETRY"
                else:
                    print "Too many attempts {0}".format(attempts)
                    dump_events()
                    result = int(attempts)

finally:
    session.close_conn()
