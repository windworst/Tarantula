# -*- coding: utf-8 -*-

# # # # # # # # Thread Func # # # # # # # # 

import threading

def thread_proc(runner):
	runner.run()

def open_threads(runner,thread_num):
	runner.still_run = True
	thread_list = []
	try:
		for i in range(thread_num):
			t = threading.Thread(target=thread_proc,args=(runner,))
			t.setDaemon(True)
			t.start()
			thread_list.append(t)
	except:
		pass

	
	try:
		while True:
			alive = False
			for t in thread_list:
				alive = alive or t.isAlive()
			if not alive:
				break
	except KeyboardInterrupt:
		if runner.still_run:
			runner.still_run = False
			sys.stdout.write ('\nAccept Ctrl+C, Quitting...\n')
			sys.stdout.flush()
	except:
		pass
	runner.still_run = False

#multi-threads runner

class runner:
	still_run = False
	instance = 0

	#args: start instance in multi-threads
	def __init__(self,instance):
		self.instance = instance
		self.still_run = False

	def run(self):
		while self.still_run:
			if not self.instance():
				break

# # # # # # Bfser # # # # # # # # # # # # 

class bfser:
	bfs_set = 0
	bfs_list = 0
	list_index = 0
	set_lock = 0
	instance = 0
	incheck = 0

	def __init__(self,instance,search_start):
		self.instance = instance
		self.bfs_set = set((search_start,))
		self.bfs_list = [search_start]
		self.list_index = 0
		self.in_bfs = 1
		self.read_lock = threading.Lock()
		self.set_lock = threading.Lock()

	def __call__(self):

		self.read_lock.acquire()

		self.set_lock.acquire()		

		#when bfs over
		if self.list_index == len(self.bfs_list):
			self.set_lock.release()
			self.read_lock.release()
			return False

		#take out
		search_item = self.bfs_list[self.list_index]
		self.list_index += 1

		empty_list = self.list_index == len(self.bfs_list)
		if not empty_list:
			self.read_lock.release()

		self.set_lock.release()
		
		list = self.instance(search_item)

		self.set_lock.acquire()

		self.in_bfs -= 1
		if list:
			for item in list:
				if item not in self.bfs_set:
					self.in_bfs += 1
					self.bfs_list.append(item)
					self.bfs_set.add(item)	
		if self.in_bfs == 0 or empty_list and self.in_bfs>0:
			try:
				self.read_lock.release()
			except:
				pass
		self.set_lock.release()
		return True


# # # # # # urlcrawler # # # # # # # # # # 

import urllib2
import sys
import gzip
from cStringIO import StringIO
from urlparse import urlparse

class urlcrawler:

	timeout = 30
	collector = 0
	url = 0

	bad_filter_rules  = ['#', '.jpeg','.jpg','.rar','.png','.zip','.rar','.7z','javascript:','mailto:']

	def __init__(self,url,collector):
		self.url = url
		self.collector = collector
		self.result = []

	def __call__(self,url):
		if not url:
			return False
		real_url =  self.usable_url(url)
		if not real_url:
			return False
		redir_url,page = self.get_page(real_url)
		if redir_url !=real_url:
			return [redir_url]
		if not page:
			return False
		if not self.page_filter(real_url,page):
			return False
		self.collector(real_url,page)
		return self.geturlsfrompage(page)

	def get_page(self,url):
		page = 0
		try:
			request = urllib2.Request(url)
			UserAgent  = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36'
			request.add_header('Accept', "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp")
			request.add_header('Accept-Encoding', "*")
			request.add_header('User-Agent', UserAgent)
			rp =  urllib2.urlopen(request,timeout = self.timeout)
			
			redir_url = rp.geturl()
			if redir_url != url:
				return redir_url,False
			
			contentEncoding =  rp.headers.get('Content-Encoding')
			if  contentEncoding == 'gzip':
				compresseddata = rp.read()
				compressedstream = StringIO(compresseddata)
				gzipper = gzip.GzipFile(fileobj=compressedstream)
				page = gzipper.read()
			else:
				page = rp.read()
			
		except:
			return False,False
		return url,page

	def url_escape(self, url):
		try:
			url = urllib2.unquote(url)
			url = urllib2.quote(url.encode('utf8'))
			url = url.replace("%3A", ":")
		except Exception, e:
			pass#print "[E]UrlEscape->%s,Url:%s" % (e, url) 

		return url;


	def usable_url(self,url):
		url_lower = url.lower()
		host = self.url 

		#out of host
		if url_lower.find("http:") >= 0 or url_lower.find("https:") >= 0:
			urlHost = ''
			try:
				urlHost = str(urlparse(url).hostname) # Have Bug
			except Exception, e:
				pass#print "[E]->UrlFilter: %s" % (e)

			if urlHost.find(host) == -1:
				return False

		#url filt
		for rule in self.bad_filter_rules:
			if url_lower.find(rule) != -1: 
				return False

		#fix url
		if url.find("http:") == -1 and url.find("https:") == -1:
			if url[0] != "/" : url = "/" + url
		if url.find("http:") == -1 and url.find("https:") == -1:
			url = "http://" + host + url

		url = self.url_escape(url)
		return url
	

	def page_filter(self,url,page):
		return True

	def geturlsfrompage(self,page):
		url_list = []
		url_head = 'href="'
		pos = 0;
		while True:
			pos = page.find(url_head,pos)
			if pos==-1:
				break
			pos += len(url_head)
			end = page.find('"',pos)
			if end==-1:
				break
			url = page[pos:end]
			pos = end + 1
			#remove Anchor
			hashpos = url.rfind('#')
			if hashpos != -1:
				url = url[0:hashpos]
			url_list.append(url)
		return url_list


