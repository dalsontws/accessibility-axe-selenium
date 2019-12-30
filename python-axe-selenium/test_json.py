from collections import Counter

a_dict = {
    "https://www.hdb.gov.sg/cs/infoweb/residential": {
        "inapplicable": [
            {
                "description": "Ensures every accesskey attribute value is unique",
                "help": "accesskey attribute value must be unique",
                "helpUrl": "https://dequeuniversity.com/rules/axe/3.1/accesskeys?application=axeAPI",
                "id": "accesskeys",
                "impact": 'null',
                "nodes": [],
                "tags": [
                    "best-practice",
                    "cat.keyboard"
                ]
            }]}}

# print(a_dict["https://www.hdb.gov.sg/cs/infoweb/residential"]["inapplicable"])

# print(type(a_dict))
for items in a_dict.values():
    print(items['inapplicable'])
    for item in items['inapplicable']:
        print(item['description'])
        print()
    # keys = Counter(items.values())
    # mode = keys.most_common(1)

# print(mode)
