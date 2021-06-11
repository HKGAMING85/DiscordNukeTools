import platform, sys


platforms = {"Linux": '/etc/hosts', "Windows": r"C:\Windows\System32\drivers\etc\hosts"}

try:
    choose = platforms[platform.system()]
except:
    sys.exit()


def unblock(websites):
    with open(choose, 'r+') as hostfile:
        hosts = hostfile.readlines()
        hostfile.seek(0)
        for host in hosts:
            if not any(site in host for site in websites):
                hostfile.write(host)
        hostfile.truncate()

websites = [
    'www.discord.com',  'discord.com',  
]

unblock(websites)
