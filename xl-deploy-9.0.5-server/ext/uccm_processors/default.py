from uccm.utils.profile import ProcessorChain


def process(cf_template, profile_dictionary):
    return ProcessorChain(['noop']).process(cf_template, profile_dictionary)
