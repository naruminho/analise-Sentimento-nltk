#-*- coding: utf-8 -*-
import pygtk
pygtk.require("2.0")
import gtk
import subprocess

from nltk.classify.util import apply_features

from testarMsg import *
import pango
import config

featureList=[]

opcao=""

def extract_features(message):
    lista_msg=message
    features={}
    #print("\n\tFeatureList: %s "%(featureList))
    for word in featureList:
        features['contains(%s)' %word] = (word in lista_msg)
    return features

########################################################################################################

def avaliar_Sentimento(message,training):
    #print ("\n\tTraining: %s"%training)
    training_set = training
    #print ("\n\tTraining_set -> %s\n"%training)
    classifier= nltk.NaiveBayesClassifier.train(training_set)
    #print(classifier.show_most_informative_features(300))
    print ("\n\tSentimento Provavel: %s \n"%(classifier.classify(extract_features(message))))
    return (classifier.classify(extract_features(message)))

########################################################################################################

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
        #    print("Mensagem - %s "%x)
        else:
            listaFell.append(x)
        #    print ("Sentimento - %s "%x)
        i+=1
    while ( y < len(listaMsg)):    
        features = getAllFeatures(listaMsg[y],features) # Todas palavras relevantes/caracteristicas da mensagem
        featureVector = getFeatureVector(listaMsg[y])
        lista_feature_fell.append((featureVector,listaFell[y]))
        y+=1
    return features

########################################################################################################

def get_feature_list(opcao):
    return gera_lista_features(opcao)

########################################################################################################

def show_relacao(relacao):
    relacionado=[]
    nao_relacionado=[]
    for i in relacao:
       if (i[1] == 'Termo Desconhecido'):
           print(bcolors.FAIL+"\t%s: Termo Desconhecido"%(i[0])+bcolors.ENDC)
           #print (bcolors.FAIL + "Warning: No active frommets remain. Continue?" 
      #+ bcolors.ENDC)

       if (i[1] == 'positivo'):
           print(bcolors.OKBLUE+"\t%s: %s "%(i[0],i[1])+bcolors.ENDC)
       if (i[1] == 'negativo'):
           print(bcolors.OKGREEN+"\t%s: %s "%(i[0],i[1])+bcolors.ENDC)


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

########################################################################################################

