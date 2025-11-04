from fastapi import FastAPI, HTTPException, status
import pandas as pd
from pydantic import BaseModel
from uuid import UUID
import os
from typing import Optional


# arquivo CSV
ARQUIVO_CSV = "dados.csv"
#df_dados = pd.read_csv(ARQUIVO_CSV, sep=";", decimal=",")

#Definicao do Modelo de dados
class Livro(BaseModel):
    id: UUID
    titulo: str
    valor: str
    tipo: str
    imagem: str
    disponibilidade: str

db_livros: dict[UUID, Livro] = {}

# Instanciando FASTAPI no app
app = FastAPI(title="API livros", description="API de conexão com base de dados livros", version="1.0")

@app.on_event("startup")
async def load_data():
    """
    Carrega o arquivo CSV para um DataFrame do Pandas e o converte 
    em um dicionário para buscas rápidas.
    """
    global db_livros
    
    try:
        # Carrega o CSV para um DataFrame
        df_dados = pd.read_csv(ARQUIVO_CSV, sep=";", decimal=",")

        # Converte a coluna 'id' para o tipo UUID, para que a busca funcione corretamente
        df_dados['id'] = df_dados['id'].apply(lambda x: UUID(x))
        df_dados.set_index('id', inplace=True)
        
        # Converte o DataFrame para um dicionário de objetos Pydantic
        livros_dict_of_dicts = df_dados.to_dict('index')
        
        # Converte o dicionário Pandas (dict-of-dicts) para o formato Pydantic
        for id_val, dados in livros_dict_of_dicts.items():
            dados['id'] = id_val
            db_livros[id_val] = Livro(**dados)
            
        print(f"Dados carregados com sucesso! {len(db_livros)} livros encontrados.")
        
    except FileNotFoundError:
        print(f"ERRO: Arquivo '{ARQUIVO_CSV}' não encontrado.")
        db_livros = {}
    except Exception as e:
        print(f"ERRO ao carregar dados do CSV: {e}")
        db_livros = {}



@app.get(
    "/",
    summary="Retorna a ativação da API."
)
async def obter_livros():
    """
    Retorna todo o conteúdo do DataFrame em formato JSON (padrão do FastAPI).
    """
    return "API ativada"


@app.get(
    "/api/v1/books",
    tags=["JSON"],
    response_model=list[Livro],
    summary="Retorna o DataFrame completo como uma lista de objetos JSON."
)
async def obter_livros():
    """
    Retorna todo o conteúdo do DataFrame em formato JSON (padrão do FastAPI).
    """
    # to_dict(orient='records') converte cada linha em um dicionário, 
    # resultando em uma lista de objetos JSON.
    return list(db_livros.values())

@app.get("/api/v1/books/search", response_model=list[Livro], summary="Buscar Livros por Título e/ou Gênero")
async def buscar_livros_por_titulo_e_tipo(
    title: Optional[str] = None,
    category: Optional[str] = None
):
    """
    Filtra livros por parte do título e/ou pelo nome exato do gênero.
    Se nenhum parâmetro for fornecido, retorna todos os livros.
    
    - **titulo**: Filtra livros que contenham esta string no título (case-insensitive).
    - **genero**: Filtra livros que correspondam exatamente a este gênero (case-insensitive).
    """
    
    # 1. Obter todos os livros para começar a filtrar
    livros_encontrados = list(db_livros.values())
    
    # Prepara os filtros (converte para minúsculas se existirem)
    filtro_titulo = title.lower() if title else None
    filtro_genero = category.lower() if category else None
    
    # Se houver qualquer filtro, aplica a lógica
    if filtro_titulo or filtro_genero:
        
        # Filtra a lista de livros
        resultados_finais = []
        for livro in livros_encontrados:
            
            # Condições de filtro
            match_titulo = False
            match_genero = False
            
            # A. Verifica Título (Busca parcial, case-insensitive)
            if filtro_titulo:
                if filtro_titulo in livro.titulo.lower():
                    match_titulo = True
            else:
                # Se não houver filtro de título, consideramos que o título "corresponde"
                match_titulo = True
                
            # B. Verifica Gênero (Busca exata, case-insensitive)
            if filtro_genero:
                if filtro_genero == livro.tipo.lower():
                    match_genero = True
            else:
                # Se não houver filtro de gênero, consideramos que o gênero "corresponde"
                match_genero = True
            
            # O livro é adicionado à lista final se corresponder a AMBOS os filtros fornecidos
            if match_titulo and match_genero:
                resultados_finais.append(livro)
                
        livros_encontrados = resultados_finais

    # 2. Lida com o caso de não encontrar resultados
    if not livros_encontrados:
        raise HTTPException(
            status_code=404, 
            detail="Nenhum livro encontrado com os critérios de busca fornecidos."
        )

    return livros_encontrados



@app.get("/api/v1/books/{livro_id}", response_model=Livro, summary="Buscar Livro pelo ID")
async def buscar_livro_por_id(livro_id: UUID):
    """
    Busca e retorna os detalhes de um livro específico usando seu ID.

    - **livro_id**: O ID (inteiro) do livro a ser buscado.
    """
    
    # Tenta buscar o livro no "banco de dados"
    livro = db_livros.get(livro_id)
    
    # 5. Lidar com o caso de livro não encontrado
    if livro is None:
        # Se o livro não for encontrado, levanta uma exceção HTTP 404
        raise HTTPException(
            status_code=404, 
            detail=f"Livro com ID {livro_id} não encontrado."
        )
        
    # Se o livro for encontrado, ele é retornado automaticamente em formato JSON
    return livro


@app.get("/api/v1/categories", response_model=list[str], summary="Listar todos os Gêneros Únicos")
async def listar_generos():
    """
    Extrai e retorna uma lista de todos os valores únicos presentes na coluna 'genero'.
    """
    # 1. Obtém todos os objetos Livro (os valores do dicionário)
    # 2. Usa uma list comprehension para extrair o campo 'genero' de cada objeto
    # 3. Converte para um conjunto (set) para garantir que apenas valores ÚNICOS sejam mantidos
    # 4. Converte de volta para uma lista (list) para o retorno da API
    generos_unicos = sorted(list({livro.tipo for livro in db_livros.values()}))
    
    return generos_unicos














@app.get("/api/v1/health", summary="Verificar Status da API e Conectividade de Dados")
async def health_check():
    """
    Verifica se a API está online e se os dados do CSV foram carregados corretamente.

    Retorna:
    - Status 200 (OK) se a API estiver rodando e os dados estiverem carregados.
    - Status 503 (Service Unavailable) se a API estiver rodando, mas os dados não carregaram.
    """
    
    status_data = "OK"
    data_loaded = True
    message = "API online e dados do CSV carregados com sucesso."
    
    # 1. Checa a conectividade dos dados (o cache)
    if not db_livros:
        status_data = "ERROR"
        data_loaded = False
        message = f"API online, mas os dados não foram carregados. (Arquivo {CSV_FILE} ausente ou com erro de formato)."
        
        # Opcional: Verifica se o arquivo CSV está fisicamente ausente
        if not os.path.exists(ARQUIVO_CSV):
             message = f"API online, mas o arquivo CSV ({ARQUIVO_CSV}) não foi encontrado."

        # Retorna um erro 503 (Serviço Indisponível) se os dados não estiverem prontos
        return HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail={
                "status": "UNAVAILABLE",
                "message": message,
                "data_count": len(db_livros),
            }
        )

    # 2. Retorna OK se o cache de dados tiver itens
    return {
        "status": "OK",
        "message": message,
        "data_source": ARQUIVO_CSV,
        "data_count": len(db_livros),
    }
