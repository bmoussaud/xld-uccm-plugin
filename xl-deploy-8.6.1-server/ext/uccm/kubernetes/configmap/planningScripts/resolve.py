import uccm.deltas.compute

reload(uccm.deltas.compute)


import hashlib
import json


def resolve(deployed, config):
    #print "resolve config.id {0}".format(config.id)
    # https://blog.questionable.services/article/kubernetes-deployments-configmap-change/
    h = hashlib.md5(json.dumps(config.placeholders, sort_keys=True))
    short_h = str(int(h.hexdigest(), 16) % (10 ** 8))
    checksum = str(config.deployable.checksum)
    data_md5 = "d-{0}-f-{1}".format(short_h, checksum[0:10])
    config.data_hash = data_md5
    #print "resolve config.data_hash {0}".format(config.data_hash)
    resource_name = '{0}-{1}-{2}-configmap'.format(deployed.name, config.name, data_md5)
    config.resourceName = resource_name
    #print "resolve config.resourceName {0}".format(config.resourceName)


import traceback

try:
    for config in deployed.mountedFiles:
        resolve(deployed, config)
except:
    raise Exception(str(traceback.format_exc()))
