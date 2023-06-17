from playwright.sync_api import Playwright, sync_playwright, expect
import pandas as pd
import numpy as np
import time
from contextlib import redirect_stdout
from customtkinter import filedialog
import customtkinter as ctk

def Assertiva():
    xlsxfile = ctk.filedialog.askopenfile()
    file_path = xlsxfile.name
    file_path_raw = r"{}".format(file_path)
    save_path = ctk.filedialog.asksaveasfilename(defaultextension=".csv")
    df = pd.read_excel(file_path_raw)
    CNPJ = df.iloc[:, 0].tolist()
    print(CNPJ)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://painel.assertivasolucoes.com.br/login")
        page.get_by_label("E-mail *").click()
        page.get_by_label("E-mail *").fill("corretordepablo@gmail.com")
        page.get_by_label("Senha *").click()
        page.get_by_label("Senha *").fill("Fdp84053690.")
        page.get_by_label("Senha *").press("Enter")
        page.get_by_role("link", name="Assertiva Localize Assertiva Localize").click()
        page.get_by_role("button", name="Consultar CPF").click()
        page.get_by_role("option", name="Consultar CNPJ").click()
        page.get_by_role("button", name="Finalidade").click()
        page.get_by_text("Confirmação de identidade", exact=True).click()

        result_list = []

        for x in range(0, 3):
            page.get_by_placeholder("Digite o CNPJ").click()
            page.get_by_placeholder("Digite o CNPJ").fill(CNPJ[x])
            page.get_by_placeholder("Digite o CNPJ").press("Enter")
            time.sleep(1)
            # Wait for the element to become stale or for its text to change
            element = page.locator('//div[contains(text(), "CNPJ:")]')
            time.sleep(1)
            element_text = element.inner_text()
            print(element_text)
            result_list.append(element_text)

        df_result = pd.DataFrame({"Situacao": result_list})
        df_result.to_csv(save_path, index=False)

        browser.close()


if __name__ == "__main__":
    Assertiva()
