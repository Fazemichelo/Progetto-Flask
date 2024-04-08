
from flask import Flask, render_template, url_for, redirect, request
import os
my_secret = os.environ['MongoDB']
from bson import ObjectId

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


uri ="mongodb+srv://michelegatti0407:"+my_secret+"@dripdb.468qvza.mongodb.net/?retryWrites=true&w=majority&appName=DripDB"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

app = Flask(__name__)

db = client.get_database('DripDB')
coll_scarpe = db['scarpe']
coll_vestiti = db['vestiti']



#home page - Restituisce la pagina principale renderizzata
@app.route("/")
def leggiDB():
  
  rows=list (coll_scarpe.find({}))
  rowsV = list(coll_vestiti.find({}))
  return render_template('indexSQL.html', DBtoHtml=rows, DBtoHtmlV=rowsV)



#Riceve dal template mediante metodo POST i dati da inserire
@app.route('/inserisci', methods=['POST'])
def inserisci():
  a = request.form.get('MarcaScarpa')
  b = request.form.get('ModelloScarpa')
  c = request.form.get('ColorwayScarpa')
  d = request.form.get('PrezzoRetail')
  coll_scarpe.insert_one({'marca':a, 'modello':b, 'colorway':c, 'prezzoRetail':d})
  return redirect(url_for('leggiDB'))

@app.route('/cancellaScarpa/<idscarpa>', methods=['POST'])
def cancellaScarpa(idscarpa):
  print (idscarpa)

  coll_scarpe.delete_one({"_id":ObjectId(idscarpa)})
  return redirect(url_for('leggiDB'))


@app.route('/ricerca')
def ricerca():
  marca_query = request.args.get('MarcaScarpaQ')
  modello_query = request.args.get('ModelloScarpaQ')
  colorway_query = request.args.get('ColorwayScarpaQ')
  prezzo_query = request.args.get('PrezzoRetailQ')

  non_null_query = {}
  if marca_query:
        non_null_query['marca'] = marca_query
  if modello_query:
        non_null_query['modello'] = modello_query
  if colorway_query:
        non_null_query['colorway'] = colorway_query
  if prezzo_query:
        non_null_query['prezzoRetail'] = prezzo_query

  rows = list(coll_scarpe.find(non_null_query))
  
  return render_template('query.html', QueryToHtml = rows )

@app.route('/inserisciV', methods=['POST'])
def inserisciV():
  a = request.form.get('MarcaVestito')
  b = request.form.get('ModelloVestito')
  c = request.form.get('ColoreVestito')
  d = request.form.get('PrezzoRetail')
  coll_vestiti.insert_one({'marca':a, 'modello':b, 'colorway':c, 'prezzoRetail':d})
  return redirect(url_for('leggiDB'))

@app.route('/cancellaVestito/<idvestito>', methods=['POST'])
def cancellaVestito(idvestito):
  print (idvestito)
  coll_vestiti.delete_one({"_id":ObjectId(idvestito)})
  return redirect(url_for('leggiDB'))

@app.route('/ricercaVestito')
def ricercaVestito():
  marca_query = request.args.get('MarcaVestitoQ')
  modello_query = request.args.get('ModelloVestitoQ')
  colorway_query = request.args.get('ColoreVestitoQ')
  prezzo_query = request.args.get('PrezzoRetailVestitoQ')

  non_null_query = {}
  if marca_query:
        non_null_query['marca'] = marca_query
  if modello_query:
        non_null_query['modello'] = modello_query
  if colorway_query:
        non_null_query['colorway'] = colorway_query
  if prezzo_query:
        non_null_query['prezzoRetail'] = prezzo_query

  rows = list(coll_vestiti.find(non_null_query))

  return render_template('query.html', QueryToHtmlV = rows )

if __name__ == "__main__":
 app.run(host='0.0.0.0', port=8080)