from uccm.cloudformation.utils.cfclient_proxy import CFClientUccmProxy


def process(task_vars):
    deployed = task_vars['deployed']
    environment = task_vars['environment']
    client = CFClientUccmProxy(deployed,  environment)
    if client.create_stack():
        print("Stack '%s' created successfully." % deployed.name)
    else:
        raise Exception("Stack '%s' already exists." % deployed.name)


if __name__ == '__main__' or __name__ == '__builtin__':
    process(locals())
