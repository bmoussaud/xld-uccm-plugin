from uccm.dynamic.file_store import TemplateFileStore

if "name" in request.query.keys():
    response.entity = TemplateFileStore().read_planner(request.query['name'])
else:
    response.entity = TemplateFileStore().list_planner_names()
