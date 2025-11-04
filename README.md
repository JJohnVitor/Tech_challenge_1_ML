1. Criar o Ambiente Virtual (venv)
Execute este comando no terminal (na raiz do projeto) para criar a pasta venv que isolará as dependências:

Bash
python -m venv venv

2. Ativar o Ambiente Virtual
A ativação é crucial para que as bibliotecas sejam instaladas no ambiente correto. O comando varia de acordo com o sistema operacional:

No Windows (PowerShell):
.\venv\Scripts\Activate.ps1

No Windows (Prompt de Comando - CMD):
Bash
venv\Scripts\activate

No macOS ou Linux:
Bash
source venv/bin/activate


3. Instalar as Dependências
Com o ambiente virtual ativo (você verá (venv) no seu terminal), instale todas as bibliotecas listadas no arquivo requirements.txt:

Bash
pip install -r requirements.txt


4. Executar scraping na página web
python scraping.py

5. Ativar API
uvicorn app:app --reload 


