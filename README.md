# ROBO CONSULTA SUBLOGINS

### Este robô em Python realiza consulta a sublogins de Corretor com base nos códigos de funcinário inseridos e separados por ",".

- Query base da consulta:

```sql
SELECT
                codigo AS CallCenter,
                Login,
                nome,
                cpf
            FROM Corretor_Usuarios
            WHERE codigo_funcionario IN (
                
                -- Códigos AQUI!!!
            
            )
            AND STATUS = 'A' 
```

## Para Start do projeto siga o passo a passo abaixo:

- Crie um ambiente virtual

```python -m venv venv```

- Ative o ambiente

```venv\Scripts\activate```

- Instale as dependências contidas no requirements.txt

```pip install -r riquirements.txt```

- Crie o executável com Interface

```pyinstaller --onefile interface.py```

- Criar sem Interface

```pyinstaller --onefile consulta.py```

### Após a criação do executável, o mesmo se encontrará dentro da pasta dist com o nome "consulta.exe"
### Obs.: Deve ser excluido o arquivo "consulta.spec" pois não é necessário.
