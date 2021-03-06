# -*- coding: utf-8 -*-

import codecs
import sys
import re
from gerarLista import gera_lista
import nltk
from normalizar_Colecao import *



#start getfeatureVector
def getFeatureVector(msg):
    stopWords = carregar_stopWords()
    featureVector = []
    words = process1_msg(msg)
    for ww in words:
        w = process2_msg(ww)
        val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", w)
        if(w in stopWords or val is None):
            continue
        else:
            w_lema = lematizar(w)
            if( w_lema not in featureVector):
                featureVector.append(w_lema)
    return featureVector
#end

# All words features
def getAllFeatures(msg,lista_features):
    stopWords=carregar_stopWords()
    words = process1_msg(msg)
    for ww in words:
        w = process2_msg(ww)
        val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", w)
        if(w in stopWords or val is None):
            continue
        else:
            w_lema = lematizar(w)
            if( w_lema not in lista_features):
                lista_features.append(w_lema)
    return lista_features
#end
    
# Funcao une todas palavras do tweet para contar a frequencia
def get_words_in_tweets(tweets):
    all_words = []
    for w in tweets:
        if (w != 'negativo' and w != 'positivo'):
            all_words.append(w)
    return all_words


# Funcao identifica os termos mais frequentes
def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    return (wordlist)

    
    
