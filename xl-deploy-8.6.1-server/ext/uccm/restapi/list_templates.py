import uccm.restapi.template_file_store
reload(uccm.restapi.template_file_store)

from uccm.restapi.template_file_store import TemplateFileStore

if all (k in request.query.keys() for k in ("name",  "type")):
    response.entity = TemplateFileStore().read_template(request.query['name'], request.query['type'])
else:
    response.entity = TemplateFileStore().list_template_names()
