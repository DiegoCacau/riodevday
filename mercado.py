# -*- coding: utf-8 -*-

from scrapy.crawler import CrawlerProcess
from scrapy.spiders import Spider
from scrapy.selector import Selector

#definiçao da classe principal
class MySpider(Spider):
	#nome da Spider
	name = "mercado"
	#dominios permitidos em que a Spider entre
	allowed_domains = ["http://mercadolivre.com.br/"]
	#url onde a Spider vai começar a extraçao
	start_urls = [
		"http://informatica.mercadolivre.com.br/placas-video/pci-express/a-partir-1-gb/placa-de-video"    
	]

	#funçao para tratamento dos dados recebidos
	def parse(self, response):
		#crio a variavel seletora "sel" que recebe o conteudo do site
		sel = Selector(response)
		#seletor para os itens na vitrine da pagina
		tabela = sel.xpath('//*[@id="searchResults"]/li[@class="article"]')

		#criaçao dos vetores que armazenarao os dados
		nome_ = []
		preco_ = []
		cent_ = []

		#faço iteraçoes entre os itens da vitrine
		for item in tabela:

			#extraio nomes, preços e centavos
			nomes =  item.xpath('.//a[@class=" "]//text()').extract()
			precos = item.xpath('.//ul/li[1]/div/span//text()').extract()
			cents = item.xpath('.//ul/li[1]/div/span/sup//text()').extract()

			#faço iteraçoes nos vetores de dades extraidos anteriormente e faço a limpeza dos mesmo
			#converter de unicode para utf-8 faria a mesma coisa
			for nome in nomes:
				nome_.append(nome.replace("[u'", "") ) 
			for preco in precos:
				preco_.append(preco.replace("[u'", ""))	
			for cent in cents:
				cent_.append(cent.replace("[u'", ""))

			#printo na tela os nomes e preços extraidos	
			for x in range(len(nome_)):
				print (nome_[x])
				print (preco_[int(x+(2*x))] +","+ cent_[x])
	


#cria o processo em que a Spider vai rodar
#definiçao do USER_AGENT (navegador simulado)
#desabilita os cookies para evitar que o crawler seja detectado em alguns sites e banido
#funçao de delay entre requisiçoes esta comentada, mas faz parte das boas praticas usa-la
#desabilita a funçao de log
process = CrawlerProcess({
	'USER_AGENT' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0',
	'COOKIES_ENABLED' : False,
	#"DOWNLOAD_DELAY" : 7,
	'LOG_ENABLED' : False 
	})


#adiciona a Spider ao processo criado (podem ser adicionadas Spiders diferentes, em um mesmo processo)			
process.crawl(MySpider)
#inicia o crawler
process.start() 	