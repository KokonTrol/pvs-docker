import requests
from time import sleep
from random import randint
parameters = ['is_occupied', 'has_problems']
variables = {"True": False, "False": True}
ids_list = None

def main():
    response = requests.get(
        'http://localhost:1026/v2/entities',
        headers = {'fiware-service': 'openiot'}
    )
    ids_list = [i['id'].split(':')[-1] for i in response.json()]
    while(True):
        sleep(randint(1, 3))
        ids = ids_list[randint(0, len(ids_list)-1)]
        par = parameters[randint(0, 1)]

        response = requests.get(
            f'http://localhost:1026/v2/entities/urn:ngsi-ld:Status:{ids}?type=Status',
            headers = {'fiware-service': 'openiot'}
        )
        if (response.json()[par]['value']):
            var = variables[response.json()[par]['value']]
        else:
            var = "True"

        print(f"Adding status{ids} {par}={var}")
        r = requests.post("http://localhost:7896/iot/d?k=4jggokgpepnvsb2uv4s40d59ov&i=status"+ids, 
        data=f'{par}|{var}',
        headers={'Content-Type':"text/plain"})
        print(r.status_code, r.reason)

if __name__ =="__main__":
    main()