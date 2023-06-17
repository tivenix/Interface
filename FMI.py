import pandas as pd
import time
from playwright.sync_api import Playwright, sync_playwright
from customtkinter import filedialog

def Villela():
    # Use filedialog to select the xlsx file
    xlsxfile = filedialog.askopenfilename()
    df = pd.read_excel(xlsxfile)
    df.columns = ['CNPJ']
    df.drop_duplicates(inplace=True)
    CNPJ = df['CNPJ'].tolist()
    print(df)

    result_list = []
    x=0
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

        for x in range(0,10):
            page.get_by_placeholder("CNPJ da Empresa").click()
            page.get_by_placeholder("CNPJ da Empresa").fill(CNPJ[x])
            page.get_by_role("button").first.click()
            time.sleep(1)
            atenc = page.get_by_text("Atenção, cliente ativo na Villela Brasil.", exact=True)
            if atenc.is_visible():
                result_list.append([CNPJ[x], "Cliente"])
                time.sleep(1.2)
            else:
                result_list.append([CNPJ[x], "Não é Cliente"])

        context.close()
        browser.close()

    result_df = pd.DataFrame(result_list, columns=["CNPJ", "Clientes"])
    save_path = filedialog.asksaveasfilename(defaultextension=".xlsx")
    result_df.to_csv(save_path, index=False, encoding='utf-8')

if __name__ == "__main__":
    Villela()
