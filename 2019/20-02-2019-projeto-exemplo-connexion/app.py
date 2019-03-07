from flask import Flask, jsonify, request
import connexion
#from flasgger import Swagger
from datetime import date, datetime


PESSOAS = [
  {"id": 1,
   "nome": "Algrorn",
   "nascimento": date(1980, 3, 20)},
  {"id": 2,
   "nome": "Teath",
   "nascimento": date(1320, 10, 18)},
  {"id": 3,
   "nome": "Kros",
   "nascimento": date(1995, 6, 12)}
]


#app = Flask(__name__)
#swagger = Swagger(app)

#@app.route('/pessoas', methods=['GET'])
def pessoas():
  """Lista de pessoas
  ---
  parameters:
    - name: nome
      in: query
      type: string
      description: Filtro por parte do nome.
  responses:
    200:
      description: Lista de pessoas.
      schema:
        type: string
        example:
          Exemplo.
  """
  nome = request.args.get('nome', None)
  if nome is not None:
    nome = nome.lower()
    resultado = list(filter(lambda x: nome in x["nome"].lower(), PESSOAS))
  else:
    resultado = PESSOAS
  return jsonify({"pessoasssss": resultado})



#@app.route('/pessoas/<int:pk>')
def pessoa(pk):
  try:
    pessoa = next(x for x in PESSOAS if x["id"] == pk)
    return jsonify(pessoa)
  except StopIteration:
    return 'Not Found', 404


#@app.route('/pessoas', methods=['POST'])
def nova_pessoa():
  entrada = request.get_json()
  if entrada is None or "nome" not in entrada or "nascimento" not in entrada:
    return 'Bad request.', 400
  PESSOAS.append({
    "id": max(x["id"] for x in PESSOAS) + 1,
    "nome": entrada["nome"],
    "nascimento": datetime.strptime(entrada["nascimento"], '%d/%m/%Y')
  })
  return 'Created.', 201


app = connexion.App(__name__, specification_dir='static/')
app.add_api('openapi.yml', validate_responses=True)
app.run(port=5000, debug=True)
