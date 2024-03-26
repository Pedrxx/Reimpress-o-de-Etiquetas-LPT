import tkinter as tk
from tkinter import ttk
import subprocess
import tempfile
import os
from datetime import datetime


def gravar_log_impressao(texto):
    # Obtém a data e hora atuais
    agora = datetime.now()
    # Formata a data e hora no formato desejado (por exemplo, "dd/mm/YYYY H:M:S")
    data_hora_formatada = agora.strftime("%d/%m/%Y %H:%M:%S")
    # Cria a string final adicionando a data e hora atual ao texto fornecido
    string_final = f"[{data_hora_formatada}] : {texto}"
    # Abre (ou cria, se não existir) o arquivo em modo de escrita
    with open("c:/temp/log_imp_etiq.txt", "w") as arquivo:
        # Grava a string final no arquivo
        arquivo.write(string_final)


def envia_impressao(cod_eti,lote,peso,data,tambor):
    # Sua string ZPL
    zpl_string = """
    CT~~CD,~CC^~CT~
    ^XA
    ~TA000
    ~JSN
    ^LT0
    ^MNW
    ^MTT
    ^PON
    ^PMN
    ^LH0,0
    ^JMA
    ^PR4,4
    ~SD22
    ^JUS
    ^LRN
    ^CI27
    ^PA0,1,1,0
    ^XZ
    ^XA
    ^MMT
    ^PW799
    ^LL1359
    ^LS0
    ^FO607,32^GFA,2425,6768,24,:Z64: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:2572
    ^FT607,1335^BQN,2,8
    ^FH\^FDLA,{}^FS
    ^BY5,3,88^FT56,384^BCR,,N,N
    ^FH\^FD>:{}^FS
    ^FT722,504^A0R,37,38^FH\^CI28^FDAGROPRATINHA S/A^FS^CI27
    ^FT666,400^A0R,37,38^FH\^CI28^FDPARANAVAI - PARANA - BRAZIL^FS^CI27
    ^FT610,31^A0R,37,48^FB1328,1,9,C^FH\^CI28^FDFROZEN CONCENTRATED ORANGE JUICE^FS^CI27
    ^FT522,56^A0R,37,38^FH\^CI28^FDTICKET^FS^CI27
    ^FT458,56^A0R,37,38^FH\^CI28^FDBATCH^FS^CI27
    ^FT394,56^A0R,37,38^FH\^CI28^FDNET WT^FS^CI27
    ^FT330,56^A0R,37,38^FH\^CI28^FDPRODUCTION DATE^FS^CI27
    ^FT266,56^A0R,37,38^FH\^CI28^FDVALIDTY^FS^CI27
    ^FT203,56^A0R,37,38^FH\^CI28^FDDRUM^FS^CI27
    ^FT522,0^A0R,37,38^FB1314,1,9,R^FH\^CI28^FD{}^FS^CI27
    ^FT458,0^A0R,37,38^FB1309,1,9,R^FH\^CI28^FD{}^FS^CI27
    ^FT394,0^A0R,37,38^FB1306,1,9,R^FH\^CI28^FD{}^FS^CI27
    ^FT330,0^A0R,37,38^FB1302,1,9,R^FH\^CI28^FD{}^FS^CI27
    ^FT266,0^A0R,37,38^FB1300,1,9,R^FH\^CI28^FD2 YEARS^FS^CI27
    ^FT203,0^A0R,37,38^FB1304,1,9,R^FH\^CI28^FD{}^FS^CI27
    ^PQ1,0,1,Y
    ^XZ

    """.format(cod_eti,cod_eti,cod_eti,lote,peso,data,tambor)

    # zpl_string.replace("%CODETI%",cod_eti)
    # zpl_string.replace("%LOTE%",lote)
    # zpl_string.replace("%PESO%",peso)
    # zpl_string.replace("%DTNASC%",data)
    # zpl_string.replace("%CODETI%",validade)
    # zpl_string.replace("%TAMBOR%",tambor)

    # Cria um arquivo temporário
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        caminho_arquivo_temp = temp_file.name
        # Escreve a string ZPL para o arquivo temporário
        temp_file.write(zpl_string.encode('utf-8'))
        temp_file.close()  # Fecha o arquivo para garantir que ele seja salvo antes de enviar

    # Comando para enviar o arquivo para a porta LPT1
    comando = f'COPY /B "{caminho_arquivo_temp}" LPT1'

    # Executar o comando
    try:
        subprocess.run(comando, check=True, shell=True)
        # print("Dados enviados para a porta LPT1 com sucesso.")
        gravar_log_impressao("Dados enviados para a porta LPT1 com sucesso.")
    except subprocess.CalledProcessError:
        # print("Falha ao enviar dados para a porta LPT1.")
        gravar_log_impressao("Falha ao enviar dados para a porta LPT1.")

    # Limpa o arquivo temporário
    os.remove(caminho_arquivo_temp)

# Função chamada quando o botão "Validar" é pressionado
def validar():
    etiqueta = entry_etiqueta.get()
    data_producao = entry_data_producao.get()
    lote = entry_lote.get()
    peso = entry_peso.get()
    tambor = entry_tambor.get()
    
    # print("Etiqueta:", etiqueta)
    # print("Data de Produção:", data_producao)
    # print("Lote:", lote)
    # print("Peso:", peso)
    # print("Tambor:", tambor)

    envia_impressao(etiqueta,lote,peso,data_producao,tambor)

# Cria a janela principal e define seu tamanho
window = tk.Tk()
window.title("Reeimpressão de Etiquetas")
window.geometry("300x200")

window.resizable(False, False)


# Cria um frame para centralizar os campos e o botão
frame = tk.Frame(window)
frame.place(relx=0.5, rely=0.5, anchor="center")

# Cria e posiciona as etiquetas e campos de entrada no frame
tk.Label(frame, text="Etiqueta:").grid(row=0, column=0, sticky="w", pady=(0,5))
entry_etiqueta = tk.Entry(frame)
entry_etiqueta.grid(row=0, column=1)

tk.Label(frame, text="Data de Produção:").grid(row=1, column=0, sticky="w", pady=(0,5))
entry_data_producao = tk.Entry(frame)
entry_data_producao.grid(row=1, column=1)

tk.Label(frame, text="Lote:").grid(row=2, column=0, sticky="w", pady=(0,5))
entry_lote = tk.Entry(frame)
entry_lote.grid(row=2, column=1)

tk.Label(frame, text="Peso:").grid(row=3, column=0, sticky="w", pady=(0,5))
entry_peso = tk.Entry(frame)
entry_peso.grid(row=3, column=1)

tk.Label(frame, text="Tambor:").grid(row=4, column=0, sticky="w", pady=(0,5))
entry_tambor = tk.Entry(frame)
entry_tambor.grid(row=4, column=1)


# Cria e posiciona o botão de validação
validate_button = ttk.Button(frame, text="Imprimir", command=validar)
validate_button.grid(row=5, column=0, columnspan=2, pady=(20,0))

# Inicia a execução da janela
window.mainloop()