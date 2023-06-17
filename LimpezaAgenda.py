import pandas as pd
import customtkinter as ctk
from customtkinter import filedialog
    
def limparlista():
    xlsxfile = ctk.filedialog.askopenfile()

    file_path = xlsxfile.name
    file_path_raw = r"{}".format(file_path)
    # Ler as tabelas em duas listas
    lista = pd.read_excel(file_path_raw).values.tolist()
    agenda_list = pd.read_excel(r"E:\captcha\agenda.xlsx").values.tolist()

    # Remover linhas duplicadas em cada lista
    lista = [list(x) for x in set(tuple(x) for x in lista)]
    agenda_list = [list(x) for x in set(tuple(x) for x in agenda_list)]

    # Remover linhas que aparecem em ambas as tabelas
    unique_list = []
    for row in lista:
        if row not in agenda_list:
            unique_list.append(row)
 # Ask the user for a file path to save the CSV file
    save_path = ctk.filedialog.asksaveasfilename(defaultextension=".xlsx")
    # Criar DataFrame com as linhas únicas
    df_unique = pd.DataFrame(unique_list, columns=pd.read_excel(file_path_raw).columns)

    # Salvar as linhas únicas em um novo arquivo Excel
    df_unique.to_excel(save_path, index=False)


if __name__ == "__main__":
    limparlista()