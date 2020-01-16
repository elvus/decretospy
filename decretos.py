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
                "descripcion":HTMLParser().unescape(i['cell'][2]).replace(u'\xa0', u'').strip(),
                "link":re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', i['cell'][3])[0]
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