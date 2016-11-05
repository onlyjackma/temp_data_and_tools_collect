#!/usr/bin/python
# -*- coding:utf-8 -*- 

import Queue
import threading
import requests
import simplejson as json
import time
import sys
class WorkingThread(threading.Thread):
	URL='http://hm.iovyw.com/platform/res/rpc.do'

	def __init__(self, queue, command):
		threading.Thread.__init__(self)
		self.queue = queue
		self.command = command
		self.flag = False

	def checkOnline(self, devsn):
		req={'method':'list','param':devsn}
		r=requests.post(self.URL,data=req)
		if r.status_code!=200:
			return False
		v=r.text.encode('utf-8').strip().split(',')
		print(r.text.encode('utf-8'))
		if len(v)==3 and v[1]=='1':
			return True
		return False

	def getDevInfo(self, dev):
		devsn=dev['sn']
		devnum=dev['num']
		if self.checkOnline(devsn)==False:
			print("######################################################\n### %s:%s\nOFFLINE\n" % (devsn,devnum) )
			odev={'sn':devsn,'online':0,'num':devnum}
			#self.queue.put(odev)
			self.flag = False
			return False
		mycommand=self.command
		print(mycommand)
		param={'sn':devsn, 'script':mycommand}
		req={'method':'shell','param':json.dumps(param)}
		r=requests.post(self.URL,data=req)
		print("######################################################\n### %s:%s result:%s\n" % (devsn,devnum,r.text.encode('utf-8')) )
		print("\n### %s:%s result:%s\n" % (devsn,devnum,r.text.encode('utf-8')) )
		self.flag = True
		return True

	def run(self):
		while True:
			if self.queue.empty():
				break
			dev = self.queue.get()
			self.getDevInfo(dev)
			self.queue.task_done()
			if self.flag:
				time.sleep(1)
			else:
				time.sleep(1)

def LoadDevList(devQueue):
	URL='http://16wifi.iovyw.com/e3g/res/rpc.do'
	req={'method':'list'}
	r=requests.post(URL,data=req)
	if r.status_code!=200:
		return False
	lines=r.text.encode('utf-8').split('\n')
	for line in lines:
		v=line.strip().split(',')
		if len(v)!=3:
			print("Ignore: "+line)
			continue
		dev={'sn':v[0], 'online':v[1], 'num':v[2]}
		devQueue.put(dev)
	return True

def LoadDevFromFile(devQueue, filename):
	f = open(filename, "r")
	if f is None:
		print(filname + " not exitst")
		return False

	i = 1
	for line in f:
		dev={'sn':line.strip(), 'online':0, 'num':i}
		i=i+1
		devQueue.put(dev)
	f.close()

	return True

def main():
	#command="logread | grep 'Info:acc'"
	#command="mount | grep extdata"
	threads=[]
	filename=sys.argv[2]
	#command = "cd /tmp; wget http://115.28.137.90/up.sh -O /tmp/t.sh && chmod +x /tmp/t.sh; /tmp/t.sh "
	command = sys.argv[1] #"cd /tmp;uci get -P /var/state update.base.version 2>/dev/null"
	queue = Queue.Queue()
	LoadDevFromFile(queue,filename)
	for i in range(5):
		t = WorkingThread(queue, command)
		#t.setDaemon(True)
		threads.append(t)
		t.start()
	
	#LoadDevList(queue)
	for j in range(5):
		threads[j].join()

	queue.join()

if __name__=='__main__':
	start = time.time()
	main()
	print "Elapsed Time: %s" % (time.time() - start)


