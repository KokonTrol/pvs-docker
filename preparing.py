import requests

headers = {
        'fiware-service': 'openiot',
    }
path = 'http://localhost:1026/v2/entities'

def get_all_entity_id(type_name: str):
    objects_id = []

    response = requests.get(
        path,
        headers=headers
    )
    response_json = response.json()
    for obj in response_json:
        if (obj['type'] == type_name):
            objects_id.append(obj['id'].split(":")[-1])
    print(objects_id)
    return objects_id

if __name__ == "__main__":
    get_all_entity_id("Status")
