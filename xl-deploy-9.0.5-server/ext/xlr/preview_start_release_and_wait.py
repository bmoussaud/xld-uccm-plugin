import requests

url_check="{0}/api/v1/templates/Applications/{1}".format(xlreleaseServer.url,templateId)
#print(url_check)
headers = {'content-type': 'application/json',
           'Accept': 'application/json'}

r=requests.get(url_check,auth=(xlreleaseServer.username, xlreleaseServer.password),headers=headers )

print ('  ')
print ('  ')
print ("Start a new release using the XLRelease Template '{0}' for the validation".format(r.json()['title']))

