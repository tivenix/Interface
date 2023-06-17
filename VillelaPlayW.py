import pandas as pd
import time
from contextlib import redirect_stdout
from playwright.sync_api import Playwright, sync_playwright, expect
import customtkinter as ctk
from customtkinter import filedialog


def Villela():
    xlsxfile = ctk.filedialog.askopenfile()
    file_path = xlsxfile.name
    file_path_raw = r"{}".format(file_path)
    df = pd.read_excel(file_path_raw)
    df.columns=['CNPJ']
    df.drop_duplicates()
    CNPJ = df['CNPJ'] #criando nova tabela para consulta
    print(df)
    x= 0
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://portal.aceleradorvillela.com/auth/login")
        page.get_by_placeholder("E-mail").click()
        page.get_by_placeholder("E-mail").fill("felipe.machado@villelabrasil.com.br")
        page.get_by_placeholder("Password").click()
        page.get_by_placeholder("Password").fill("villela2022")
        page.get_by_placeholder("Password").press("Enter")
        page.get_by_role("link", name="Funil de Vendas").click()
        page.get_by_role("link", name="Consultas").click()
        time.sleep(0.9)
        for x in range(0,len(CNPJ)):
            page.get_by_placeholder("CNPJ da Empresa").click()
            page.get_by_placeholder("CNPJ da Empresa").fill(CNPJ[x])
            page.get_by_role("button").first.click()
            time.sleep(1)
            atenc = page.get_by_text("Atenção, cliente ativo na Villela Brasil.",exact=True)
            if atenc.is_visible():
                print(CNPJ[x],"Cliente")
                with open("E:\Script felipe\SC\Joinville\Joinville100k\Joinville100kVillela.txt",'a+',encoding='utf-8') as f:
                    with redirect_stdout(f):
                        print(CNPJ[x], "Cliente")
                time.sleep(1)            
            else:
                with open("E:\Script felipe\SC\Joinville\Joinville100k\Joinville100kVillela.txt",'a+',encoding='utf-8') as f:
                    with redirect_stdout(f):
                        print(CNPJ[x], "Não é Cliente")
        # ---------------------
        context.close()
        browser.close()


if __name__ == "__main__":
    Villela()
