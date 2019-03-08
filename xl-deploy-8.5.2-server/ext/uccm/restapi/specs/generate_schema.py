from genson import SchemaBuilder

entity = request.entity

builder = SchemaBuilder()
builder.add_schema({"type": "object", "properties": {}})
builder.add_object(entity["spec"])

response.entity = builder.to_schema()
