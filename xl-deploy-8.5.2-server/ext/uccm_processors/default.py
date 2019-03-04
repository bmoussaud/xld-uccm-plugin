from uccm.utils.profile import ProcessorChain


def process(cf_template, profile_dictionary):
    return ProcessorChain(['sanatize']).process(cf_template, profile_dictionary)
