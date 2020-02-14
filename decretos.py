import json
import pymongo
import re
import requests
import urllib3

from bs4 import BeautifulSoup
from datetime import datetime
from html.parser import HTMLParser
from pymongo import MongoClient

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def connection():
    client=MongoClient("mongodb://localhost:27017/")
    db=client["decretospy"]
    return db

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
                "decreeId":i['id'],
                "nro":i['cell'][0],
                "fecha":i['cell'][1],
                "descripcion":i['cell'][1]+": "+BeautifulSoup(i['cell'][2], 'html.parser').text.title().strip(),
                "link":urllib3.util.parse_url(BeautifulSoup(i['cell'][3], 'html.parser').a['href']).url,
                'tweet':False
            })
        return body
        
    except requests.ConnectionError:
        print("error al conectar")
    except Exception as e:
        print(e)   

def write_output():
    db=connection()
    sorted_list = sorted(decretos(), key=lambda i: i['decreeId'])
    for i in sorted_list:
        try:
            db.decretos.insert_one(i)
            db.decretos.create_index("decreeId", unique=True)
        except pymongo.errors.DuplicateKeyError:
            pass
    
    #print(list(db.decretos.find()))

write_output()