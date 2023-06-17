import pandas as pd
import re
import time
from itertools import zip_longest
import os
from contextlib import redirect_stdout
from playwright.sync_api import Playwright, sync_playwright, expect
import customtkinter as ctk
from customtkinter import filedialog

def run_eproc_scraping():
    xlsxfile = ctk.filedialog.askopenfile()
    file_path = xlsxfile.name
    file_path_raw = r"{}".format(file_path)

    df = pd.read_excel(file_path_raw)
    df.columns = ['CNPJ']
    CNPJ = df['CNPJ']
    print(CNPJ)
    cnpj_regex = r"\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}"
    processo_regex = r"\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}"

    x = 0
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://eprocwebcon.tjsc.jus.br/consulta1g/externo_controlador.php?acao=processo_consulta_publica&acao_origem=processo_seleciona_publica&acao_retorno=processo_consulta_publica&hash=2b2fc99f2ca39e3e4a26a799e70e626f")
        page.get_by_text("Pessoa Jurídica").click()
        page.get_by_label("CNPJ:").click()
        page.get_by_label("CNPJ:").fill(CNPJ[x])
        captcha = page.locator("iframe[title=\"Widget contendo caixa de seleção para desafio de segurança hCaptcha\"]")
        
        # Create a DataFrame with the extracted data
        data = {"CNPJ": [], "Processo": [], "Text": []}
        for x in range(len(CNPJ)):
            if captcha.is_visible():
                print(CNPJ[x], "Captcha")
                time.sleep(15)
            else:
                page.get_by_text("Pessoa Jurídica").click()
                page.get_by_label("CNPJ:").click()
                page.get_by_label("CNPJ:").fill(CNPJ[x])
                page.get_by_label("CNPJ:").press("Enter")
                time.sleep(0.3)

            if page.locator("table").is_hidden():
                time.sleep(0.3)
                with open('semeproc.txt', 'a+', encoding='utf-8') as f:
                    with redirect_stdout(f):
                        print(CNPJ[x], "Sem Processo No EPROC")
                print(CNPJ[x], "Sem Processo No EPROC")

            else:
                time.sleep(0.2)
                text = page.locator("table").inner_text()
                processos = re.findall(processo_regex, text)
                noprocesso = re.findall(rf"{processo_regex}\s+(.*)", text)
                for processo, text in zip(processos, noprocesso):
                    data["CNPJ"].append(CNPJ[x])
                    data["Processo"].append(processo)
                    data["Text"].append(text)

        df_result = pd.DataFrame(data)
        print(df_result)

        # Ask the user for a file path to save the CSV file
        save_path = ctk.filedialog.asksaveasfilename(defaultextension=".xlsx")

        # Save the DataFrame to a CSV file
        df_result.to_csv(save_path, index=False)

        context.close()
        browser.close()

if __name__ == "__main__":
    run_eproc_scraping()
