from pyssword import Pyssword
from datetime import datetime
from MyJson import MyJson
from subprocess import call
import sys


##############################################
#* /// UI FUNCTIONS ///

def clear_screen():
    #* Push all print statements out of the terminal.
    for i in range(0,100):
        call('clear')   
    print(' /// Pyssword ///\n')

##############################################
#* /// CREATE PROFILE ///

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


##############################################
#* /// VIEW AND SELECT PROFILES ///

def display_menu():
    clear_screen()
    print('1. Search by ID')
    print('2. Search by field')
    print('3. View all')
    select = input('[?] ')
    if select == '1':
        alter_profile() 
    elif select == '2':
        search_profiles() 
    elif select == '3':
        view_all()


def display_profile(x): 
    #* Display dict data 
    #! Rename x variable cmon now
    print('////////////PYSSWORD////////////')
    print(f'[*] Profile ID: {x["id"]}' )
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


def view_all():
    for user in pyss.all_profiles:
        display_profile(user)
    input('[X] Press enter to clear the screen... \n')
    clear_screen()


def gather(key,value=None):
    #* Used within search_profiles() to gather profiles where 
    #* the desired value matches the category given.
    found = []   
    if not value: # Take value from user when a bool isn't supplied
        value = input('[?] Search value: ')
    # Parse all profiles and add the dict when a match is found
    for user in pyss.all_profiles:
        if user[key] == value:
            found.append(user)
    return found # Return dict of all found profiles


def search_profiles():
    #* Allow user to choose a attr to search
    print('1. URL')
    print('2. Username')
    print('3. Email')
    print('4. Stale')
    print('5. Chain')
    select = input('[?] Attribute to search: ')
    if select == '1':
        found = gather('site_name')
    elif select == '2':
        found = gather('username')
    elif select == '3':
        found = gather('email')
    elif select == '4':
        found = gather("is_stale",True)
    elif select == '5':
        found = gather("is_chain",'y')
    if found: # Display profiles if any were found 
        for user in found:
            display_profile(user)
    else: # Display a message when no matches. 
        print('[X] No profiles found with those parameters.')

#############################################
#* /// ALTER PROFILE VALUES

def select_profile():
    user_id = input('[*] Enter the profile ID: ')
    for user in pyss.all_profiles:
        if user["id"] == int(user_id):
            return user
    raise ValueError('[X] Could not find a profile with that ID.')
    

def alter_profile():
    #* Edit, reset and delete profile information
    profile = select_profile()
    display_profile(profile)
    print('1. Reset password 2. Edit Account 3. Delete Account')
    selection = input('[?] ')
    if selection == '1':
        pyss.update_password(profile["id"])
        print('[!] Password has been reset!')
        input('[!] Press enter to continue...')
        display_profile(profile)
        input('[X] ')
        end()
    elif selection == '2':
        pass
    elif selection == '3':
        pyss.delete_account(profile["id"])
        print(f'[X] Account deleted.')
        input('[!] Press enter to continue...')
        end()
   
#############################################
#* /// CONFIGURATION FUNCTIONS ///

def settings_menu():
    clear_screen()
    print('/// Pyssword Settings ///')
    print('1. Reset crypt key')
    
    select = input('[?] ')
    
    if select == '1':
        reset_crypt_key()


def reset_crypt_key():
    clear_screen()
    print('[!] WARNING:')
    print('[!] Once the key is reset, it cannot be undone.')
    print('[!] The key will be displayed only once, if you lose it, it\'s gone.')
    print('[!] Enter "Pyssword Reset" to continue.')
    print('[!] Enter anything else to cancel.')
    confirm = input('[!] ')
    if confirm == 'Pyssword Reset':
        clear_screen()
        print('[!] Generating passkey...')
        pyss.generate_crypt_key()
        print('[!] New crypt key:')
        print(f'///  {str(pyss.crypt_key)}  /// ')
        input('[!] Press enter to exit.') 
             
        
    else:
        print('[X] Process cancelled.')
        input('[X] Press enter to continue.')
        
    end()
     
##############################################
#* /// START/STOP FUNCTIONS ///

def end():
    pyss.lock()
    clear_screen()
    print('[!] Log updated.')
    print('[!] Pyssword terminated.')
    sys.exit()


def run():
    print('1. Create new password')
    print('2. View passwords')
    print('3. Settings')
    select = input('[?] ')
    clear_screen()
    if select == '1':
        create_profile() 
    elif select == '2':
        display_menu()
    elif select == '3':
        settings_menu()
    end()
        
##############################################
#* /// RUN FUNCTIONS ///

try:
    key_try = input('[!] Enter the key: ')
    clear_screen()
    pyss = Pyssword(key_try)
    run()
except KeyboardInterrupt:
    clear_screen()
    print('[X] Killed.')
    sys.exit()    
