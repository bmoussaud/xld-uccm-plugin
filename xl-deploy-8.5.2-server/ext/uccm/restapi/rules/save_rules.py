from uccm.dynamic.file_store import TemplateFileStore

entity = request.entity
TemplateFileStore().save_rules(entity['rules'])
