import random as r
from MyJson import MyJson
from datetime import datetime
from cryptography.fernet import Fernet
import sys 
import json

class Pyssword:
    def __init__(self, crypt_key):
        #* File locations 
        self.crypt_key = 'resource_files/secret.key'
        self.data_file = 'resource_files/data.json'
        self.key_file = 'resource_files/passes.json'
        #* Usable chars for key
        self.chars = []
        self.specials = []
        self.nums = []
        self.usable_chars = []
        #* Key options 
        self.use_specials = True 
        self.key_length = 10 
        #* Profile Information
        self.site_name = ''
        self.key = ''
        self.username = None 
        self.email = None 
        self.is_chain = False 
        self.created = None 
        self.stale_time = 30 
        self.key_data = {}
        #* Encryption Information 
        self.crypt_key = crypt_key
        self.all_profiles = []
        #* Init functions
        self.verify_user()
        self.load_chars()


##############################################
#* Generate and organize password information.

    def load_chars(self):
        #* Load characters from JSON file 
        # Open JSON and get all lists
        json = MyJson.MyJson(self.data_file)
        data = json.read("data_bank") 
        all_chars = data["all_chars"]
        imported_chars = all_chars["chars"]
        imported_nums = all_chars["nums"]
        imported_specials = all_chars["specials"]
        # Parse each list and add it to self.usable_chars
        for char in imported_chars:
            self.usable_chars.append(char)
            self.usable_chars.append(char.upper())
        for num in imported_nums:
            self.usable_chars.append(num)
        if self.use_specials:
            for spec in imported_specials:
                self.usable_chars.append(spec)
        
        return True

        
    def generate_password(self):
        #* Generate and return password based on object attributes.
        for i in range(0,self.key_length):
            self.key += r.choice(self.usable_chars)
        return True

    
    def create_profile(self):
        #* Compile user data into dictionary and update self.key_data
        key_data = {
            "site_name":self.site_name,
            "key":self.key,
            "username":self.username,
            "email":self.email,
            "is_chain":self.is_chain,
            "created":self.created,
            "last_touched":None,
            "stale_time":self.stale_time,
            "is_stale":False,
        }
   
        self.key_data = key_data

    
    def save_profile(self):
        #* Update JSON dict and save file.
        key_json = MyJson.MyJson(self.key_file)
        data = key_json.read()
        data["keys"].append(self.key_data)
        key_json.save_json(data)
        return True

    
    def log_key(self):
        #* Chain functions to save new profile to the JSON dict. 
        self.generate_password()
        self.create_profile()
        self.save_profile()

#############################################
#* Encryption functions
# Fernet guide: https://devqa.io/encrypt-decrypt-data-python/

    def generate_crypt_key(self):
        #* Generate the crypt key
        key = Fernet.generate_key()
        with open("secret.key",'wb') as key_file:
            key_file.write(key)


    def encrypt(self,text):
        #* Encrypts and returns text
        encoded = text.encode()
        f = Fernet(self.crypt_key)
        encrypted = f.encrypt(encoded)
        
        return str(encrypted)


    def decrypt(self,text):
        # Decrypt and return text
        f = Fernet(self.crypt_key)
        dec = f.decrypt(text.encode())
        return str(dec.decode())
        

    def lock(self):
        # *Encrypt all data in keylog file.
        myjson = MyJson.MyJson(self.key_file)
        myjson.verbose = False
        data = myjson.read()
        # Parse through each profile and alter data.
        for account in data['keys']:
            account["site_name"] = self.encrypt(account["site_name"])
            account["key"] = self.encrypt(account["key"])
            account["username"] = self.encrypt(account["username"])
            account["email"] = self.encrypt(account["email"])
        
        # Save JSON file with encrypted data.
        myjson.save_json(data)
        
    
    def unlock(self):
        #* Decrypt all data in keylog file.
        file = open(self.key_file,'rb')
        data = json.load(file)
        file.close()
        # Parse through each profile and alter data.
        for account in data['keys']:
            account["site_name"] = self.decrypt(account["site_name"][2:])
            account["key"] = self.decrypt(account["key"][2:])
            account["username"] = self.decrypt(account["username"][2:])
            account["email"] = self.decrypt(account["email"][2:])
            
            # Append unlocked profile to obj list
            # Better than saving to drive.
            self.all_profiles.append(account)

        # # Save JSON file with encrypted data.
        # new_file = open(self.key_file,'w')
        # new_data = json.dumps(data,indent=4)
        # new_file.write(new_data)
        # new_file.close()
        
        
############################################
#* Verification functions 

    def verify_user(self): 
        try:
            self.unlock()
        except: 
            sys.tracebacklimit = 0
            print('[X] Incorrect key.')
            sys.exit()  

    def mayday(self):
        #* Overwrite password file.
        file = open(self.key_file,'w')
        for i in range(0,1000):
            file.write('can i keep you ' * 1000)
            file.write('\n')
        file.close()
        print('can i keep you?')
    
    

    
    
    