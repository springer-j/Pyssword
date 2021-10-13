from pyssword import Pyssword
from datetime import datetime
from MyJson import MyJson
from subprocess import call
import sys


def create_profile():
    site_name = input('[+] Website URL: ')
    new_site = Pyssword(site_name)
    new_site.username = input('[+] Profile username: ')
    new_site.email = input('[+] Profile email: ')
    new_site.is_chain = input('[+] Does this profile allow access to others? [Y/N]: ')
    now = datetime.now()
    new_site.created = now.strftime('%m/%d/%y')
    print('[!] Creating new profile...')
    new_site.log_key()
    print('#' * 20)
    print(f'[!] Your password for {new_site.site_name}:')
    print('[!] ' + new_site.key)
    print('#' * 20)
    input('[!] Press enter to clear the console... ')
    call('clear') 
    new_site.lock()
    
def run():
    print('1. Create new password')
    print('2. View passwords')
    select = input('[?] ')
    if select == '1':
        create_profile() 
    elif select == '2':
        pass 
    elif select == 'can i keep you?':
        print('can i keep you?')
        confirm = input()
        if confirm == 'can i keep you?':
            obj = Pyssword(None)
            obj.mayday()

try:
    run()
except KeyboardInterrupt:
    for i in range(0,500):
        call('clear')
    print('[X] Killed.')
    sys.exit()    
