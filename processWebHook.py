import os
import pickle
from flask import send_from_directory, Flask, render_template, request

app = Flask(__name__)

model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    result =''
    return render_template('index.html', **locals())
                               

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    total_errors = float(request.form['totalErrors'])
    algum_acerto = float(request.form['algumAcerto'])
    questoes_certas = float(request.form['questoesCertas'])
    acertos_100 = float(request.form['acertos_100'])
    submissoes = float(request.form['submissoes'] )
    questoes_tentadas = float(request.form['questoesTentadas'])
    subms_por_questao = float(submissoes/questoes_tentadas)
    tempo_lista = float(request.form['tempoLista'])
    perc_total_error = float(total_errors/submissoes)
    perc_algum_acerto = float(algum_acerto/submissoes)
    perc_acerto_100 = float(acertos_100/submissoes)

    desistente = model.predict([[total_errors, algum_acerto, questoes_certas, acertos_100, submissoes, subms_por_questao, tempo_lista, perc_total_error, perc_algum_acerto, perc_acerto_100]])[0]    
    if(desistente==0):
        desistente='Não'
    else:
        desistente ='Sim'
    result = desistente
    return render_template('index.html', **locals())

if __name__ == "__main__":
    app.secret_key = 'ItIsASecret'
    app.debug = True
    app.run()