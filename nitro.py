import os
import time
import string
import ctypes
import numpy
import requests
from discord_webhook import DiscordWebhook, DiscordEmbed

# ANSI escape codes for text color
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
RESET = '\033[0m'

try:
    import requests
except ImportError:
    input(RED + "Module 'requests' not installed. Install it using 'pip install requests' and try again. Press Enter to exit." + RESET)
    exit()

try:
    import numpy
except ImportError:
    input(RED + "Module 'numpy' not installed. Install it using 'pip install numpy' and try again. Press Enter to exit." + RESET)
    exit()

def check_internet_connection():
    url = "https://xenx.vip"
    try:
        response = requests.get(url)
        print(GREEN + "Internet check" + RESET)
        time.sleep(.4)
    except requests.exceptions.ConnectionError:
        input(RED + "You are not connected to the internet. Check your connection and try again. Press Enter to exit." + RESET)
        exit()

def print_header():
    os.system('cls' if os.name == 'nt' else 'clear')
    if os.name == "nt":
        print("")
        ctypes.windll.kernel32.SetConsoleTitleW("SpEc-X Nitro Gen/Check")
    else:
        print(f'SpEc-X Nitro Gen/Check', end='', flush=True)

    print(GREEN + """
     _______..______    _______   ______      ___   ___ 
    /       ||   _  \  |   ____| /      |     \  \ /  / 
   |   (----`|  |_)  | |  |__   |  ,----' _____\  V  /  
    \   \    |   ___/  |   __|  |  |     |______>   <   
.----)   |   |  |      |  |____ |  `----.      /  .  \  
|_______/    | _|      |_______| \______|     /__/ \__\ 

""" + RESET)

class NitroGen:
    def __init__(self):
        self.fileName = "Nitro Codes.txt"

    def main(self):
        global USE_WEBHOOK  # Declare USE_WEBHOOK as a global variable
        print_header()

        self.slowType(GREEN + "Made by: SpEc012 - " + YELLOW + "https://xenx.vip" + RESET, 0.02)
        time.sleep(1)
        
        # Ask for the Discord webhook URL
        webhook = input("\nIf you want to use a Discord webhook, type it here or press Enter to ignore: ")
            
        if webhook != "":
            USE_WEBHOOK = True
            discord_webhook = DiscordWebhook(url=webhook)
            embed = DiscordEmbed(title="Nitro Generator and Checker", description="Started checking URLs. Coded by SpEc012.\n\n**Results will be displayed here.**", color=0x00ff00)
            # You can include an image in the description using Markdown syntax:
            embed.description = "Started checking URLs. Coded by SpEc012.\n\n**Results will be displayed here.**\n\n![Boost-Discord](https://media.tenor.com/-iJ1olfz7qsAAAAC/boost-discord.gif)"
            discord_webhook.add_embed(embed)
            discord_webhook.execute()

        self.slowType("\nInput How Many Codes to Generate and Check: ", .02, newLine=False)

        try:
            num = int(input(''))
        except ValueError:
            input(RED + "Specified input wasn't a number. Press Enter to exit" + RESET)
            exit()

        valid = []
        invalid = 0
        chars = []
        chars[:0] = string.ascii_letters + string.digits

        c = numpy.random.choice(chars, size=[num, 16])
        for s in c:
            try:
                code = ''.join(x for x in s)
                url = f"https://discord.gift/{code}"

                result = self.quickChecker(url)

                if result:
                    valid.append(url)
                else:
                    invalid += 1
            except KeyboardInterrupt:
                print("\nInterrupted by user")
                break

            except Exception as e:
                print(RED + f" Error | {url}" + RESET)

            if os.name == "nt":
                ctypes.windll.kernel32.SetConsoleTitleW(
                    f"{GREEN}Nitro Generator and Checker - {len(valid)} Valid | {invalid} Invalid - Made by SpEc012, Good Luck!" + RESET)
                print("")
            else:
                print(
                    f'\33]0;Nitro Generator and Checker - {len(valid)} Valid | {invalid} Invalid - Made by SpEc012, Good Luck!\a', end='', flush=True)

        print(f"""
Results:
 {GREEN}Valid: {len(valid)}{RESET}
 {RED}Invalid: {invalid}{RESET}
 {GREEN}Valid Codes: {', '.join(valid)}{RESET}""")

        if USE_WEBHOOK:
            self.post_results(valid, invalid, webhook)

        input(GREEN + "\nThe end! Press Enter 5 times to close the program." + RESET)
        [input(i) for i in range(4, 0, -1)]

    def post_results(self, valid, invalid, webhook):
        if USE_WEBHOOK:
            discord_webhook = DiscordWebhook(url=webhook)
            embed = DiscordEmbed(title="Nitro Generator and Checker Results", color=0xff0000)
            embed.add_embed_field(name="Valid", value=str(len(valid)), inline=True)
            embed.add_embed_field(name="Invalid", value=str(invalid), inline=True)
            embed.add_embed_field(name="Valid Codes", value=', '.join(valid), inline=False)
            # You can include an image in the description using Markdown syntax:
            embed.description = "Started checking URLs. Coded by SpEc012.\n\n**Results will be displayed here.**\n\n![Boost-Discord](https://media.tenor.com/-iJ1olfz7qsAAAAC/boost-discord.gif)"
            discord_webhook.add_embed(embed)
            discord_webhook.execute()

    def slowType(self, text: str, speed: float, newLine=True):
        for i in text:
            print(i, end="", flush=True)
            time.sleep(speed)
        if newLine:
            print()

    def quickChecker(self, nitro:str, notify=None):
        url = f"https://discordapp.com/api/v9/entitlements/gift-codes/{nitro}?with_application=false&with_subscription_plan=true"
        response = requests.get(url)

        if response.status_code == 200:
            print(f" {GREEN}Valid | {nitro} {RESET}", flush=True,
                  end="" if os.name == 'nt' else "\n")
            with open("Nitro Codes.txt", "w") as file:
                file.write(nitro)

            if notify is not None:
                discord_webhook = DiscordWebhook(url=notify)
                embed = DiscordEmbed(title="Valid Nitro Code Detected!", color=0x00ff00)
                embed.add_embed_field(name="Code", value=nitro, inline=False)
                discord_webhook.add_embed(embed)
                discord_webhook.execute()

            return True

        else:
            print(f" {RED}Invalid | {nitro} {RESET}", flush=True,
                  end="" if os.name == 'nt' else "\n")
            return False

if __name__ == '__main__':
    Gen = NitroGen()
    Gen.main()

