import base64

extra = dict()

encoded_secured_env = {}
for k, v in deployed.securedEnv.items():
    encoded = base64.b64encode(v)
    encoded_secured_env[str(k)] = str(encoded)

extra['encoded_secured_env']=encoded_secured_env

apply_step = steps.kubectlApply(
    **{'resource': 'secret',
       'resourceName': '{0}-securedenv'.format(deployed.resourceName),
       'order': 59,
       'ci': deployed,
       'profile': 'securedenv',
       'extra': extra})

context.addStepWithCheckpoint(apply_step, delta)
