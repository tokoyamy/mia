import spacy
import pandas as pd
import string
import spacy
import random
import numpy as np
from src.core.core import *


if __name__ == "__main__":
    base_dados = pd.read_csv('/src/database/base_treinamento.txt', encoding='utf-8')

    exemplo_base_dados = [["este trabalho é agradável", {"ALEGRIA": True, "MEDO": False}],
                          ["este lugar continua assustador", {"ALEGRIA": False, "MEDO": True}]]

    base_dados_final = []
    for texto, emocao in zip(base_dados['texto'], base_dados['emocao']):
        # print(texto, emocao)
        if emocao == 'alegria':
            dic = ({'ALEGRIA': True, 'MEDO': False})
        elif emocao == 'medo':
            dic = ({'ALEGRIA': False, 'MEDO': True})

        base_dados_final.append([texto, dic.copy()])

    modelo = spacy.blank('pt')
    categorias = modelo.create_pipe("textcat")
    categorias.add_label("ALEGRIA")
    categorias.add_label("MEDO")
    modelo.add_pipe(categorias)
    historico = []

    modelo.begin_training()
    for epoca in range(1000):
        random.shuffle(base_dados_final)
        losses = {}
        for batch in spacy.util.minibatch(base_dados_final, 30):
            textos = [modelo(texto) for texto, entities in batch]
            annotations = [{'cats': entities} for texto, entities in batch]
            modelo.update(textos, annotations, losses=losses)
        if epoca % 100 == 0:
            print(losses)
            historico.append(losses)

    historico_loss = []
    for i in historico:
        historico_loss.append(i.get('textcat'))

    historico_loss = np.array(historico_loss)
    print(historico_loss)

    modelo.to_disk("src/model/modelo")

    modelo_carregado = spacy.load("modelo")

    texto_positivo = 'eu adoro cor dos seus olhos'

    texto_positivo = Aiko.preprocessing(texto_positivo)
    print(texto_positivo)

    previsao = modelo_carregado(texto_positivo)
    print(previsao)

    print(previsao.cats)

    texto_negativo = 'estou com medo dele'
    previsao = modelo_carregado(Aiko.preprocessing(texto_negativo))
    print(previsao.cats)
