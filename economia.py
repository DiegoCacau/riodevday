# -*- coding: utf-8 -*-

from scrapy.crawler import CrawlerProcess
from scrapy.spiders import Spider
from scrapy.selector import Selector
import os

#definiçao da classe principal
class MySpider(Spider):
	#nome da Spider
	name = "uol"
	#dominios permitidos em que a Spider entre
	allowed_domains = ["http://uol.com.br/"]
	#url onde a Spider vai começar a extraçao
	start_urls = [
	"http://cotacoes.economia.uol.com.br/acao/cotacoes-historicas.html?codigo=vale5.SA"    
	]

	#funçao para tratamento dos dados recebidos
	def parse(self, response):
		#crio a variavel seletora "sel" que recebe o conteudo do site
		sel = Selector(response)
		#seletor para a tabela com os valores a serem extaidos
		tabela = sel.xpath('//*[@id="tblInterday"]/tbody')

		#criaçao dos vetores que armazenarao os dados
		a=[] 
		b=[]
		c=[]
		d=[]
		e=[]
		f=[]
		g=[]
		
		#faço iteraçoes entre os itens da tabela
		for item in tabela:
			#seletor para os "tr"s (linhas) da tabela
			trs =  item.xpath('.//tr')
			#itero nas linhas
			for tr in trs:
				#extraio o texto de cada coluna (em cada linha)
				tds =  tr.xpath('.//td//text()').extract()
				#armazeno os dados nos vetores
				a.append(tds[0])
				b.append(tds[1])
				c.append(tds[2])
				d.append(tds[3])
				e.append(tds[4])
				f.append(tds[5])
				g.append(tds[6])

		#impressao dos valores encontrados		
		print ("")
		print("%11s %7s %6s %6s %6s %6s %8s" % ("Data/Hora"," Cotação"," Mínima","Máxima",
												" Variação","Variação (%)","Volume"))		
		for i in range(len(a)):
			print ("%11s %7s %7s %6s %10s %8s %14s" % (a[i],b[i],c[i],d[i],e[i],f[i],g[i]))			
				
		print ("")	




os.system("clear")

#cria o processo em que a Spider vai rodar
#definiçao do USER_AGENT (navegador simulado)
#desabilita os cookies para evitar que o crawler seja detectado em alguns sites e banido
#funçao de delay entre requisiçoes esta comentada, mas faz parte das boas praticas usa-la
#desabilita a funçao de log				
process = CrawlerProcess({
	'USER_AGENT' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:38.0) \
					Gecko/20100101 Firefox/38.0',
	'COOKIES_ENABLED' : False,
	#"DOWNLOAD_DELAY" : 7,
	'LOG_ENABLED' : False 
	})


#adiciona a Spider ao processo criado (podem ser adicionadas Spiders diferentes, em um mesmo processo)			
process.crawl(MySpider)
#inicia o crawler
process.start() 	
