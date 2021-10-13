from pyssword import Pyssword
from datetime import datetime
from MyJson import MyJson
from subprocess import call
import sys

def clear_screen():
    for i in range(0,500):
        call('clear')   


def create_profile():
    # Create Pyssword obj and collect attributes.
    pyss.site_name = input('[+] Website URL: ')
    pyss.username = input('[+] Profile username: ')
    pyss.email = input('[+] Profile email: ')
    pyss.is_chain = input('[+] Does this profile allow access to others? [Y/N]: ')
    now = datetime.now()
    pyss.created = now.strftime('%m/%d/%y')
    print('[!] Creating new profile...')
    # Generate password
    pyss.create_profile()
    print('#' * 20)
    # Display password
    print(f'[!] Your password for {pyss.site_name}:')
    print('[!] ' + pyss.key)
    print('#' * 20)
    input('[!] Press enter to clear the console... ')
    call('clear') 
    pyss.lock()


def view_profiles(): 
    for x in pyss.all_profiles:
        print('////////////PYSSWORD////////////')
        print(f'[*] URL: {x["site_name"]}')
        if x["username"]:
            print(f'[*] Username: {x["username"]}')
        if x["email"]:
            print(f'[*] Email: {x["email"]}')  
        print(f'[*] Password: {x["key"]}')
        print(f'[*] Profile created: {x["created"]}')
        print(f'[*] Last altered: {x["last_touched"]}')
        if x["is_stale"]:
            print('[!] Password reset recommended.')
            
        if x["is_chain"] == 'y':
            print('[!] This site could give access to others.')
    print('////////////PYSSWORD////////////')
    input('[X] Press enter to clear the screen... \n')
    clear_screen()
    
        
        
        
       


def run():
    print('1. Create new password')
    print('2. View passwords')
    select = input('[?] ')
    if select == '1':
        create_profile() 
    elif select == '2':
        view_profiles()
  

try:
    key_try = input('[!] Enter the key: ')
    pyss = Pyssword(key_try)
    run()
except KeyboardInterrupt:
    clear_screen()
    print('[X] Killed.')
    sys.exit()    
