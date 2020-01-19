import json
import requests
import urllib3
import re

from bs4 import BeautifulSoup
from datetime import datetime
from html.parser import HTMLParser

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def decretos():
    body=[]
    try:
        parameters={"page": 1,"rows": 50,"sord": "desc"	}
        soup=json.loads(
            requests.post(
                "https://www.presidencia.gov.py/tmpl/grillas/decretos.php", 
                data=parameters,
                timeout=5,
            ).text #trae los últimos 50 decretos
        )
        
        for i in soup['rows']:
            body.append({
                "id":i['id'],
                "nro":i['cell'][0],
                "fecha":i['cell'][1],
                "descripcion":BeautifulSoup(i['cell'][2], 'html.parser').text.strip(),
                "link":urllib3.util.parse_url(BeautifulSoup(i['cell'][3], 'html.parser').a['href']).url
            })
        
        return json.dumps(
            body,
            indent=4,
            sort_keys=True,
            separators=(",", ": "),
        )
    except requests.ConnectionError:
        print("error al conectar")
    except Exception as e:
        print(e)   

def get_output():
    with open("decretos.json","r") as f:
        response=f.read()
    return response

def write_output():
    response = decretos()
    with open("decretos.json", "w") as f:
        f.write(response)

write_output()