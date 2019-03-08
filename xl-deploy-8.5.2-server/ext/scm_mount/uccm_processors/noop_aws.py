from uccm.utils.freemarker_renderer import FreemarkerRenderer
import json

def process(cf_template, profile_dictionary, deployed, deployed_application):
    fm = FreemarkerRenderer({"deployed": deployed, "dictionaries": deployed_application.environment.profileDictionaries})
    result = fm.evaluate_template_from_path("uccm_templates/test.json.ftl")
    return json.loads(result)

