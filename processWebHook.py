import os
import pickle
from flask import send_from_directory, Flask, render_template, request
import json

app = Flask(__name__)

model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    result =''
    return render_template('index.html', **locals())

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/favicon.png')                       

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    predict_data={}
    for d in request.args.keys():
        val=request.args.get(d)
        predict_data[d]=val
    total_errors = float(predict_data['totalErrors'])
    algum_acerto = float(predict_data['algumAcerto'])
    questoes_certas = float(predict_data['questoesCertas'])
    acertos_100 = float(predict_data['acertos_100'])
    submissoes = float(predict_data['submissoes'] )
    questoes_tentadas = float(predict_data['questoesTentadas'])
    subms_por_questao = float(submissoes/questoes_tentadas)
    tempo_lista = float(predict_data['tempoLista'])
    perc_total_error = float(total_errors/submissoes)
    perc_algum_acerto = float(algum_acerto/submissoes)
    perc_acerto_100 = float(acertos_100/submissoes)

    desistente = model.predict([[total_errors, algum_acerto, questoes_certas, acertos_100, submissoes, subms_por_questao, tempo_lista, perc_total_error, perc_algum_acerto, perc_acerto_100]])[0]    
    #if(desistente==0):
    #   desistente='Não'
    #else:
    #    desistente ='Sim'
    result = desistente

    json_return = json.dumps({'desistente': int(result)})
    return json_return

if __name__ == "__main__":
    app.secret_key = 'ItIsASecret'
    app.debug = True
    app.run()