#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import json
import sys
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


def dump_std_response(response):
    for line in response.stdout:
        print line
    for line in response.stderr:
        print line

result=""
stack_status=""
command_line = "{0} cloudformation describe-stacks --stack-name {1} --region {2}".format('aws', stack_name,previousDeployed.container.region)

if get_value_context(stack_name) == None:
    print command_line

session = OverthereHostSession(target_host)
while True:
    try:
        response = session.execute(command_line, check_success=False)
        rc = response.rc

        if rc != 0:
            dump_std_response(response)
            if rc == 255:
                #An error occurred (ValidationError) when calling the DescribeStacks operation: Stack with id aws-prod-petweb-petclinic-europ-prod does not exist
                break
            else:
                print "Non zero Exit Code {0}".format(rc)
                raise Exception("Non zero Exit Code {0}".format(rc))

        data = json.loads(" ".join(response.stdout))
        if get_value_context(stack_name) == None:
            stack_id =  data['Stacks'][0]['StackId']
            print stack_id

        new_stack_status =  data['Stacks'][0]['StackStatus']
        if new_stack_status == stack_status:
            sys.stdout.write(".")
        else:
            sys.stdout.write("\n")
            sys.stdout.write(new_stack_status)
            stack_status = new_stack_status

        if stack_status == "ROLLBACK_COMPLETE" or stack_status == "UPDATE_ROLLBACK_COMPLETE":
            sys.stdout.write("\n")
            print "KO"
            sys.exit(1)
            break
        else:
            result="RETRY"
    finally:
        if result == "RETRY":
            inc_context(stack_name)
            cpt = get_value_context(stack_name)
            #print "WAIT....{0}/{1}".format(cpt, attempts)
            if cpt < int(attempts):
                result = "RETRY"
                import time
                time.sleep(5)
            else:
                print "Too many attempts {0}".format(attempts)
                result = int(attempts)

session.close_conn()
