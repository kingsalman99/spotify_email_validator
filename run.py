import requests
import re
import time
import threading
import sys
import queue
import sys
import datetime
import json
import asyncio
from proxybroker import Broker
import random
from colorama import init
init()
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
print(f"""
  +-------------------------------------------------+
  | {bcolors.OKGREEN}Spotify Email Validator{bcolors.ENDC}                         |
  +-------------------------------------------------+ 
  | {bcolors.WARNING}Version 1.0{bcolors.ENDC}            | {bcolors.OKBLUE}github.com/lav13enrose{bcolors.ENDC} |
  +-------------------------------------------------+
  | 1. PROXY GRABBING - LIVE PROXY FROM API         |
  | 2. MULTI THREAD CHECKING                        |
  | 3. AUTO SAVE RESULT WITH EACH TEXT FILE         |
  +-------------------------------------------------+
  |            {bcolors.OKBLUE}github.com/lav13enrose{bcolors.ENDC}               |  
  +-------------------------------------------------+
""")
async def save(proxies, filename):
	with open(filename, 'w') as f:
		while True:
			proxy = await proxies.get()
			if proxy is None:
				break
			proto = 'https' if 'HTTPS' in proxy.types else 'http'
			row = '%s://%s:%d\n' % (proto, proxy.host, proxy.port)
			f.write(row)
def main():
	proxies = asyncio.Queue()
	broker = Broker(proxies)
	tasks = asyncio.gather(
		broker.find(types=['HTTP', 'HTTPS'], limit=100),
		save(proxies, filename='proxies.txt'),
	)
	loop = asyncio.get_event_loop()
	loop.run_until_complete(tasks)
try:

	nanya_proxy = input("[+] Fetch Proxy? (y/n) : ")
	if "y" in nanya_proxy:
		main()
	elif "Y" in nanya_proxy:
		main()	
	elif "n" in nanya_proxy:
		print("[!] Make sure you already have proxies.txt")
		pass
	elif "N" in nanya_proxy:
		print("[!] Make sure you already have proxies.txt")
		pass
	else:
		print("[!] its a yes or no question, my cat even know that")
		exit()
except KeyboardInterrupt:
	print("\n[!] Keyboard Interrupt, exiting...")
	exit()
class spotify():
	version = "Spotify Email Validator v1" #Dont Remove this you total dipshit
	input_queue = queue.Queue()
	def __init__(self):
		try:
			self.mailist = input("[+] Enter Mailist : ")
			self.thread = input("[+] Thread : ")
			self.count_list = len(list(open(self.mailist)))
		except KeyboardInterrupt:
			print("\n[!] Keyboard Interrupt, exiting...")
			exit()
	def filesave(self,filetext,x):
		kl = open(filetext, 'a+')
		kl.write(x)
		kl.close()
	def post_email(self,eml):
		anjayz = random.choice(open('proxies.txt').readlines())
		proxies = {
			"http": anjayz,
		}
		r = requests.get('https://spclient.wg.spotify.com/signup/public/v1/account',
                    params={'validate': '1','email': eml}, proxies=proxies
				)
		buset = json.loads(r.content)
		penentu = buset["status"]
		if "20" in str(penentu): return 'live'
		elif "1" in str(penentu): return 'die'
		elif "0" in str(penentu): return 'banned'
		else : return 'unknown'
	def chec(self):
		while 1:
			eml = self.input_queue.get()
			result = self.post_email(eml)

			if result == 'live':
				print('[L] ',datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'- LIVE - '+eml)
				self.filesave('live.txt',eml+'\n')
			elif result == 'die':
				print('[D]',datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'- DEAD - '+eml)
				self.filesave('die.txt',eml+'\n')
			elif result == 'banned':
				print('[B]',datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'- IP BAN - '+eml)
			elif result == 'unknown':
				print('[U]',datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'- UNKN - '+eml)
				self.filesave('unknown.txt',eml+'\n')

			self.input_queue.task_done()

	def run_thread(self):

		for x in range(int(self.thread)):
			t = threading.Thread(target=self.chec)
			t.setDaemon(True)
			t.start()

		for y in open(self.mailist, 'r').readlines():
			self.input_queue.put(y.strip())
		self.input_queue.join()

	def finish(self):
		print('')
		print('-------------------------------------------------')
		print('Live : ',len(list(open('live.txt'))),'emails')
		print('Die : ',len(list(open('die.txt'))),'emails')
		print('Unknown : ',len(list(open('unknown.txt'))),'emails')
		print('')

			

heh = spotify()
heh.run_thread()
heh.finish()
