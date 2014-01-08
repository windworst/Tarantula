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

class bfser:
	bfs_set = 0
	bfs_list = 0
	list_iter = 0
	set_lock = 0
	instance = 0

	def __init__(self,instance,search_start):
		self.instance = instance
		self.bfs_set = set((search_start,))
		self.bfs_list = [search_start]
		self.list_iter = iter(self.bfs_list)
		self.set_lock = threading.Lock()

	def __call__(self):
		try:
			self.set_lock.acquire()
			search_item = self.list_iter.next()
		except:
			return False
		finally:
			self.set_lock.release()
		list = instance(search_item)

		self.set_lock.acquire()
		for item in list
			if item not in self.bfs_set:
				self.bfs_list.append(item)
				self.bfs_set.add(item)
		self.set_lock.release()
		return True


# # # # # # urlcrawler # # # # # # # # # # 

import urllib

class urlcrawler:

	collector = 0
	url = 0

	def __init__(self,url,collector):
		self.url = url
		self.collector = collector
		self.result = []

	def __call__(self,url):
		if not url_filter(url):
			return False
		page = get_page(url)
		if not page_filter(page):
			return False
		self.collector(url,page)
		return geturlsfrompage(page)

	def get_page(self,url):
		return urllib.urlopen(url).read()

	def url_filter(self,url):
		return True

	def page_filter(self,url,page):
		return True

	def geturlsfrompage(self,page):
		return []

