import requests
import pandas as pd
from bs4 import BeautifulSoup
import uuid

## Salvar dados em CSV
def salvar_csv(dados, nome_arquivo="dados.csv"):
    """Salva os dados coletados em um arquivo CSV."""
    if not dados:
        print("Nenhum dado para salvar.")
        return

    # Converte a lista de dicionários para um DataFrame do pandas
    df = pd.DataFrame(dados)
    
    # Salva o DataFrame como CSV
    df.to_csv(nome_arquivo, index=False, encoding='utf-8', sep=';')
    print(f"\n✅ Dados salvos com sucesso em: {nome_arquivo}")    

# local de armazenamento dos dados
dados_livros = []


for num_pagina in range(1,51):
    
    if num_pagina <=51:
        #request faz requisicoes para obter o html de uma páginma
        url = "https://books.toscrape.com" if num_pagina <=1 else f"https://books.toscrape.com/catalogue/page-{num_pagina}.html"
        response = requests.get(url)

        # pegar o html em response.text, mas está bastante sujp
        if response.status_code == 200:
            html_content =  response.text
            print("HTML obtido com sucesso")
        else:
            print("erro:", response.status_code)


        # Usamos o beautifulSoup para deixar mais arrumado o html
        soup = BeautifulSoup(response.text, 'lxml')

        # pegando o href dos livros
        lista_hrefs = []
        links_dos_produtos = soup.select('ol.row li article.product_pod h3 a')
        for link in links_dos_produtos:
            href = link.get('href')
            lista_hrefs.append(href)
        
        # Pegando o titulo de cada livro
        lista_title = [i['title'] for i in soup.find_all('a', title=True)]
        iterador_titulo = 0
        
        # iterando sobre os Href e fazendo a conexão com cada uma das URL
        for link in lista_hrefs:
            url_base = "https://books.toscrape.com/" if num_pagina ==1 else "https://books.toscrape.com/catalogue/"
            link_completo = url_base+link
            print(link_completo)
            response_link = requests.get(link_completo)
            soup_pagina_livro = BeautifulSoup(response_link.text, 'lxml')


            titulo = lista_title[iterador_titulo]

            valor = soup_pagina_livro.find("p",{"class":"price_color"})
            disponibilidade = soup_pagina_livro.find("p",{"class":"instock availability"})

            # pegando o tipo do livros
            todas_as_tags_a = soup_pagina_livro.select('ul.breadcrumb a')

            if len(todas_as_tags_a) > 2:
                tipo = todas_as_tags_a[2].text.strip()
            print(tipo)

            # pegando a imagem
            tag_img = soup_pagina_livro.select_one('div.item.active img')
            url_imagem = tag_img.get('src')
            print(url_imagem)

            # pegando informacoes de disponibilidade
            tag_availability = soup_pagina_livro.find('th', string='Availability')
            disponibilidade = tag_availability.find_next_sibling('td').text
            print(disponibilidade)



            # pegando informacões sobre o rating
            tag_rating = soup.select_one('p.star-rating')

            # Extrair a string completa da classe
            if tag_rating and 'class' in tag_rating.attrs:
                # Retorna uma lista de strings: ['star-rating', 'One']
                classes = tag_rating['class']
    
            # 4. Encontrar a classe de classificação
            if len(classes) >= 2:
                rating = classes[1]
                print(f"Classificação encontrada: {rating}")

            

            dados_livros.append(
                {
                    "id": uuid.uuid4(),
                    "titulo":titulo,
                    "valor": valor.text,
                    "tipo": tipo,
                    "imagem": url_imagem,
                    "disponibilidade": disponibilidade,
                    "rating": rating

                })
            print(link_completo)
            iterador_titulo = iterador_titulo + 1

        salvar_csv(dados_livros)
        
    else:
        break


                                                                           









 



