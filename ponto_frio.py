# -*- coding: utf-8 -*-

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import Spider
from scrapy.selector import Selector



#definiçao da classe principal
class MySpider(Spider):
	#nome da Spider
	name = "pontofrio"
	#dominios permitidos em que a Spider entre
	allowed_domains = ["http://pontofrio.com.br/"]
	#url onde a Spider vai começar a extraçao
	start_urls = [
		"http://www.pontofrio.com.br/TelefoneseCelulares/Smartphones/Android/?Filtro=C38_C326_C3266"    
	]

	#funçao para tratamento dos dados recebidos
	def parse(self, response):
		#crio a variavel seletora "sel" que recebe o conteudo do site
		sel = Selector(response)
		#busco pelo link da proxima pagina e armazeno no seletor "proxima"
		proxima = sel.xpath('//*[@id="ctl00_Conteudo_ctl04_divBuscaResultadoInferior"]/div/ul/li[@class="next"]//@href')
		#seletor para os itens na vitrine da pagina
		itens = sel.xpath('//ul[@class="vitrineProdutos"]/li/div/a')
		#abro o arquivo de saida no modo "append"
		a = open("saida.txt","a")
		#faço iteraçoes entre os itens da vitrine
		for item in itens:
			#extraio o nome do produto da iteraçao
			nome = item.xpath('strong[@class="name fn"]//text()').extract()
			#extraio o preço do produto da iteraçao
			preco = item.xpath('span[@class="productDetails"]/span[@class="for price sale"]/strong//text()').extract()
			#para garantir que so serao escritos no arquivo de saida os produtos em estoque (que possuem preço)
			if len(nome) > 0 and len(preco) > 0:
				a.write(nome[0]+"\n")
				a.write(preco[0]+"\n\n")
		#fecha o arquivo de saida
		a.close()

		#caso haja link de proxima pagina, o adiciona a lista de urls a serem extraidas, 
		#faz o request dela e recomeça o processo de tratamento dos dados
		#caso nao haja link de proxima, printa "Fim do Programa!" e termina a execuçao
		try:	
			yield self.make_requests_from_url(proxima.extract()[0])
		except:
			print('Fim do Programa!')	
		







	
#cria o processo em que a Spider vai rodar
#definiçao do USER_AGENT (navegador simulado)
#desabilita os cookies para evitar que o crawler seja detectado em alguns sites e banido
#funçao de delay entre requisiçoes esta comentada, mas faz parte das boas praticas usa-la
#desabilita a funçao de log
process = CrawlerProcess({
	'USER_AGENT' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0',
	'COOKIES_ENABLED' : False,
	#"DOWNLOAD_DELAY" : 3,
	'LOG_ENABLED' : False 
	})

#cria o arquivo de saida
a = open("saida.txt","w")
a.close()
#adiciona a Spider ao processo criado (podem ser adicionadas Spiders diferentes, em um mesmo processo)
process.crawl(MySpider)
#inicia o crawler
process.start() 	