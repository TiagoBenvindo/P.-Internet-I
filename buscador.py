import requests
import requests_cache
from bs4 import BeautifulSoup 

requests_cache.install_cache() # Implementando cache
#requests_cache.clear() # Limpando cache

paginas = [] # guadar todas as paginas e o seu nivel
paginas_palavra = [] # guardar todas as paginas contendo a palavra
texto = [] # guardar todas as ocorrencias com os trechos

# Baixa a página
def download(url):
	response = ''
	try:
		response = requests.get(url)
	except Exception as ex:
		response = None
	finally:
		return response


def texto_da_pagina(pagina):
	soup = BeautifulSoup(pagina.text,'html.parser')
	page = soup.text

	return page

# Busca e guarda trecho do texto contendo a palavra
def busca_guarda_palavra(keyword,page):
	tamanho_keyword = len(keyword)
	trecho_ocorrencia = ''
	# Busca palavra
	palavra = page.find(keyword)

	# Guarda palavra
	if palavra < 0:
		return texto
	elif palavra < 15:
		texto.append(page[0:palavra+tamanho_keyword+15:1])
	elif palavra > 15:
		texto.append(page[palavra-15:palavra+tamanho_keyword+15:1])

	page = page[:palavra] + page[palavra+tamanho_keyword:]
	nova_ocorrencia = page.find(keyword)

	if nova_ocorrencia != None:
		busca_guarda_palavra(keyword,page)
	
	return texto

# Formata link
def formatar_link(url,url_original):
	if url != None:
		if url.startswith('http://') or url.startswith('https://'):
			return url
		elif url.startswith('/'):
			return url_original + url
		else:
			return url

# Percorre os links
def percorre_links(pagina,url):
	# Cria objeto 
	soup = BeautifulSoup(pagina.text,'html.parser')
	# Busca os links dentro da página
	links = soup.find_all('a')
	if len(links) > 10:
		links = links[0:10]
	# Guada os links em uma lista
	for link in links:
		if formatar_link(link.get('href'),url) != None:
			url = formatar_link(link.get('href'),url)			
			paginas.append(url)

	return


def exibir_links():
	print('------------------------------------------------------')
	print('Os 10 primeiros links encontrados')
	for pagina in paginas:
		print(str(paginas.index(pagina)+1) + ': ' + pagina)


def busca(url):
	pagina = download(url)
	percorre_links(pagina,url)
	exibir_links()
	keyword = input('Digite a palavra chave para a busca: ')
	link_da_lista = int(input('Digite o numero correspondete ao link desejado: ')) - 1
	pagina = download(paginas[link_da_lista])
	if pagina != None:
		page = texto_da_pagina(pagina)
		if busca_guarda_palavra(keyword,page) != None:
			print('------------------------------------------------------')			
			print('Trechos com a palavra desejados encontrados')
			for trecho in texto:
				print(trecho)
		else:
			print('------------------------------------------------------')			
			print('Palavra não encontrada')
	else:
		print('------------------------------------------------------')
		print('Erro na requsição da pagina')


def main():
	continua = True
	while (continua):
		url = input('Coloque o link de sua escolha: ')
		busca(url)
		continua = int(input('Se desejar realizar novamente digite 1: '))


if __name__ == '__main__':
	main()