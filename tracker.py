import requests
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
from datetime import datetime
import os
from colorama import Fore, Style, init

init(autoreset=True)

LOG_FILE = "tracker_logs.txt"

def log_data(data):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] {data}\n")

def clear_logs():
    if os.path.exists(LOG_FILE):
        open(LOG_FILE, "w").close()
        print(Fore.GREEN + "\n[✔] Logs cleared successfully!\n")
    else:
        print(Fore.RED + "\n[!] No log file found.\n")

# ------------------- OWN IP ------------------- #
def own_ip_menu():
    while True:
        ip = requests.get("https://api64.ipify.org?format=json").json()["ip"]
        print(Fore.GREEN + f"\n[+] Your Public IP: {ip}\n")
        log_data(f"Checked Own IP → {ip}")

        choice = input(Fore.RED + "[1] Refresh  [2] Back → " + Style.RESET_ALL)
        if choice == "2":
            break

# ------------------- TRACK IP ------------------- #
def track_ip():
    while True:
        ip = input(Fore.RED + "\nEnter IP to track (or type 'back' to return): " + Style.RESET_ALL)
        if ip.lower() == "back":
            break

        url = f"http://ip-api.com/json/{ip}?fields=66846719"
        response = requests.get(url).json()

        if response["status"] == "success":
            details = f"""
{Fore.GREEN}IP: {response['query']}
ISP: {response['isp']}
Org: {response['org']}
Continent: {response['continent']}
Country: {response['country']} ({response['countryCode']})
Region: {response['regionName']}
City: {response['city']}
Zip: {response['zip']}
Timezone: {response['timezone']}
Lat/Lon: {response['lat']}, {response['lon']}
Map: https://www.google.com/maps?q={response['lat']},{response['lon']}
Currency: {response.get('currency', 'N/A')}
Languages: {response.get('languages', 'N/A')}
"""
            print(details)
            log_data(f"Tracked IP → {ip} → {details}")
        else:
            print(Fore.RED + "[!] Could not track IP\n")

# ------------------- PHONE TRACKER ------------------- #
def phone_tracker():
    while True:
        number = input(Fore.RED + "\nEnter phone number (with country code) or type 'back': " + Style.RESET_ALL)
        if number.lower() == "back":
            break

        try:
            parsed = phonenumbers.parse(number)
            info = f"""
{Fore.GREEN}Number: {number}
Valid: {phonenumbers.is_valid_number(parsed)}
Possible: {phonenumbers.is_possible_number(parsed)}
Region: {geocoder.description_for_number(parsed, "en")}
Carrier: {carrier.name_for_number(parsed, "en")}
Timezone: {timezone.time_zones_for_number(parsed)}
"""
            print(info)
            log_data(f"Tracked Phone → {number} → {info}")
        except Exception as e:
            print(Fore.RED + f"[!] Error: {e}\n")

# ------------------- USERNAME RECON ------------------- #
def username_recon():
    while True:
        username = input(Fore.RED + "\nEnter username (or type 'back'): " + Style.RESET_ALL)
        if username.lower() == "back":
            break

        sites = [
            f"https://facebook.com/{username}",
            f"https://twitter.com/{username}",
            f"https://instagram.com/{username}",
            f"https://github.com/{username}",
            f"https://t.me/{username}",
            f"https://www.reddit.com/user/{username}",
            f"https://www.pinterest.com/{username}"
        ]
        print(Fore.GREEN + "\n[+] Possible profiles:")
        for site in sites:
            print(Fore.GREEN + " -> " + site)
        log_data(f"Username Recon → {username}")

# ------------------- MAIN MENU ------------------- #
def menu():
    while True:
        print(Fore.RED + """
╔════════════════════════════════════════════════════════════════════════════════════════════╗
    
██╗░░░██╗░█████╗░██████╗░████████╗███████╗██╗░░██╗░█████╗░██████╗░██╗░░░██╗██████╗░██╗░░██╗
██║░░░██║██╔══██╗██╔══██╗╚══██╔══╝██╔════╝╚██╗██╔╝██╔══██╗██╔══██╗╚██╗░██╔╝██╔══██╗╚██╗██╔╝
╚██╗░██╔╝██║░░██║██████╔╝░░░██║░░░█████╗░░░╚███╔╝░██║░░╚═╝██████╔╝░╚████╔╝░██████╔╝░╚███╔╝░
░╚████╔╝░██║░░██║██╔══██╗░░░██║░░░██╔══╝░░░██╔██╗░██║░░██╗██╔══██╗░░╚██╔╝░░██╔═══╝░░██╔██╗░
░░╚██╔╝░░╚█████╔╝██║░░██║░░░██║░░░███████╗██╔╝╚██╗╚█████╔╝██║░░██║░░░██║░░░██║░░░░░██╔╝╚██╗
░░░╚═╝░░░░╚════╝░╚═╝░░╚═╝░░░╚═╝░░░╚══════╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝░░░╚═╝░░░╚═╝░░░░░╚═╝░░╚═╝
              
            Made By : @vortexeditor || discord : https://discord.gg/e9tgXpDuhT
                          ~ Publisher : Team CrypX
╚═════════════════════════════════════════════════════════════════════════════════════════════╝
""" + Fore.GREEN + """
    [1] Own IP
    [2] Track IP
    [3] Phone Number Tracker
    [4] Username Tracker
    [5] Exit
    [6] Clear Logs
""" + Style.RESET_ALL)

        choice = input(Fore.RED + "Choose option: " + Style.RESET_ALL)

        if choice == "1":
            own_ip_menu()
        elif choice == "2":
            track_ip()
        elif choice == "3":
            phone_tracker()
        elif choice == "4":
            username_recon()
        elif choice == "5":
            print(Fore.RED + "Exiting...")
            break
        elif choice == "6":
            clear_logs()
        else:
            print(Fore.RED + "Invalid option!\n")

if __name__ == "__main__":
    menu()
