# -*- coding: utf-8 -*-

import sys
from gerarLista import gera_lista

from nltk.classify.util import apply_features
import subprocess
from getFeaturesVector import *

from normalizar_Colecao import *
from nltk import wordpunct_tokenize
from nltk.corpus import stopwords
from normalizar_Colecao import carregar_stopWords

#######################################################################################################

featureList=[]
msg_input=[]
lista_msg=[]
message=[]
lista_feature_fell=[]

#######################################################################################################

def extract_features(message):
    ##print("\n\ttestarMsg")
    lista_msg=message
    features={}
    ##print("\n\tLista_msg: %s "%lista_msg)
    ##print("\n\tFeatureList: %s "%featureList)
    for word in featureList:
        features['contains(%s)' %word] = (word in lista_msg)
    return features

#######################################################################################################

# Gerar lista de caracteristicas de cada colecao: Fatec, Dilma, Copa e Palmeiras
def gera_lista_features(tema):      
    #all_features=[]
    features=[]
    listaColecao = tema
    i=1
    y=0
    listaMsg=[]
    listaFell=[]
    # Chamando gera_lista 
    lista=gera_lista(listaColecao)
    #Separa a mensagem e o sentimento
    for x in lista:
        if(i%2 == 1):
            listaMsg.append(x)
            #print("Mensagem - %s "%x)
        else:
            listaFell.append(x)
            #print ("Sentimento - %s "%x)
        i+=1
    while ( y < len(listaMsg)):    
        features = getAllFeatures(listaMsg[y],features) # Todas palavras relevantes/caracteristicas da mensagem
        featureVector = getFeatureVector(listaMsg[y])
        lista_feature_fell.append((featureVector,listaFell[y]))
        y+=1
    return features

#######################################################################################################

def get_lista_feature_fell():
    return lista_feature_fell

#######################################################################################################

def get_feature_list():
    return featureList

#######################################################################################################

def avaliar_Sentimento(message,training):
    #print ("\n\tMensagem")
    #print(message)
    training_set = training
    #print ("\n\tTraining_set -> %s\n"%training)
    classifier= nltk.NaiveBayesClassifier.train(training_set)
    #print(classifier.show_most_informative_features(300))
    print ("\n\tSentimento Provavel: %s \n"%(classifier.classify(extract_features(message))))
    return (classifier.classify(extract_features(message)))

#######################################################################################################

def obter_sentimento_associado(listamsg,features):
    relacao=[]
    controle=[]       
    for w in features: # features encontradas na msg Exemplo:[u'mass', 'legal']
        achado='false'
        count=0
        for s in listamsg: # features e classificacao Exemplo: ([u'cert', u'prox', u'not', u'melhor'], u'positivo')
            count=count+1    
            for x in s[0]:                
                #print("Count: %s "%count)
                #print("Termo1: %s Termo2: %s "%(w,x))
                if (w == x and w not in controle):
                    #print("n\t\tAchado: %s igual %s "%(w,x))
                    relacao.append((w,s[1]))
                    controle.append(w)
                    achado = 'true'
                #print ("Achado: %s Count: %d "%(achado,count))
                if (count == len(listamsg) and achado != 'true'):
                    #print("Termo desconhecido: %s "%w)
                    count=0
                    relacao.append((w,'Termo Desconhecido'))
    return relacao

def show_relacao(relacao):
    count=0
    valido=''
    for i in relacao:
       if (i[1] == 'Termo Desconhecido'):
           print(bcolors.FAIL+"\n\t%s: Termo Desconhecido"%(i[0])+bcolors.ENDC)
           count=count+1   

       if (i[1] == 'positivo'):
           print(bcolors.OKBLUE+"\n\t%s: %s "%(i[0],i[1])+bcolors.ENDC)
       if (i[1] == 'negativo'):
           print(bcolors.OKGREEN+"\n\t%s: %s "%(i[0],i[1])+bcolors.ENDC)
       
       if(count == len(relacao)):
           valido='false'
       else:
           valido='true'
    return valido
 

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''

      

