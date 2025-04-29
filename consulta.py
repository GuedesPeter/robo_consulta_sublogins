import pyodbc


server = 'FAC-DB53.facta.com.br'
database = 'Facta_01_BaseDados'
driver = '{ODBC Driver 17 for SQL Server}'

conn = None
cursor = None

try:
   
    conn = pyodbc.connect(
        f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes;ApplicationIntent=ReadOnly'
    )
    cursor = conn.cursor()
    print("Conexão estabelecida com sucesso!")

    while True:
        entrada = input("Digite os códigos de funcionário separados por vírgula (ou 'exit' para sair): ")
        if entrada.lower() == 'exit':
            break

        codigos_str = [codigo.strip() for codigo in entrada.split(',')]
        codigos = [codigo for codigo in codigos_str if codigo.isdigit()]

        if not codigos and codigos_str != ['']:
            print("Nenhum código válido informado.")
            continue

        if codigos:
            
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

                
                if resultados:
                    print("\nResultados encontrados:")
                    for row in resultados:
                        print(f"Código: {row.CallCenter} | Login: {row.Login} | Nome: {row.nome} | CPF: {row.cpf}")
                else:
                    print("Nenhum registro encontrado para os códigos informados.")
            except pyodbc.Error as e:
                print("Erro ao executar a consulta:", e)
        else:
            print("Nenhum código de funcionário foi digitado.")

except pyodbc.Error as e:
    print("Erro ao conectar ao banco de dados:", e)
except Exception as e:
    print(f"Ocorreu um erro inesperado: {e}")

# Fecha conexão
finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
    print("Conexão encerrada.")