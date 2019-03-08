from uccm.dynamic.file_store import TemplateFileStore

entity = request.entity
TemplateFileStore().save_planner(entity['name'], entity['planner'])
