import pandas as pd
import re
import time
from contextlib import redirect_stdout
from customtkinter import filedialog
import customtkinter as ctk
from contextlib import redirect_stdout
from playwright.sync_api import Playwright, sync_playwright, expect

#criando nova tabela para consulta


cnpj_regex = r"^\d{14}$"
#cnpj_regex = r"\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}"
processo_regex = r"\d+\.\s+(EXECUÇÃO FISCAL|EXECUÇÃO DE TÍTULO EXTRAJUDICIAL|Cumprimento de Sentença contra a Fazenda Pública|CUMPRIMENTO DE SENTENÇA|MANDADO DE SEGURANÇA|PROCEDIMENTO COMUM) - \d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}"


def trf():
    xlsxfile = ctk.filedialog.askopenfile()
    file_path = xlsxfile.name
    file_path_raw = r"{}".format(file_path)
    save_path = ctk.filedialog.asksaveasfilename(defaultextension=".csv")
    df = pd.read_excel(file_path_raw,dtype={"CNPJ":"string"})
    df.columns=['CNPJ']
    CNPJ = df['CNPJ']
    print(CNPJ)
    x = 0
    

    
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://consulta.trf4.jus.br/trf4/controlador.php?acao=consulta_processual_pesquisa")
        for x in range(0, len(CNPJ[x])):
            processo_matches = []
            tipo_matches = []
            data = []
            
            page.locator("#selFormaI").select_option("CP")
            time.sleep(0.3)
            page.locator("#txtValorI").click()
            page.locator("#txtValorI").fill(CNPJ[x])
            time.sleep(0.3)
            page.locator("#selOrigemI").select_option("SC")
            page.get_by_role("button", name="Pesquisar").click()
            time.sleep(0.3)
            
            if page.locator("#lblInfraCaptcha").is_visible():
                time.sleep(10)
            
            if page.on("dialog", lambda dialog: dialog.accept()):
                #page.on("dialog", lambda dialog: dialog.dismiss())
                
                print(CNPJ[x], "Sem Processo trf4")
                page.locator("#txtValorI").fill("")
                time.sleep(0.3)
                page.locator("#txtValorI").fill(CNPJ[x])
                page.get_by_role("button", name="Pesquisar").click()
                time.sleep(0.4)
                
            if page.get_by_text("Consulta Processual Unificada - Resultado da PesquisaATENÇÃO!1. A consulta proce").is_visible():
                time.sleep(0.5)
                print(CNPJ[x])
                text = page.get_by_text("Consulta Processual Unificada - Resultado da PesquisaATENÇÃO!1. A consulta proce").inner_text()
                processo_matches.extend(re.findall(r"\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}", text))
                tipo_matches.extend(re.findall(r"(EXECUÇÃO FISCAL|EXECUÇÃO DE TÍTULO EXTRAJUDICIAL|Cumprimento de Sentença contra a Fazenda Pública|CUMPRIMENTO DE SENTENÇA|MANDADO DE SEGURANÇA|PROCEDIMENTO COMUM)", text))
                
                for processo, tipo in zip(processo_matches, tipo_matches):
                    data.append({"Processo": processo, "Tipo": tipo, "CNPJ": CNPJ[x]})
                
                page.get_by_role("link", name="Nova Consulta").click()
        
        # Convert the matches to a dataframe
        df_result = pd.DataFrame(data)
        print(df_result)
        df_result.to_csv(save_path, index=False)

        context.close()
        browser.close()

if __name__ == "__main__":
    trf()