#######################################################################################################

         
def _calculate_languages_ratios(text):
    """
    Calculate probability of given text to be written in several languages and
    return a dictionary that looks like {'french': 2, 'spanish': 4, 'english': 0}
    
    @param text: Text whose language want to be detected
    @type text: str
    
    @return: Dictionary with languages and unique stopwords seen in analyzed text
    @rtype: dict
    """

    languages_ratios = {}

    '''
    nltk.wordpunct_tokenize() splits all punctuations into separate tokens
    
    >>> wordpunct_tokenize("That's thirty minutes away. I'll be there in ten.")
    ['That', "'", 's', 'thirty', 'minutes', 'away', '.', 'I', "'", 'll', 'be', 'there', 'in', 'ten', '.']
    '''

    tokens = wordpunct_tokenize(text)
    words = [word.lower() for word in tokens]

    # Compute per language included in nltk number of unique stopwords appearing in analyzed text
    for language in stopwords.fileids():
        stopwords_set = set(stopwords.words(language))
        ##print ("\n\nStopwords_set: %s \n\n" %stopwords_set)
        if (language == 'portuguese'):
           port_Stop = carregar_stopWords()
           stopwords_set = set(port_Stop)
         #  #print ("\n\nStopwords_set portuguese: %s \n\n" %stopwords_set)
        words_set = set(words)
        common_elements = words_set.intersection(stopwords_set)
        languages_ratios[language] = len(common_elements) # language "score"

    return languages_ratios



def detect_language(text):
    """
    Calculate probability of given text to be written in several languages and
    return the highest scored.It uses a stopwords based approach, counting how many unique stopwords
    are seen in analyzed text.@param text: Text whose language want to be detected
    @type text: str
    @return: Most scored language guessed
    @rtype: str
    """

    ratios = _calculate_languages_ratios(text)

    most_rated_language = max(ratios, key=ratios.get)

    return most_rated_language
    
######################################################################

def freq_words(lista_features_fell, most_freq_words):
    most_freq=[]
    for w in most_freq_words:
        for x in lista_features_fell:
            if w in str(x):
                most_freq.append(x)
    return most_freq


if __name__ == '__main__':
    if (len(sys.argv) == 3 and (sys.argv[1] != '') and (sys.argv[2] == 'fatec' or sys.argv[2] == 'dilma' or sys.argv[2] == 'copa' or sys.argv[2] == 'palmeiras')):
        # Limpar a tela
        #subprocess.call("clear")
        listaColecao = sys.argv[2]
        print (bcolors.OKBLUE+"\n\t\tAnálise de Sentimento\n\t\tAssunto: %s "%listaColecao.upper()+bcolors.ENDC)
        # Gera a lista de caracteristicas usada no metodo extract_features
        ##print("\n\tFeatureList: %s "%featureList)
        featureList = gera_lista_features(listaColecao)
        #print ("\n\tCaracteristicas conhecidas:\n\t%s "%(featureList))

        #print (bcolors.FAIL + "Warning: No active frommets remain. Continue?" 
      #+ bcolors.ENDC)

        lista_feature_fell = get_lista_feature_fell()
        #print("\n\tCaracteristica / Sentimento:\n\t %s"%lista_feature_fell)
        tema = listaColecao
        msg=sys.argv[1]
        language = detect_language(msg)
        ##print ("\n\tLingua: %s "%language)        
        #if ( language == 'portuguese'):
        print("\n\tAnalisar Msg: %s "%msg.capitalize())
        msg2 = normalizar(msg)
        #print("\n\tNormalizado: %s "%msg2)
        features_msg=getFeatureVector(msg2)
        most_freq_words = get_word_features(featureList)
        #print ("\n\tMost freq words- %s "%most_freq_words)
        lista_feature_fell_freq = freq_words(lista_feature_fell,most_freq_words)
        #print ("\n\tLista features / fell +freq - %s "%lista_feature_fell_freq)
        print ("\n\tCaracteristicas da Msg - %s "%features_msg)
        
        relacao = obter_sentimento_associado(lista_feature_fell_freq,features_msg)
        valor = show_relacao(relacao)
        if(valor == 'true'):
            training_set = apply_features(extract_features,lista_feature_fell_freq)
            #print("\n\tTraining_set:  %s "%training_set)
            # Avalia mensagem
            avaliar_Sentimento(features_msg,training_set)
        else:
            print(bcolors.FAIL+"\n\tAvaliação Impossível\n\n"+bcolors.ENDC)
            
        #else:
        #    print ("\n\tPor favor insira o texto novamente\n\n")
    else:
        print ('\nUsage: python testarMsg.py msg fatec|dilma|copa|palmeiras\n')