# # # # # # collector # # # # # # # # # # 
def to_utf8(text):
	charset_list = ['gbk','gb2312','gb18030']
	for charset in charset_list:
		try:
			return text.decode(charset).encode('utf-8')
		except Exception, e:
			pass
	return text

class simple_collector:
	result = []
	mutex = 0
	def __init__(self):
		self.result = []
		self.mutex = threading.Lock()

	def __call__(self,url,page):
		self.mutex.acquire()
		print 'get:',url
		title = self.gettitle(page)
		if not title:
			title = url
		self.result.append((title,url))
		self.mutex.release()
	
	def gettitle(self,page):
		page = to_utf8(page)
		page_lower = page.lower()
		pos = page_lower.find('<title>')
		if pos ==-1 :
			return False
		pos += len('<title>')
		end = page_lower.find('</title>',pos)
		if end == -1:
			return False
		return page[pos:end]

# # # # # # # # # # # # # # # # # # # # # # # # # # # 

#output result of collector
def out_to_file(filename,result):
	outlist = sorted(result,key = lambda item:item[0])
	f = open(filename,"w")
	f.write('%c%c%c'%(0XEF,0XBB,0XBF))#UTF Head
	f.write('<html>\n')
	f.write('<head>\n<meta http-equiv="Content-Type" content="text/html; charse=utf-8" />\n</head>\n')
	f.write('<title>Result</title>\n')
	for item in outlist:
		f.write( '<a href=\"%s\">%s</a><br />\n' % (item[1],item[0] ) )
	f.write('</html>\n')

import time
#main
if __name__=='__main__':
	if len(sys.argv)<=1:
		print 'Usage: python me.py <Host Site> [threads=10]'
		sys.exit()

	target_url = sys.argv[1].lower()

	thread_num = 10
	if len(sys.argv) >= 3:
		thread_num = int(sys.argv[2])

	target_url_lower = target_url.lower()
	if 'http://' not in target_url_lower and 'https://' not in target_url_lower:
		target_url = 'http://'+target_url
	if target_url[-1:len(target_url)] != '/':
		target_url = target_url + '/'

	target_host = target_url
	try:
		target_host = str(urlparse(target_url).hostname)
	except:
		pass
	
	print 'Site:',target_url
	print 'host:',target_host
	print 'threads:',thread_num

	s = simple_collector()
	u = urlcrawler(target_host,s)
	b = bfser(u,target_url)

	r = runner(b)

	start = time.clock()
	print 'Start...'

	open_threads(r,thread_num)
	print 'Finish...'

	checked = b.list_index
	get = len(s.result)
	print 'Checked:',checked,'Get:',get,'Time:',time.clock()-start,'sec'

	out_to_file('result.html',s.result)

