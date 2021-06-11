import platform
import sys
import colorama
from colorama import Back, Fore
import os

colorama.init(autoreset=True)

sure = input(f"{Fore.RED}this script will never allow you to access the discord site\nagain and will delete all discord files,\nare you sure you want to open it? [Y/n] >")

platforms = {"Linux": '/etc/hosts', "Windows": r"C:\Windows\System32\drivers\etc\hosts"}

try:
    choose = platforms[platform.system()]
except:
    sys.exit()

if "n" in sure.lower():
    sys.exit()

def block(websites):
    with open(choose, 'r+') as hostfile:
        hosts = hostfile.read()
        for site in  websites:
            if site not in hosts:
               hostfile.write("127.0.0.1 "+site+'\n')

websites = ['www.discord.com', 'discord.com']
block(websites)

if platform.system() == "Windows":
    os.chdir("C:\\Users\\filip\\AppData\\Local\\Discord\\")
    for file in os.listdir():
        try:
            os.remove(file)
        except:
            try:
                os.rmdir(file)
            except:
                pass
    for file in os.listdir():
        if file.startswith("app-"):
            os.chdir(file)
            for file in os.listdir():
                try:
                    os.remove(file)
                except:
                    pass
    os.chdir("C:\\Users\\filip\\AppData\\Local\\\DiscordPTB\\")
    for file in os.listdir():
        try:
            os.remove(file)
        except:
            try:
                os.rmdir(file)
            except:
                pass
    for file in os.listdir():
        if file.startswith("app-"):
            os.chdir(file)
            for file in os.listdir():
                try:
                    os.remove(file)
                except:
                    pass
    os.chdir("C:\\Users\\filip\\AppData\\Local\\DiscordDevelopment")
    for file in os.listdir():
        try:
            os.remove(file)
        except:
            try:
                os.rmdir(file)
            except:
                pass
    for file in os.listdir():
        if file.startswith("app-"):
            os.chdir(file)
            for file in os.listdir():
                try:
                    os.remove(file)
                except:
                    pass
