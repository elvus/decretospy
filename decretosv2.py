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

def obtener_decretos(url):
    decretos = []
    try:
        soup=BeautifulSoup(
            requests.get(url, timeout=10,
            headers={'user-agent': 'Mozilla/5.0'}, verify=False).text, "html.parser")     
        tbody = soup.find('tbody')
        for tr in tbody.findAll('tr'):
            td = tr.findAll('td')
            decreeId = [d for d in td[len(td)-1].a.get('href') if d.isdigit()]
            decretos.append({
                "decreeId": ''.join(decreeId),
                "nro": tr.find('th').text,
                "fecha": td[0].text,
                "descripcion": td[0].text+": "+td[1].text.title().strip(),
                "link": td[2].a.get('href'),
                "tweet": False
            })

        return decretos
    except requests.ConnectionError:
        print("error al conectar")
    except Exception as e:
        print(e)

def decretos():
    decretos = []
    url = "https://www.presidencia.gov.py/url-sistema-visor-decretos/index.php/decretos/"
    while len(decretos)<50:
        try:
            decretos.extend(obtener_decretos(url))
            soup=BeautifulSoup(
                requests.get(url, timeout=10,
                headers={'user-agent': 'Mozilla/5.0'}, verify=False).text, "html.parser")     
            tags = soup.find("ul")
            url = tags.find("a", {'rel':'next'}).get('href')
        except requests.ConnectionError:
            print("error al conectar")
        except Exception as e:
            print(e)

    return decretos

def write_output():
    db=connection()
    sorted_list = sorted(decretos(), key=lambda i: datetime.strptime(i['fecha'], '%d/%m/%Y'))
    for i in sorted_list:
        try:
            db.decretos.insert_one(i)
            db.decretos.create_index("decreeId", unique=True)
        except pymongo.errors.DuplicateKeyError:
            if db.decretos.count_documents({ 'decreeId':i['decreeId'], 'descripcion':i['descripcion'], 'link':i['link']}) == 0:
                db.decretos.update_one({'decreeId':i['decreeId']},
                    {'$set':{'descripcion':i['descripcion'], 'link':i['link'], 'fecha_modificacion':datetime.now(),'tweet':False}})
            else:
                pass
        except BulkWriteError as bwe:
            pass