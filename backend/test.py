import json


with open("test.json") as file:
    print(file.name)
    print(file.read())
    print(json.load(file))



# with open("test.json", "w") as file:
#     file.write(json.dumps({"A": "B"}, indent=2))





