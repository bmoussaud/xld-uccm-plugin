import os
from os import path


class TemplateFileStore(object):
    def __init__(self):
        self.base_dir = os.path.join(os.getcwd(), "ext", "uccm_templates")

    def list_template_names(self):
        onlyfiles = [f for f in os.listdir(self.base_dir) if path.isfile(path.join(self.base_dir, f))]
        only_json_ftl_files = [f[:-9] for f in onlyfiles if f.endswith(".json.ftl")]
        return only_json_ftl_files

    def _get_template_path(self, name):
        if not name.endswith(".json.ftl"):
            name = "%s.json.ftl" % name
        return path.join(self.base_dir, name)

    def read_template(self, name):
        file_path = self._get_template_path(name)
        if path.isfile(file_path):
            with open(file_path, "r") as f:
                return {"name": name, "template": f.read()}
        else:
            raise Exception("Template '%s' not found." % name)

    def save_template(self, name, content):
        file_path = self._get_template_path(name)
        with open(file_path, "w") as f:
                f.write(content)


entity = request.entity
TemplateFileStore().save_template(entity['name'], entity['template'])
