from uccm.dynamic.file_store import TemplateFileStore

entity = request.entity
TemplateFileStore().save_template(entity['name'], entity['type'], entity['template'])
