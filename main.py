from fastapi import FastAPI, Request  
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import requests
import json
import asyncio
from fastapi import WebSocket

from preparing import get_all_entity_id

app = FastAPI()
templates = Jinja2Templates(directory="static")
app.mount("/static", StaticFiles(directory="static"), name="static")



objects_id = get_all_entity_id("Status")
attrs = ['is_occupied', 'has_problems']
subs_headers = {
    'fiware-service': 'openiot', 'fiware-servicepath': '/',
}

subs_params = {
    'type': 'Status',
    'lastN': '2',
}
subs_path = 'http://localhost:8666/STH/v2/entities/'
delete_subs_path = 'http://localhost:8666/STH/v1/contextEntities/type/Status/id'


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/all_objects")
def all_objects():
    response = requests.get(
        'http://localhost:1026/v2/entities',
        headers = {'fiware-service': 'openiot'}
    )
    response_json = response.json()
    return json.dumps(response_json)

@app.websocket("/check/ws")
async def is_occupied(websocket: WebSocket):
    await websocket.accept()
    while True:
        await asyncio.sleep(1)
        js = []

        for i in objects_id:
            for attr in attrs:
                response = requests.get(
                    subs_path + 'urn:ngsi-ld:Status:' + i + '/attrs/'+attr,
                    params=subs_params,
                    headers=subs_headers,
                )
                resp_value_len = len(response.json()['value'])
                if (resp_value_len>0):
                    attrValue = response.json()['value'][resp_value_len-1]['attrValue']

                    requests.delete(delete_subs_path+ '/urn:ngsi-ld:Status:' + i + '/attributes/' + attr, 
                    headers=subs_headers)

                    js.append({'id': i, 'attr': attr, "value": attrValue})

        if len(js)>0:
            await websocket.send_json(js)