from uccm.utils.freemarker_renderer import FreemarkerRenderer
from uccm.utils.profile import ProfileDictionary, ProfileProcessor
from uccm.dynamic.file_store import TemplateFileStore
import jsonschema
import json
from syntactical.sugar import unwrap


class DynamicPlanner(object):
    PRE_FLIGHT = 0
    STOP_ARTIFACTS = 10
    STOP_CONTAINERS = 20
    UNDEPLOY_ARTIFACTS = 30
    DESTROY_RESOURCES = 40
    CREATE_RESOURCES = 60
    DEPLOY_ARTIFACTS = 70
    START_CONTAINERS = 80
    START_ARTIFACTS = 90
    POST_FLIGHT = 100

    def __init__(self, planner_vars):
        self.vars = planner_vars
        self.steps = planner_vars['steps']
        self.context = planner_vars['context']
        self.delta = planner_vars['delta']
        self.deployed_application = planner_vars['deployedApplication']
        self.profile_dictionary = ProfileDictionary(self.deployed_application.environment.profileDictionaries)
        self.deployed = planner_vars['deployed']
        self.previous_deployed = planner_vars['previousDeployed']
        if self.deployed.hasProperty("jsonSpec"):
            self.dynamic_deployed = json.loads(self.deployed.jsonSpec)
            self.previous_dynamic_deployed = None if self.previous_deployed is None else json.loads(self.deployed.jsonSpec)
            self.validate_dynamic_deployed()

    def handle(self, create=None, modify=None, create_modify=None, destroy=None):
        if create_modify is not None:
            create = create_modify
            modify = create_modify

        operation = str(self.delta.operation)
        if operation == 'CREATE':
            create(self)
        elif operation == 'DESTROY':
            destroy(self)
        elif operation == 'MODIFY':
            modify(self)

    def add_step_with_check_point(self, step, parameters=None):
        if isinstance(step, basestring):
            self.context.addStepWithCheckpoint(self.steps[step](**parameters), self.delta)
        else:
            self.context.addStepWithCheckpoint(step, self.delta)

    def add_step(self, step, parameters=None):
        if isinstance(step, basestring):
            self.context.addStep(self.steps[step](**parameters))
        else:
            self.context.addStep(step)

    def get_active_template_profile(self, dynamic_type):
        return self.profile_dictionary.resolve(dynamic_type, dynamic_type)

    def active_profile_template_path(self, dynamic_type, ext="json.ftl"):
        return "/scm_mount/uccm_templates/%s.%s" % (self.get_active_template_profile(dynamic_type), ext)

    def validate_dynamic_deployed(self):
        schema = TemplateFileStore().read_spec_json_file(self.deployed.apiVersion.replace("/", "-"))
        jsonschema.validate(instance=self.dynamic_deployed, schema=schema)

    def process_profile_template(self, profile, **context):
        freemarker_context = {"deployed": self.deployed._delegate,  "previousDeployed": unwrap(self.previous_deployed),
         "deployedApplication": unwrap(self.deployed_application), "dictionaries": self.profile_dictionary}
        freemarker_context.update(context)
        fm = FreemarkerRenderer(freemarker_context)
        result = fm.evaluate_template_from_path(self.active_profile_template_path(profile))
        json_template = json.loads(result)
        process_template = ProfileProcessor(self.deployed, self.deployed_application).process(json_template, profile)
        return  json.dumps(process_template, indent=4)

