from com.xebialabs.deployit.plugin.generic.freemarker import ConfigurationHolder, CiAwareObjectWrapper
from java.io import StringWriter, StringReader
from java.util import HashMap
from freemarker.template import Template


class FreemarkerRenderer(object):
    def __init__(self, context, mask_passwords=True):
        self.context = HashMap(context)
        self.mask_passwords = mask_passwords
        self.cfg = ConfigurationHolder.getConfiguration()

    def _evalute_resolved_template(self, template):
        sw = StringWriter()
        template.createProcessingEnvironment(self.context, sw, CiAwareObjectWrapper(None, self.mask_passwords)).process()
        return sw.toString()

    def evaluate_template(self, template):
        template = Template("expression", StringReader(template), self.cfg)
        return self._evalute_resolved_template(template)

    def evaluate_template_from_path(self, template_path):
            template = self.cfg.getTemplate(template_path)
            return self._evalute_resolved_template(template)
