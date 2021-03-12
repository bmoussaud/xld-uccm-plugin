s_data="{'replicas': 1, 
'readyReplicas': 1, 
'updatedReplicas': 1, 
'availableReplicas': 1, 
'conditions': [{'reason': 'MinimumReplicasAvailable', 'lastTransitionTime': '2020-04-12T09:27:19Z', 'message': 'Deployment has minimum availability.', 'type': 'Available', 'lastUpdateTime': '2020-04-12T09:27:19Z', 'status': 'True'}, {'reason': 'NewReplicaSetAvailable', 'lastTransitionTime': '2020-04-12T09:27:15Z', 'message': 'ReplicaSet tutorial-deployment-1.0.18-8587cb8db6 has successfully progressed.', 'type': 'Progressing', 'lastUpdateTime': '2020-04-12T09:27:19Z', 'status': 'True'}],
'observedGeneration': 1}"
import json

data = json.loads(s_data)
if not 'condition' in data['status']:
        print data['status']
        result = "RETRY"
else:
    for condition in data['status']:
        print "Status {status} {reason}: {message}".format(**condition)

print("-end")

