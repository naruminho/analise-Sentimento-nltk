#!/usr/bin/env python
#-*- coding: utf-8 -*-

import pygtk
pygtk.require("2.0")
import gtk
from funcoes/testarMsg import avaliar_Sentimento

class tgApp(object):
    def __init__(self):
        builder = gtk.Builder()
        builder.add_from_file("tg.glade")
        self.window = builder.get_object("window1")
        self.text_area = builder.get_object("text_entry")
        self.window.show()
        builder.connect_signals({"gtk_main_quit": gtk.main_quit,
                            "on_button_analisar_clicked": self.analisar_frase,
                            "on_text_entry_activate": self.analisar_frase,
                            "on_copy_activate": self.copy_text,
                            "on_paste_activate": self.paste_text,
                            "on_button_clear_clicked": self.clear_text,
                            "on_button_dilma_clicked": self.opcao_dilma,
                            "on_button_copa_clicked": self.opcao_copa,
                            "on_button_palmeiras_clicked": self.opcao_palmeiras,
                            "on_button_fatec_clicked": self.opcao_fatec,
                                })
                            
    def analisar_frase(self, widget):
        """Função Principal do programa, irá armazenar a frase que o usuário
        digitar na área de texto e inverte-la"""
        frase = self.text_area.get_text()
        frase = frase[::-1]
        print("Frase %s:"%frase)
        self.text_area.set_text(frase)
        
    def copy_text(self, widget):
        """Função para copiar o valor digitado na área de texto para o
        clipboard do sistema"""
        clipboard = gtk.clipboard_get()
        frase = self.text_area.get_text()
        clipboard.set_text(frase)
        clipboard.store()
        
    def paste_text(self, widget):
        """Função para colar o texto armazenado no clipboard na área de texto
        do programa"""
        clipboard = gtk.clipboard_get()
        frase = clipboard.wait_for_text()
        self.text_area.set_text(frase)
        
    def clear_text(self, widget):
        """Função para apagar qualquer texto que esteja inserido na
        área de texto"""
        self.text_area.set_text("Frase:")

    def opcao_dilma(self, widget):
        """Função para definir a opcao Dilma"""
        opcao="dilma"
        print ("Analisar: %s "%opcao)

    def opcao_copa(self, widget):
        """Função para definir a opcao Copa"""
        opcao="copa"
        print ("Analisar: %s "%opcao)

    def opcao_palmeiras(self, widget):
        """Função para definir a opcao Palmeiras"""
        opcao="palmeiras"
        print ("Analisar: %s "%opcao)

    def opcao_fatec(self, widget):
        """Função para definir a opcao Fatec"""
        opcao="fatec"
        print ("Analisar: %s "%opcao)
        
if __name__ == "__main__":
    app = tgApp()
    gtk.main()
         
