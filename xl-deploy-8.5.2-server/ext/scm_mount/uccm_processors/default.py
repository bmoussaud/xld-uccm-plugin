from uccm.utils.profile import ProcessorChain


def process(cf_template, profile_dictionary, deployed, deployed_application):
    return ProcessorChain(['noop'],  deployed, deployed_application).process(cf_template)
