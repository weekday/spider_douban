#coding:utf-8



from doubanSQL import SpiderData
import requests
from lxml import etree
'''
   爬取豆瓣电影top250上相关电影的信息，包括影片链接、影片名称、上映时间、排名、豆瓣评分、导演、剧情简介。
'''

header = {
			'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'
		}
dbconn = SpiderData()

def getSpiderData(page):
	#豆瓣top250，每页25部电影
	start_number = (int(page) - 1) * 25
	start = 0
	while start <= start_number:
		#访问网址，可以看到其规律在于'start='后面值得变化，按照25的倍数变化
		url = 'https://movie.douban.com/top250?start={0}&filter='.format(start)

		#使用requests模块获取网页信息
		request = requests.get(url,headers=header)
		content = request.content.decode('utf-8')

		html = etree.HTML(content)

		#使用xpath过滤所有相关影片链接
		all_url_list = html.xpath(u"//div[@class='info']/div[@class='hd']/a/@href")

		for u in all_url_list:
			request = requests.get(url=u,headers = header)
			content = request.content

			html2 = etree.HTML(content)
			#获取排名
			top_number = html2.xpath(u"//div[@class='top250']/span/text()")
			if top_number:
				movie = html2.xpath(u'//h1/span/text()')

				#获取电影名称
				movie_name = movie[0].encode('utf-8')
				#上映时间
				movie_year = movie[1]
				#豆瓣评分
				score = html2.xpath(u"//div[@class='rating_wrap clearbox']/div[@class='rating_self clearfix']/strong/text()")[0]
				#导演
				daoyan = html2.xpath(u"//div[@id='info']/span/span[@class='attrs']/a/text()")[0].encode('utf-8')
				#剧情简介
				conten = html2.xpath(u"//div[@id='link-report']/span/text()")[0].encode('utf-8')

				dbconn.create(url=u,movieName=movie_name,movieYear=movie_year,movieAtor=daoyan,movieScore=score,movieRank=top_number,movieDes=conten)

		start += 25

if __name__ == '__main__':
	getSpiderData(10)
