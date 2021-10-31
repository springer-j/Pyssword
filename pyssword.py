import random as r
from MyJson import MyJson
from datetime import datetime, date
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
        self.key_length = 13
        #* Profile Information
        self.id = 0
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
        self.update_stale_state()

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
        new_key = ''
        for i in range(0,self.key_length):
            new_key += r.choice(self.usable_chars)
        self.key = new_key
        return new_key

    
    def create_profile(self):
        #* Compile user data into dictionary and update self.key_data
        if self.all_profiles:
            self.id = self.all_profiles[-1]["id"] + 1
        else:
            self.id = 1
        key_data = {
            "id":self.id,
            "site_name":self.site_name,
            "key":self.generate_password(),
            "username":self.username,
            "email":self.email,
            "is_chain":self.is_chain,
            "created":self.created,
            "last_touched":self.created,
            "stale_time":self.stale_time,
            "is_stale":False,
        }
   
        self.all_profiles.append(key_data)

#############################################
#* Calculating is_stale

    def get_date_object(self,date_string):
        month = date_string[0:2]
        day = date_string[3:5]
        year = '20' + date_string[6:]
        return date(int(year),int(month),int(day))
    
    
    def calculate_date_since(self,password_date):
        now = date.today()
        last_altered = self.get_date_object(password_date)
        delta = now - last_altered 
        return delta.days
    
    
    def update_stale_state(self):
        for profile in self.all_profiles:
            days_since = self.calculate_date_since(profile["last_touched"])
            profile["is_stale"] = days_since > profile["stale_time"]

############################################
#* Edit account information 

    def update_password(self,id):
        now = datetime.now()
        new_password = self.generate_password()
        for user in self.all_profiles:
            if user["id"] == id: # Find user in list by ID key.
                user["key"] = new_password # Assign new password 
                user["last_touched"] = now.strftime("%m/%d/%y") # Update "last touched"
                user["is_stale"] = False # Ensure is_stale is False 


    def delete_account(self, id):
        for user in self.all_profiles:
            if user["id"] == id:
                self.all_profiles.remove(user)
                break
        
       
############################################
#* Encryption functions
# Fernet guide: https://devqa.io/encrypt-decrypt-data-python/

    def generate_crypt_key(self):
        #* Generate the crypt key and assign to obj attr.
        self.crypt_key = Fernet.generate_key()


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
        # Parse through each profile and alter data.
        for account in self.all_profiles:
            account["site_name"] = self.encrypt(account["site_name"])
            account["key"] = self.encrypt(account["key"])
            account["username"] = self.encrypt(account["username"])
            account["email"] = self.encrypt(account["email"])
        
        # Save JSON file with encrypted data.
        myjson.save_json(self.all_profiles)
        
    
    def unlock(self):
        #* Decrypt all data in keylog file.
        file = open(self.key_file,'rb')
        data = json.load(file)
        file.close()
        # Parse through each profile and alter data.
        for account in data:
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
        # try:
        self.unlock()
        # except: 
        #     sys.tracebacklimit = 0
        #     print('[X] Incorrect key.')
        #     sys.exit()  


    def mayday(self):
        #* Overwrite password file.
        file = open(self.key_file,'w')
        for i in range(0,1000):
            file.write('can i keep you ' * 1000)
            file.write('\n')
        file.close()
        print('can i keep you?')
    
