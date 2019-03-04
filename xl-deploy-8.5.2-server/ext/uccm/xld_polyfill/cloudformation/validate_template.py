from uccm.xld_polyfill.cloudformation.utils.cfclient_proxy import CFClientUccmProxy


def process(task_vars):
    deployed = task_vars['deployed']
    environment = task_vars['environment']
    client = CFClientUccmProxy(deployed,  environment)
    response = client.validate_template()
    if response:
        print("Stack '%s' validated successfully." % deployed.name)
    else:
        raise Exception("Stack '%s' validation failed." % deployed.name)


if __name__ == '__main__' or __name__ == '__builtin__':
    process(locals())
