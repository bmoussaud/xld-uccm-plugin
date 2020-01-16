class StepGenerator():

    def __init__(self, delta, list_of_deltas):
        self.list_of_deltas = list_of_deltas
        self.delta = delta

    def create(self, delta, deployed, sub):
        print "-- create " + self

    def destroy(self, delta, deployed, sub):
        print "-- destroy.... "

    def noop(self, delta, deployed, sub):
        print "-- noop " + self


    def generate(self):
        for d in self.list_of_deltas:
            operation = d[0]
            if operation == "CREATE":
                self.create(self.delta, self.delta.deployed, d[1])
            elif operation == "DESTROY":
                self.destroy(self.delta, self.delta.previous, d[2])
            elif operation == "NOOP":
                self.noop(self.delta, self.delta.previous, d[1])
            elif operation == "MODIFY":
                self.destroy(self.delta, self.delta.previous, d[2])
                self.create(self.delta, self.delta.deployed, d[1])


class DeltasBuilder(object):

    def __init__(self):
        self.list_of_deltas = []

    def noOp(self, d):
        self.list_of_deltas.append(('NOOP', d, d))

    def modify(self, previous, d):
        self.list_of_deltas.append(('MODIFY', d, previous))

    def create(self, d):
        self.list_of_deltas.append(('CREATE', d, None))

    def destroy(self, d):
        self.list_of_deltas.append(('DESTROY', None, d))

    def build(self):
        return self.list_of_deltas

    def build2(self, operation, deployed, previous, property_name):
        if operation == "CREATE":
            [self.create(port) for port in deployed.getProperty(property_name)]
        elif operation == "DESTROY":
            [self.destroy(port) for port in previous.getProperty(property_name)]
        else:
            self.calculate_upgrade(previous.getProperty(property_name), deployed.getProperty(property_name))

        return self.build()

    def calculate_upgrade(self, oldDeployeds, newDeployeds):
        olds = set(oldDeployeds)
        news = set(newDeployeds)

        for old in olds:
            aNew = find_similar(old, news)
            if aNew != None:
                news.remove(aNew)
                if is_different(old, aNew):
                    self.modify(old, aNew)
                else:
                    self.noOp(aNew)
            else:
                self.destroy(old)

        for aNew in news:
            self.create(aNew)


def find_similar(old, news):
    for aNew in news:
        if is_similar(old, aNew):
            return aNew
    return None


def is_similar(old, new):
    return new.getId() == old.getId() and old.getType() == new.getType()


def get_modified_properties(deployed, previous):
    # [(propertyname, value, previousvalue)]
    modified_properties = []
    if deployed == None or previous == None:
        return modified_properties

    ci_type = deployed.type
    # ci_descriptor = metadataService.findDescriptor(Type.valueOf(str(ci_type)))
    ci_descriptor = ci_type.getDescriptor()
    for pd in ci_descriptor.getPropertyDescriptors():
        result = (pd, pd.get(deployed), pd.get(previous))
        print("%s:%s<->%s" % (result))
        if "deployable" == pd.getName() or "container" == pd.getName() or pd.isHidden() or pd.isTransient():
            continue
        if not (pd.areEqual(deployed, previous)):
            print(" add %s:%s<->%s" % (result))
            modified_properties.append(result)
    return modified_properties


def is_different(old, new):
    return len(get_modified_properties(new, old)) > 0


def calculate_upgrade(builder, oldDeployeds, newDeployeds):
    olds = set(oldDeployeds)
    news = set(newDeployeds)

    for old in olds:
        aNew = find_similar(old, news)
        if aNew != None:
            news.remove(aNew)
            if is_different(old, aNew):
                builder.modify(old, aNew)
            else:
                builder.noOp(aNew)
        else:
            builder.destroy(old)

    for aNew in news:
        builder.create(aNew)
    return builder