class tgApp(object):
    def __init__(self):
        global opcao
        
        self.builder = gtk.Builder()
        self.builder.add_from_file("glade/tg.ok.glade")
        self.window = self.builder.get_object("window1")
        self.window.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#000000"))
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.set_size_request(800,600) # largura X altura
        self.vbox = self.builder.get_object("vbox1")
        self.image_fatec = self.builder.get_object("fatec")
        self.image_fatec.set_from_file('glade/imgs/FATECSJC.png')
        self.image_fatec.show()

        self.image_tg = self.builder.get_object("image2")
        self.image_tg.set_from_file('glade/imgs/tg.png')
        self.image_tg.show()

        self.image_doubtLeft = self.builder.get_object("doubtLeft")
        self.image_doubtLeft.set_from_file('glade/imgs/duvidaL.png')
        self.image_doubtLeft.show()
        
        self.image_black = self.builder.get_object("black")
        self.image_black.set_from_file('glade/imgs/duvida.png')
        self.image_black.show()

        self.image_doubtRight = self.builder.get_object("doubtRight")
        self.image_doubtRight.set_from_file('glade/imgs/duvidaR.png')
        self.image_doubtRight.show()

        self.window.show()
        self.doubtLeft = self.builder.get_object("doubtLeft")
        self.black = self.builder.get_object("black")
        self.doubtRight = self.builder.get_object("doubtRight")
        self.text_area = self.builder.get_object("text_entry")
        self.text_area.modify_font(pango.FontDescription("monospace 16"))
        self.text_area2 = self.builder.get_object("text_entry2")
        self.text_area2.modify_font(pango.FontDescription("sans bold  12"))
        self.text_area2.modify_text(gtk.STATE_NORMAL, gtk.gdk.color_parse("#FF0000"))
        self.text_area2.set_text("Sentimento -->")
        
        self.opcao = ""
        self.fell = ""
        #print ("Opcao antes: %s "%self.opcao)
        self.builder.connect_signals({"gtk_main_quit": gtk.main_quit,
                            "on_button_analisar_clicked": self.analisar_frase,
                            "on_button_clear_clicked": self.clear_text,
                            "on_button_dilma_clicked": self.opcao_dilma,
                            "on_button_copa_clicked": self.opcao_copa,
                            "on_button_palmeiras_clicked": self.opcao_palmeiras,
                            "on_button_fatec_clicked": self.opcao_fatec,
                             })
    
    
    def analisar_frase(self, widget):
        """Função: analisar a frase que o usuário"""
        # Limpar a tela
        subprocess.call("clear")
        print ("\n\tAnalise")
        global featureList
        frase = self.text_area.get_text()
        if ( frase != ""):
            frase_proc= normalizar(frase)
            self.text_area.set_text(frase)
            if (self.opcao == 'dilma' or self.opcao == 'copa' or self.opcao == 'palmeiras' or self.opcao == 'fatec'):
                #print("Opcao depois: %s "%self.opcao)

              # Gera a lista de caracteristicas usada no metodo extract_features
                featureList = gera_lista_features(self.opcao)
                #print ("\n\tCaracteristicas conhecidas:\n\t%s "%(featureList))
                lista_feature_fell = get_lista_feature_fell()
                #print("\n\tCaracteristica / Sentimento:\n\t %s"%lista_feature_fell)

              #  features = get_feature_list(self.opcao)
              #  print("\n\tFeatureListtt: %s "%(features))
           
                frase = self.text_area.get_text()
                frase_Normal = normalizar(frase)
                features_msg = getFeatureVector(frase_Normal)

                print ("\n\tFrase analisada: %s "%frase)
                print ("\n\tCaracteristicas da Msg - %s\n "%features_msg)
                
                # Obter sentimentos associados
                show_relacao(obter_sentimento_associado(lista_feature_fell,features_msg))
                
                training_set = apply_features(extract_features,lista_feature_fell)
                self.fell = avaliar_Sentimento(features_msg,training_set)
                
                language = detect_language(frase)
                #print ("\n\tLingua: %s "%language)        
                if ( language == 'portuguese'):
                    #print ("\n\tSentimento: %s "%self.fell)
                    # text color
                    self.text_area.modify_text(gtk.STATE_NORMAL, gtk.gdk.color_parse("#FF0000"))
                    self.text_area2.modify_text(gtk.STATE_NORMAL, gtk.gdk.color_parse("#FF0000"))
                    # text font
                    # entry.modify_font(pango.FontDescription("monospace 16"))
                    self.text_area2.modify_font(pango.FontDescription("sans bold  16"))
                    if ( self.fell == 'negativo'):
                        frase = self.text_area.get_text()
                        self.text_area.set_text(frase)
                        self.text_area2.set_text("			 Sentimento: Negativo")
                        self.image_black.set_from_file('glade/imgs/cry.png')
                        self.image_black.show

                        self.image_doubtRight = self.builder.get_object("doubtRight")
                        self.image_doubtRight.set_from_file('glade/imgs/black.png')
                        self.image_doubtRight.show()
                        self.image_doubtLeft = self.builder.get_object("doubtLeft")
                        self.image_doubtLeft.set_from_file('glade/imgs/black.png')
                        self.image_doubtLeft.show()
                     
                    else:
                        self.text_area2.set_text("			 Sentimento: Positivo")
                        self.image_black.set_from_file('glade/imgs/happy.png')
                        self.image_black.show
                        
                        self.image_doubtRight = self.builder.get_object("doubtRight")
                        self.image_doubtRight.set_from_file('glade/imgs/black.png')
                        self.image_doubtRight.show()
                        self.image_doubtLeft = self.builder.get_object("doubtLeft")
                        self.image_doubtLeft.set_from_file('glade/imgs/black.png')
                        self.image_doubtLeft.show()
                        
                else:
                    self.text_area2.set_text(" Ce ta de Brincaxxon comigo ?????")     
                        
            
    def clear_text(self, widget):
        """Função: para apagar o texto na área de texto"""
        self.text_area.set_text("")
        self.text_area2.set_text("Sentimento -->")
        self.text_area.modify_text(gtk.STATE_NORMAL, gtk.gdk.color_parse("#000000"))
        self.image_black.set_from_file('glade/imgs/duvida.png')
        self.image_black.show()

        self.image_doubtRight = self.builder.get_object("doubtRight")
        self.image_doubtRight.set_from_file('glade/imgs/duvidaR.png')
        self.image_doubtRight.show()
        self.image_doubtLeft = self.builder.get_object("doubtLeft")
        self.image_doubtLeft.set_from_file('glade/imgs/duvidaL.png')
        self.image_doubtLeft.show()
        
        
    def opcao_dilma(self, widget):
        """Função: para definir a opcao Dilma"""
        self.opcao="dilma"
              
    def opcao_copa(self, widget):
        """Função: para definir a opcao Copa"""
        self.opcao="copa"

    def opcao_palmeiras(self, widget):
        """Função: para definir a opcao Palmeiras"""
        self.opcao="palmeiras"

    def opcao_fatec(self, widget):
        """Função: para definir a opcao Fatec"""
        self.opcao="fatec" 


        
if __name__ == "__main__":
    
    app = tgApp()
    gtk.main()
    
   
         
