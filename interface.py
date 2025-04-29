import pyodbc
import tkinter as tk
from tkinter import messagebox, scrolledtext

# Função para conectar ao banco de dados
def conectar_bd():
    server = 'FAC-DB53.facta.com.br'
    database = 'Facta_01_BaseDados'
    driver = '{ODBC Driver 17 for SQL Server}'

    try:
        conn = pyodbc.connect(
            f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes;ApplicationIntent=ReadOnly'
        )
        cursor = conn.cursor()
        return conn, cursor
    except pyodbc.Error as e:
        messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {e}")
        return None, None

# Função para executar a consulta
def executar_consulta():
    conn, cursor = conectar_bd()
    if not conn or not cursor:
        return

    # Obtenção do código de funcionário inserido
    codigos_str = entry_codigos.get().strip().split(',')
    codigos = [codigo.strip() for codigo in codigos_str if codigo.isdigit()]

    if not codigos:
        messagebox.showwarning("Aviso", "Nenhum código válido informado.")
        return

    placeholders = ','.join('?' for _ in codigos)
    query = f"""
    SELECT
        codigo AS CallCenter,
        Login,
        nome,
        cpf
    FROM Corretor_Usuarios
    WHERE codigo_funcionario IN ({placeholders})
    AND STATUS = 'A'
    """

    try:
        cursor.execute(query, codigos)
        resultados = cursor.fetchall()

        # Limpar o campo de resultados antes de mostrar novos resultados
        result_text.delete(1.0, tk.END)

        if resultados:
            for row in resultados:
                result_text.insert(tk.END, f"Código: {row.CallCenter} | Login: {row.Login} | Nome: {row.nome} | CPF: {row.cpf}\n")
        else:
            result_text.insert(tk.END, "Nenhum registro encontrado para os códigos informados.\n")

    except pyodbc.Error as e:
        messagebox.showerror("Erro", f"Erro ao executar a consulta: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Criando a janela principal
root = tk.Tk()
root.title("Consulta de Sublogins de Corretor")
root.geometry("600x400")

# Label e Entry para o código de funcionário
label_codigos = tk.Label(root, text="Digite os códigos de funcionário separados por vírgula:")
label_codigos.pack(pady=10)

entry_codigos = tk.Entry(root, width=50)
entry_codigos.pack(pady=5)

# Botão para executar a consulta
btn_consultar = tk.Button(root, text="Consultar", command=executar_consulta)
btn_consultar.pack(pady=10)

# Campo de texto para mostrar os resultados
result_text = scrolledtext.ScrolledText(root, width=70, height=10, wrap=tk.WORD)
result_text.pack(pady=10)

# Rodapé (opcional)
footer_label = tk.Label(root, text="Desenvolvido por OpenAI | Consultas de Sublogins")
footer_label.pack(side=tk.BOTTOM, pady=5)

# Iniciar o loop da interface gráfica
root.mainloop()
