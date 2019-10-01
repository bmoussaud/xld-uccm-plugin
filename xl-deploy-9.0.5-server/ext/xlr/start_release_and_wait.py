import requests
import json
import sys

RELEASE_ID_UCCM = "RELEASE_ID_UCCM"

headers = {'content-type': 'application/json',
           'Accept': 'application/json'}
payload = {
    "releaseTitle": "xl-demo-uccm-app-canary",
    "folderId": folderId,
    "variables": {
        "application": applicationName,
        "stage": "xl-demo-production"
    },
    "releaseVariables": {
        "application": applicationName,
        "stage": "xl-demo-production"
    },
    "scheduledStartDate": None,
    "autoStart": "true"
}


if context.getAttribute(RELEASE_ID_UCCM) is None:
    print ("Start a release {0}".format(xlreleaseServer.url))
    print (json.dumps(payload))
    #templateId="Release7d25ce2f75224fae947f1bedd1f0440e"
    #http://localhost:5516/api/v1/templates/Release7d25ce2f75224fae947f1bedd1f0440e/create
    url_create="{0}/api/v1/templates/{1}/create".format(xlreleaseServer.url,templateId)
    print(url_create)

    print(json.dumps(payload))
    r = requests.post(url_create,
                      auth=(xlreleaseServer.username, xlreleaseServer.password),
                      data=json.dumps(payload),
                      headers=headers)
    print(r.status_code)
    if r.status_code == 500:
        print r.text()
        sys.exit(2)
        
    output =  r.json()
    release_id = output['id']
    print "Release id {0}".format(release_id)
    context.setAttribute(RELEASE_ID_UCCM, release_id)



release_id = context.getAttribute(RELEASE_ID_UCCM)
#print ("Check the status of {0}".format(release_id))
url_check="{0}/api/v1/templates/{1}".format(xlreleaseServer.url,release_id)
#print(url_check)
r=requests.get(url_check,auth=(xlreleaseServer.username, xlreleaseServer.password),headers=headers )
status = r.json()['status']
if status == "COMPLETED":
    result = "DONE"
    print "reset context"
    context.setAttribute(RELEASE_ID_UCCM,None)
else:
    result = "RETRY"



