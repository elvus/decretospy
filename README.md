# decretospy
```
$ pip install -r requirements.txt
```
```
$ FLASK_APP=decretosapp.py flask run
```
- Go to http://127.0.0.1:5000/api/v1/

# API

La API se encuentra alojada en https://decretos.datospy.org

# Ejemplo de uso con Javascript
```js
fetch('https://decretos.datospy.org/api/all')
  .then(response => response.json())
  .then(data => console.log(data));
```
**Repuesta**
```json
[
  {
    "_id": {"$oid": "5fb5af6b906562ff85035450"}, 
    "decreeId": "39404", 
    "nro": "4.289", 
    "fecha": "2/11/2020", 
    "descripcion": "2/11/2020: Por El Cual Se Rectifica El Decreto N\u00b0 6952 De Fecha 7 De Septiembre De 1990.", 
    "link": "https://www.presidencia.gov.py/archivos/documentos/DECRETO4289_u0ogzhkn.pdf", 
    "tweet": true
  }
  ...
]
```
# Ejemplo de uso con Filtros
```js
fetch('https://decretos.datospy.org/api/Se Rectifica El Decreto N° 6952')
  .then(response => response.json())
  .then(data => console.log(data));
```
**Repuesta**
```json
[
  {
    "_id": {"$oid": "5fb5af6b906562ff85035450"}, 
    "decreeId": "39404", 
    "nro": "4.289", 
    "fecha": "2/11/2020", 
    "descripcion": "2/11/2020: Por El Cual Se Rectifica El Decreto N\u00b0 6952 De Fecha 7 De Septiembre De 1990.", 
    "link": "https://www.presidencia.gov.py/archivos/documentos/DECRETO4289_u0ogzhkn.pdf", 
    "tweet": true
  }
]
```

