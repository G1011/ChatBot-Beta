import json
# import os
# path = 'data/stream.json'
# with open(path) as f:
#     data = json.load(f)
#
# # params={"course":"comp9021"}
# # #print(data["COMP9021"]["name"])
# #print(json.dumps(data, indent=4))
# for i in data:
#     if data[i]["name"] == "Bioinformatics":
#         #print(json.dumps(data[i], indent=4))
#         data = data[i]
#         break
# print(json.dumps(data, indent=4))
# print(data["name"])
# #print(data['COMPAS'])



path = 'knowledge_base.json'
with open(path) as f:
    data = json.load(f)

print(json.dumps(data,indent=4))