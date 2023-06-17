#import ScrapeEprocFuncional
import pandas as pd
from playwright.sync_api import Playwright, sync_playwright, expect
import customtkinter
from customtkinter import filedialog
from PIL import Image, ImageTk
from Eproc import run_eproc_scraping
from AssertivaPlayW import Assertiva
from GoogleAgenda import google
from LimpezaAgenda import limparlista
from FMI import Villela
from trf5 import trf

app = customtkinter.CTk()
app.geometry("500x780")
app.title("Scraper")

bg_image_label = customtkinter.CTkImage(Image.open(r"C:\Users\phili\Downloads\Rectangle.png"),size=(500, 780))
image_label = customtkinter.CTkLabel(app,image=bg_image_label)
image_label.place(x=0,y=0)
def run_agenda():
    google()

def run_ScrapeEproc():
    run_eproc_scraping()

def run_assertiva():
    Assertiva()

def run_limpar():
    limparlista()

def run_villela():
    Villela()

def run_trf():
    trf()



tabview = customtkinter.CTkTabview(app,width=500,height=100,bg_color="transparent")
tabview.pack()

tabview.add("Assertiva")
tabview.tab("Assertiva").grid_columnconfigure(0,weight=1)

tabview.add("Agenda")
tabview.tab("Agenda").grid_columnconfigure(0,weight=1)

tabview.add("Eproc")
tabview.tab("Eproc").grid_columnconfigure(0,weight=1)

tabview.add("Limpar Lista")
tabview.tab("Limpar Lista").grid_columnconfigure(0,weight=1)

tabview.add("TRF")
tabview.tab("TRF").grid_columnconfigure(0,weight=1)

tabview.add("Villela")
tabview.tab("Villela").grid_rowconfigure(2,weight=1)



buttoneproc = customtkinter.CTkButton(tabview.tab("Eproc"), text="Eproc",
                                command=run_ScrapeEproc,
                                width=175,
                                height=50,text_color="white",fg_color="#18034d").place(x=160,y=0)

buttonassertiva = customtkinter.CTkButton(tabview.tab("Assertiva"),text= "Assertiva",
                                          command= run_assertiva,
                                          width=175,
                                          height=50,text_color="white",fg_color="#18034d").place(x=160,y=0)

buttonagenda = customtkinter.CTkButton(tabview.tab("Agenda"),text="Passar agenda",
                                    command=run_agenda,
                                    width=175,
                                    height=50,text_color="white",fg_color="#18034d").place(x=160,y=0)

buttonlimpar = customtkinter.CTkButton(tabview.tab("Limpar Lista"),text="Limpar lista CNPJ",
                                       command= run_limpar,
                                       width=175,
                                       height=50,text_color="white",fg_color="#18034d").place(x=160)

buttonvillela = customtkinter.CTkButton(tabview.tab("Villela"),text="Vilella",
                                       command= run_villela,
                                       width=175,
                                       height=50,text_color="white",fg_color="#18034d").place(x=160)

buttontrf = customtkinter.CTkButton(tabview.tab("TRF"),text="TRF4",
                                       command= run_villela,
                                       width=175,
                                       height=50,text_color="white",fg_color="#18034d").place(x=160)


app.mainloop()

