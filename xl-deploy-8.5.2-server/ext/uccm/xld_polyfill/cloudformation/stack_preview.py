from uccm.xld_polyfill.cloudformation.utils.cfclient_proxy import CFClientUccmProxy


def process(task_vars):
    deployed = task_vars['deployed']
    environment = task_vars['environment']
    client = CFClientUccmProxy(deployed,  environment)
    return client.preview()


if __name__ == '__main__' or __name__ == '__builtin__':
    result = process(locals())
