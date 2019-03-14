from uccm.utils.profile import ProfileProcessor

process_template = ProfileProcessor(deployed, deployedApplication).process(data)
result = ProfileProcessor.formatted_json_string(process_template)