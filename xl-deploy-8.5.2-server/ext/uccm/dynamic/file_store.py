import json
import os
from os import path


class TemplateFileStore(object):
    def __init__(self):
        self.ftl_base_dir = os.path.join(os.getcwd(), "ext", "scm_mount", "uccm_templates")
        self.py_base_dir = os.path.join(os.getcwd(), "ext", "scm_mount", "uccm_processors")
        self.spec_base_dir = os.path.join(os.getcwd(), "ext", "scm_mount", "uccm_dynamic_specs")
        self.planner_base_dir = os.path.join(os.getcwd(), "ext", "scm_mount", "uccm_dynamic_planners")
        self.rules_file = os.path.join(os.getcwd(), "ext", "xl-rules.xml")

    @staticmethod
    def _find_templates(base_dir, ext, type_name):
        file_names = [f for f in os.listdir(base_dir) if path.isfile(path.join(base_dir, f))]
        offset = len(ext) * -1
        stripped = [f[:offset] for f in file_names if f.endswith(ext) and f != "__init__.py"]
        return[{"name": f, "type": type_name} for f in stripped]

    @staticmethod
    def _get_template_path(base_dir, ext, name):
        if not name.endswith(ext):
            name = "%s%s" % (name, ext)
        return path.join(base_dir, name)

    def _get_basedir_and_ext(self, type_name):
        base_dir = self.ftl_base_dir if type_name == "ftl" else self.py_base_dir
        ext = ".json.ftl" if type_name == "ftl" else ".py"
        return base_dir, ext

    def list_template_names(self):
        freemarker_templates = self._find_templates(self.ftl_base_dir, ".json.ftl", "ftl")
        py_templates = self._find_templates(self.py_base_dir, ".py", "py")
        py_templates.extend(freemarker_templates)
        return py_templates

    def read_template(self, name, type_name):
        base_dir, ext = self._get_basedir_and_ext(type_name)
        file_path = self._get_template_path(base_dir, ext, name)
        if path.isfile(file_path):
            with open(file_path, "r") as f:
                return {"name": name, "template": f.read(), "type": type_name}
        else:
            raise Exception("Template '%s' not found." % name)

    def save_template(self, name, type_name, content):
        base_dir, ext = self._get_basedir_and_ext(type_name)
        file_path = self._get_template_path(base_dir, ext, name)
        with open(file_path, "w") as f:
            f.write(content)

    def read_rules(self):
        if path.isfile(self.rules_file):
            with open(self.rules_file, "r") as f:
                return {"rules": f.read()}
        else:
            raise Exception("Rules '%s' not found." % str(self.rules_file))

    def save_rules(self, content):
        with open(self.rules_file, "w") as f:
            f.write(content)

    def list_spec_names(self):
        specs = self._find_templates(self.spec_base_dir, ".spec.json", "spec")
        return specs

    def read_spec(self, name):
        spec = self.read_spec_json_file(name)
        result = {"apiVersion": spec['apiVersion'], "spec": json.dumps(spec['spec'], indent=4), "schema": json.dumps(spec['schema'], indent=4)}
        return {"name": name, "spec": result, "type": "spec"}

    def read_spec_json_file(self, name):
        file_path = self._get_template_path(self.spec_base_dir, ".spec.json", name)
        if path.isfile(file_path):
            with open(file_path, "r") as f:
                spec = json.loads(f.read())
                return spec
        else:
            raise Exception("Spec '%s' not found." % name)

    def save_spec(self, name, content):
        file_path = self._get_template_path(self.spec_base_dir, ".spec.json", name)
        with open(file_path, "w") as f:
            f.write(json.dumps(content, indent=4))

    def list_planner_names(self):
        specs = self._find_templates(self.planner_base_dir, ".py", "plan")
        return specs

    def read_planner(self, name):
        file_path = self._get_template_path(self.planner_base_dir, ".py", name)
        if path.isfile(file_path):
            with open(file_path, "r") as f:
                return {"name": name, "planner": f.read(), "type": "plan"}
        else:
            raise Exception("Plan '%s' not found." % name)

    def save_planner(self, name, content):
        name = name.replace('-','/')
        file_path = self._get_template_path(self.planner_base_dir, ".py", name)
        with open(file_path, "w") as f:
            f.write(content)
