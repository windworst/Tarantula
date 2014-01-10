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

	while True:
		try:
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
			break
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

class bfser:http://www.cz88.net/down/download.php?id=234&url=Y3o4OF5xbW1pIzY2fXU3fnZ2fnV8N3p2dDZpcHdgcHc2bys2fnZ2fnV8aXB3YHB3cHdqbXh1dXxrN3xhfCRjejg4
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
		self.in_bfs = 0
		self.set_lock = threading.Lock()

	def __call__(self):
		self.set_lock.acquire()

		if self.list_index == len(self.bfs_list):
			self.set_lock.release()
			return self.in_bfs

		search_item = self.bfs_list[self.list_index]
		self.list_index += 1

		self.in_bfs += 1

		self.set_lock.release()
		
		list = self.instance(search_item)
		
		self.set_lock.acquire()
		self.in_bfs -= 1

		if list:
			for item in list:
				if item not in self.bfs_set:
					self.bfs_list.append(item)
					self.bfs_set.add(item)		
		self.set_lock.release()
		return True


# # # # # # urlcrawler # # # # # # # # # # 

import urllib2
import re
import sys

class urlcrawler:

	timeout = 5
	collector = 0
	url = 0

	def __init__(self,url,collector):
		self.url = url
		self.collector = collector
		self.result = []

	def __call__(self,url):
		real_url =  self.usable_url(url)
		if not real_url:
			return False
		page = self.get_page(real_url)
		if not page:
			return False
		if not self.page_filter(real_url,page):
			return False
		self.collector(real_url,page)
		return self.geturlsfrompage(page)

	def get_page(self,url):
		page = 0
		try:
			headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'} 
			req = urllib2.Request(url,headers = headers)
			page =  urllib2.urlopen(req,timeout = self.timeout).read()
		except:
			return False
		type = sys.getfilesystemencoding()  
		return page

	def usable_url(self,url):
		if self.url in url:
			return url
		if "http://" not in url:
			return self.url + url
		return False

	def page_filter(self,url,page):
		return True

	def geturlsfrompage(self,page):
		url_list = []
		url_head = "<a href="
		list = page.split('\n')
		p = re.compile("<a\s+href=\\\"\S[^\\\"]+\\\"")
		for line in list:
			m = p.search(line)
			if m:
				url = m.string[m.start()+len(url_head)+1:m.end()-1]
				url_list.append(url)
		return url_list


# # # # # # collector # # # # # # # # # # 

def remove_brackets(line):
	host = ''
	flag = False
	for c in line:
		if not flag:
			if c == '<':
				flag = True
			else:
				host += c
		else:
			if c == '>':
				flag = False
				host += ' '
	return host

import string

def gethostfrompage(page):
	list = page.split('\n')
	hostlist = []

	ip_str = 0
	reip = re.compile('\d+\.\d+\.\d+\.\d+')
	report = re.compile('\d+')
	for line in list:
		mip = 0
		mport = 0
		flag = False
		host = remove_brackets(line)

		if not ip_str:
			mip = reip.search(host)
			if mip:
				ip_str = mip.string[mip.start():mip.end()]
				mport = report.search(host[mip.end():len(host)])
		else:
			mport = report.search(host)
		if mport:
			port = string.atoi(mport.string[mport.start():mport.end()])
			addr = (ip_str,port)
			hostlist.append(addr)
			ip_str = 0
	return hostlist

class simple_collector:
	result = []
	mutex = 0
	def __init__(self):
		self.result = []
		self.mutex = threading.Lock()

	def __call__(self,url,page):
		self.mutex.acquire()
		print url
		self.result.append(url+'\n')
		self.mutex.release()

# # # # # # # # # # # # # # # # # # # # # # # # # # # 


s = simple_collector()
u = urlcrawler("http://www.cz88.net",s)
b = bfser(u,"http://www.cz88.net/proxy/index.aspx")

r = runner(b)

open_threads(r,100)

s.result.sort()
f = open("save.txt","w")
f.writelines(s.result)
