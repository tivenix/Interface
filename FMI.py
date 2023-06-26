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
    save_path = filedialog.asksaveasfilename(defaultextension=".csv")
    CNPJ = df['CNPJ'].tolist()
    print(df)
    
    result_list = []
    x=0
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://portal-saas.aceleradorvillela.com/login")
        page.locator("input[type=\"text\"]").click()
        page.locator("input[type=\"text\"]").fill("felipe.machado@villelabrasil.com.br")
        page.locator("#login_password").click()
        page.locator("#login_password").fill("villela2022")
        page.get_by_role("button", name="ENTRAR").click()
        page.get_by_role("link", name="Consultas").click()
        time.sleep(0.9)

        for x in range(0,len(CNPJ)):
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
    
    result_df.to_csv(save_path, index=False, encoding='utf-8')

if __name__ == "__main__":
    Villela()
