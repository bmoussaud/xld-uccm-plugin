#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import json
import sys
from overtherepy import OverthereHostSession
from com.google.common.io import Resources
from java.nio.charset import Charset
from string import Template
from java.lang import Thread, Integer

def load_classpath_resource(resource):
    """
    Uploads the classpath resource to the session's working directory.
    :param resource: to find on the classpath to copy
    :return: string
    """
    url = Thread.currentThread().contextClassLoader.getResource(resource)
    if url is None:
        raise Exception("Resource [%s] not found on classpath." % resource)

    return Resources.toString(url, Charset.defaultCharset())



print "load {0}".format(template_url)
template_content = load_classpath_resource(template_url)
#print template_content
template = Template(template_content)
values = {'startDelay': smoketest.startDelay,
          'maxRetries':smoketest.maxRetries,
          'retryWaitInterval':smoketest.retryWaitInterval,
          'target_url': context.getAttribute(deployed.id),
          'expectedResponseText':smoketest.expectedResponseText}


print values['target_url']

content = template.safe_substitute(values)
#print "-----------------"
#print content
#print "-----------------"
session = OverthereHostSession(target_host)
remote = session.upload_text_content_to_work_dir(content,'benoit_aws_test.sh',executable=True)
print remote.getPath()
response = session.execute(remote.getPath(),check_success=False)

for line in response.stdout:
    print line
for line in response.stderr:
    print line

rc = response.rc
if rc != 0:
    print "Non zero Exit Code: {0}".format(rc)
    sys.exit(rc)


