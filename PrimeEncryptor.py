import sys
from Crypto.Cipher import AES
from Crypto.Cipher import ChaCha20
from Crypto.Cipher import ARC4
from Crypto.Util.Padding import pad
from os import urandom
import hashlib

def AESencrypt(text):
    key=urandom(16)
    k = hashlib.sha256(key).digest()  # Derive the AES key using SHA-256
    iv = urandom(16)  # Initialization vector (16 bytes, zeroed)
    text = pad(text, AES.block_size)  # Pad the plaintext
    cipher = AES.new(k, AES.MODE_CBC, iv)  # Create AES cipher in CBC mode
    ciphertext = cipher.encrypt(text)  # Encrypt the padded plaintext
    with open("AESCode.bin", "wb") as code_file:
        code_file.write(ciphertext)
    with open("AESKey.bin", "wb") as code_file:
        code_file.write(key)
    with open("AESiv.bin", "wb") as code_file:
        code_file.write(iv)       
         
    
    ciphertext=','.join(f'0x{byte:02x}' for byte in ciphertext)
    final_key=','.join(f'0x{byte:02x}' for byte in key)
    final_iv=','.join(f'0x{byte:02x}' for byte in iv)
    print(f'unsigned char key={{{final_key}}};')
    print(f'unsigned char iv={{{(final_iv)}}};')
    print(f'unsigned char ciphertext={{{ciphertext}}};')
    
    
        
    with open("resources.rc", "w") as f:
        f.write('AESCODE RCDATA "AESCode.bin"\n')
        f.write('AESKEY RCDATA "AESKey.bin"\n')
        f.write('AESIV RCDATA "AESiv.bin"\n')
        
    print(f'{GREEN}{BOLD}resources.rc, AESCode.bin, AESiv.bin and AESKey.bin has been created')
    print(f'TO COMPILE:\n"x86_64-w64-mingw32-windres resources.rc -O coff -o resources.res"\n"x86_64-w64-mingw32-g++ --static -o payload.exe AES.cpp resources.res -lws2_32 -lshlwapi -fpermissive"')

def ROT20encrypt(text):
    
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BOLD = "\033[1m"    
    ciphertext = bytearray()
    for i in text:
        ciphertext.append((i + 20) % 256)

    #print(ciphertext)

    formatted_ciphertext = ','.join(f'0x{byte:02x}' for byte in ciphertext)
    print(f'unsigned char ciphertext[] = {{{formatted_ciphertext}}};')
    with open("rot20.bin", "wb") as code_file:
        code_file.write(ciphertext)  # Write the bytearray directly (no need to convert)

    # Save resource script for .rc file
    with open("resources.rc", "w") as f:
        f.write('ROT20 RCDATA "rot20.bin"\n')
    print(f'{GREEN}{BOLD}resources.rc and rot20.bin has been created')
    print(f'TO COMPILE:\n"x86_64-w64-mingw32-windres resources.rc -O coff -o resources.res"\n"x86_64-w64-mingw32-g++ --static -o payload.exe rot20.cpp resources.res -lws2_32 -lshlwapi -fpermissive"')

def rc4encryption(text):
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BOLD = "\033[1m"
    key=urandom(16)
    cipher = ARC4.new(key)
    encrypted_shellcode = cipher.encrypt(text)
    ciphertext = bytes(encrypted_shellcode)  # Ensuring it's in bytes
    final_key = bytes(key) 
    with open("rc4code.bin", "wb") as code_file:
        code_file.write(ciphertext)
    with open("rc4key.bin", "wb") as code_file:
        code_file.write(final_key)  # Write the bytearray directly (no need to convert)
    ciphertext=','.join(f'0x{byte:02x}' for byte in encrypted_shellcode)
    final_key=','.join(f'0x{byte:02x}' for byte in key)
    print(f'unsigned char key={{{final_key}}};')
    print(f'unsigned char ciphertext={{{ciphertext}}};')
    
    # Save resource script for .rc file
    with open("resources.rc", "w") as f:
        f.write('RC4CODE RCDATA "rc4code.bin"\n')
        f.write('RC4KEY RCDATA "rc4key.bin"\n')
    print(f'{GREEN}{BOLD}resources.rc , rc4key.bin and rc4code.bin has been created')
    print(f'{GREEN}{BOLD}TO COMPILE:\n"x86_64-w64-mingw32-windres resources.rc -O coff -o resources.res"\n"x86_64-w64-mingw32-g++ --static -o payload.exe rc4.cpp resources.res -lws2_32 -lshlwapi -fpermissive"')
    

if __name__ == "__main__":

   WHITE = "\033[97m"
   RED = "\33[91m"
   RED = "\033[91m"
   GREEN = "\033[92m"
   YELLOW = "\033[93m"
   BOLD = "\033[1m"
   MAGENTA = "\033[35m"
   RESET = "\033[0m"

   banner=f"""
  {MAGENTA}{BOLD}
  
██████╗ ██████╗ ██╗███╗   ███╗███████╗    ███████╗███╗   ██╗ ██████╗██████╗ ██╗   ██╗██████╗ ████████╗ ██████╗ ██████╗ 
██╔══██╗██╔══██╗██║████╗ ████║██╔════╝    ██╔════╝████╗  ██║██╔════╝██╔══██╗╚██╗ ██╔╝██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗
██████╔╝██████╔╝██║██╔████╔██║█████╗      █████╗  ██╔██╗ ██║██║     ██████╔╝ ╚████╔╝ ██████╔╝   ██║   ██║   ██║██████╔╝
██╔═══╝ ██╔══██╗██║██║╚██╔╝██║██╔══╝      ██╔══╝  ██║╚██╗██║██║     ██╔══██╗  ╚██╔╝  ██╔═══╝    ██║   ██║   ██║██╔══██╗
██║     ██║  ██║██║██║ ╚═╝ ██║███████╗    ███████╗██║ ╚████║╚██████╗██║  ██║   ██║   ██║        ██║   ╚██████╔╝██║  ██║
╚═╝     ╚═╝  ╚═╝╚═╝╚═╝     ╚═╝╚══════╝    ╚══════╝╚═╝  ╚═══╝ ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚═╝        ╚═╝    ╚═════╝ ╚═╝  ╚═╝

{WHITE}{BOLD}................................................{RED}{BOLD} 
                      Encryptor function creator   
---------------------------------------------------------
{MAGENTA}{BOLD}Created by Dhanush Gowda(dagowda){RED}{BOLD}
---------------------------------------------------------
{WHITE}{BOLD}................................................{RED}{BOLD}                                                                                                                       
"""
        
   print(banner)
   if len(sys.argv) < 2:
    print("Usage: python3 prime_encryptor.py <filename>")
    exit()
   try:
     with open(sys.argv[1], "rb") as f:
        plaintext = f.read()
   except FileNotFoundError:
     print(f"Error: The file {sys.argv[1]} was not found.")
     exit()
   option=input(f'Please select the encryption type:\n1.)AES encryption\n2.)rot20\n3.)rc4 encryption\n>')
   if option=="1":
      AESencrypt(plaintext)
   elif option=="2":
      ROT20encrypt(plaintext)
   elif option=="3":
      rc4encryption(plaintext)
   
   else:
      print("invalid option")
   
   
