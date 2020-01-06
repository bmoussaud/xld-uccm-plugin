from com.xebialabs.deployit.plugin.api.deployment.specification import Operation

def dump_modified_delta(delta):
    print "DUMP %s " % delta
    ci_type = delta.deployed.type
    print ci_type
    ci_descriptor = metadataService.findDescriptor(Type.valueOf(str(ci_type)))
    print ci_descriptor
    for pd in ci_descriptor.getPropertyDescriptors():
        if pd.get(delta.deployed) == pd.get(delta.previous):
            prefix = "  "
        else:
            prefix = "XX"
        print "%s %s" % (prefix,pd)
        print "\t%s"  % (pd.get(delta.deployed))
        print "\t%s"  % (pd.get(delta.previous))

def modified_delta(delta):
    #deployed -> [(propertyname, value, previousvalue)]
    modified = {}
    ci_type = delta.deployed.type
    ci_descriptor = metadataService.findDescriptor(Type.valueOf(str(ci_type)))
    for pd in ci_descriptor.getPropertyDescriptors():
        if pd.get(delta.deployed) == pd.get(delta.previous):
            prefix = "  "
        else:
            prefix = "XX"
            modified[delta.deployed]=(pd, pd.get(delta.deployed), pd.get(delta.previous))
    return modified

def all_modified_deltas():
    all_modified_deltas = []
    for _delta in deltas.deltas:
        if _delta.getOperation() == Operation.MODIFY:
            data = modified_delta(_delta)
            if len(data) > 0 :
                all_modified_deltas.append(data)
    return all_modified_deltas


print "-------------------------------------------------------------------------------------"
print "------------  DELTA SPECIFICATION ---------------------------------------------------"
print "-------------------------------------------------------------------------------------"
for _delta in deltas.deltas:
    print "[%s] " % (_delta)
    if _delta.getOperation() == Operation.MODIFY:
        dump_modified_delta(_delta)
#print "ALL -------------------------------------------------------------------------------------"
#print all_modified_deltas()
#print "/ALL -------------------------------------------------------------------------------------"

