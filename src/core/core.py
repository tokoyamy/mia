import spacy
from spacy.lang.pt.stop_words import STOP_WORDS
import string


class Aiko:
    def preprocessing(texto):
        pln = spacy.load('pt')
        stop_words = STOP_WORDS
        pontuacoes = string.punctuation
        texto = texto.lower()
        documento = pln(texto)

        lista = []
        for token in documento:
            # lista.append(token.text)
            lista.append(token.lemma_)
        lista = [palavra for palavra in lista if palavra not in stop_words and palavra not in pontuacoes]
        lista = ' '.join([str(elemento) for elemento in lista if not elemento.isdigit()])
        return lista
