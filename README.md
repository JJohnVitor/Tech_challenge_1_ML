### Descrição do projeto
Este script é uma aplicação de Web Scraping de catálogo paginado, desenvolvida para extrair dados detalhados de livros e estruturá-los em CSV. A aplicação opera em um fluxo de dois níveis: primeiro, um Loop de Navegação utiliza a biblioteca requests para iterar pelas páginas do catálogo. Em cada página, o BeautifulSoup é empregado para coletar os links e títulos de todos os livros. Em seguida, um Loop de Detalhe realiza uma nova requisição para cada link, extraindo informações cruciais como preço, categoria, disponibilidade e rating. Os dados coletados são estruturados em um dicionário, recebem um id UUID e são armazenados. Finalmente, a função de Persistência utiliza a biblioteca Pandas para converter a lista completa em um DataFrame e salvá-lo como um arquivo CSV, garantindo a organização final dos dados.

Após isso, API RESTful de alto desempenho, desenvolvida em FastAPI para servir dados de um catálogo de livros. A arquitetura centraliza-se em um mecanismo de cache em memória (db_livros), onde todos os dados são lidos do arquivo CSV (dados.csv) para um dicionário Python durante a inicialização (@app.on_event("startup")). O código utiliza Pydantic para validar a estrutura dos dados (Livro) e oferece endpoints otimizados. As funcionalidades incluem a listagem completa dos livros, a busca detalhada por ID, a filtragem avançada por título e categoria, e um endpoint de /health para verificar a disponibilidade do serviço e a integridade do carregamento dos dados. O uso do cache garante que as consultas sejam extremamente rápidas.

### Instruções de instalação e configuração
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

### Instruções para execução
1. Executar scraping na página web
python scraping.py

2. Ativar API
uvicorn app:app --reload

### Exemplos de chamadas e documentação
1. /api/v1/books - Retorna o DataFrame completo como uma lista de objetos JSON.
2. /api/v1/books/search -  Filtra livros por parte do título e/ou pelo nome exato do gênero.
3. /api/v1/books/{livro_id} -  Busca e retorna os detalhes de um livro específico usando seu ID.
4. /api/v1/categories -  xtrai e retorna uma lista de todos os valores únicos presentes na coluna 'tipo'.
5. /api/v1/health - Verifica se a API está online e se os dados do CSV foram carregados corretamente.

    Retorna:
    - Status 200 (OK) se a API estiver rodando e os dados estiverem carregados.
