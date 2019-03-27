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



result=""
resourceName=stack_name
#aws cloudformation describe-stacks --stack-name petclinic-PetStalk-aws --query 'Stacks[0].StackStatus'
command_line = "{0} cloudformation describe-stacks --stack-name {1} ".format('aws', stack_name)
if get_value_context(resourceName) == 0:
    print command_line

session = OverthereHostSession(target_host)
try:
    response = session.execute(command_line, check_success=False)
    rc = response.rc
    if rc != 0:
        print "Non zero Exit Code {0}".format(rc)
        result="RETRY"
    else:
        data = json.loads(" ".join(response.stdout))
        #print data
        stack_status =  data['Stacks'][0]['StackStatus']
        print stack_status

        if stack_status == "CREATE_COMPLETE":
            print "OK"
        else:
            result="RETRY"
finally:
    if result == "RETRY":
        inc_context(resourceName)
        cpt = get_value_context(resourceName)
        #print "WAIT....{0}/{1}".format(cpt, attempts)
        if cpt < int(attempts):
            result = "RETRY"
        else:
            print "Too many attempts {0}".format(attempts)
            result = int(attempts)

    session.close_conn()
