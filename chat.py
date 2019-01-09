#!/usr/bin/python3

import requests, json, sys, os, re
from time import sleep
from colorama import Style, Fore, init

init(autoreset = True)

class chat:

    def __init__(self, lang):
        self.url = "http://sandbox.api.simsimi.com/request.p"
        self.key = open("key.txt").read().strip()
        self.lang = lang

    def getRespon(self, **args):
        queryString = {
            "key" : self.key,
            "text" : args["chat"],
            "lc" : self.lang
        }
        try :
            sendChat = requests.get(self.url, params = queryString)
            return sendChat.text
        except requests.exceptions.ConnectionError:
            print("[!] Make sure you've been connected to internet!")
            sys.exit(0)

    def getChat(self, chat):
        responServ  = self.getRespon(chat = chat)
        jsonDecode  = json.loads(responServ)
        if jsonDecode["msg"] != "OK.":
            return jsonDecode["msg"]
        else:
            return jsonDecode["response"]

def loading():
    try:
        for x in range(3):
            sys.stdout.write(".")
            sys.stdout.flush()
            sleep(0.45)
        print()
    except (KeyboardInterrupt, SystemExit):
        pass

def listLanguages():
    filterLang = lambda x : len(x) > 2
    filterUage = lambda x : len(x) == 2
    regexLangs = re.compile(r'<td>(.+?)</td>')

    try :
        request = requests.get("http://developer.simsimi.com/lclist").text
    except requests.exceptions.ConnectionError:
        print("[-] Make sure you've been connected to internet!")
        sys.exit(0)

    lang = list(filter(filterLang, regexLangs.findall(request)))
    uage = list(filter(filterUage, regexLangs.findall(request)))
    language = list(zip(uage,lang))

    for lang,uage in language: print(Fore.YELLOW + "%s : %s" % (lang,uage))
    sys.exit(0)

def usage():
    print(Fore.YELLOW + "[!] Usage   : ./chat.py <language>")
    print(Fore.YELLOW + "[!] Example : ./chat.py id")
    print(Fore.YELLOW + "[+] For list all languages type : ./chat.py lang")
    sys.exit(0)

print(Style.BRIGHT + Fore.GREEN + """
      _           _  _____ _           _
     (_)         (_)/ ____| |         | |
  ___ _ _ __ ___  _| |    | |__   __ _| |_
 / __| | '_ ` _ \| | |    | '_ \ / _` | __|
 \__ \ | | | | | | | |____| | | | (_| | |_
 |___/_|_| |_| |_|_|\_____|_| |_|\__,_|\__|
 """)

if not os.path.exists("key.txt"):
    print(Fore.RED+"[!] Get the key from http://developer.simsimi.com for use this tool!")
    print(Fore.RED+"[!] Save the key in key.txt")
    sys.exit(0)
elif len(sys.argv) != 2:
    usage()
else :
    if sys.argv[1] == "lang":
        listLanguages()
    else:
        simiChat = chat(sys.argv[1])

while True :
    try :
        message = input(Fore.WHITE + "From you\t : ")
        respons = simiChat.getChat(message)
    except (KeyboardInterrupt, SystemExit):
        print("\n[+] Exiting Program", end = "")
        loading()
        sys.exit(0)
    else:
        print(Fore.MAGENTA + "From simi\t : %s" % respons)
