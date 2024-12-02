import requests
import random
import string
import time

# Constants
NAMES = 10  # Amount of usernames to save
LENGTH = 5  # Length of usernames
FILE = 'valid.txt'  # Automatically creates file
BIRTHDAY = '1999-04-20'  # User's birthday for validation

# Color formatting for terminal output
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    GRAY = '\033[90m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def success(username):
    print(f"{bcolors.OKBLUE}[{found}/{NAMES}] [+] Found Username: {username} {bcolors.ENDC}")
    with open(FILE, 'a+') as f:
        f.write(f"{username}\n")

def taken(username):
    print(f'{bcolors.FAIL}[-] {username} is taken {bcolors.ENDC}')

def make_username(length):
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

def check_username(username):
    url = f'https://auth.roblox.com/v1/usernames/validate?request.username={username}&request.birthday={BIRTHDAY}'
    response = requests.get(url, timeout=5)  # Set a timeout of 5 seconds
    response.raise_for_status()  # Raise an error for bad responses
    return response.json().get('code')

# Check usernames loop
found = 0
while found < NAMES:
    try:
        username = make_username(LENGTH)
        code = check_username(username)
        
        if code == 0:
            found += 1
            success(username)
        else:
            taken(username)
                
    except requests.exceptions.RequestException as e:
        print('Network error:', e)
    except KeyboardInterrupt:
        print("Script interrupted. Exiting...")
        break
    except Exception as e:
        print('Error:', e)

    time.sleep(0.1)  # Increased sleep time to avoid overwhelming the API

print(f"{bcolors.OKBLUE}[!] Finished {bcolors.ENDC}")
