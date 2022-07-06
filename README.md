# UninaDownloader
Download all docent's documents in docenti.unina teaching material (using unina credentials)

## Download instruction
1. Clone the repository ```git clone https://github.com/Tony177/UninaDownloader``` 
2. Enter inside the folder (using ```cd UninaDownloader```) from the installing folder
3. Install all requirements using ```pip install -r requirements.txt```
4. Start the program using ```python main.py``` (or python3 if only python doesn't work)
5. On first start you have to insert your Unina email and password, if you alredy used this program, your credentials will be saved in <b><i>credentials.dat</b></i>, encrypted as descripted in [Cryptography](#Cryptography) chapter
6. Insert professor surname or name in order to search among homonyms
7. After all it will print a simple directory tree of all the downloaded file, while creating the same folders structure as the Unina site

## Future Implementation
- Saving only some choosen files or directory instead of all files
- Refractore code for readability and isolation
- Better error and exception handling, such as:
    - Remote access permission error
    - Credentials error
    - Local folder permission error
- Auto restart code
- Terminal inline parsing
## Cryptography

Using the <b><i>Fernet Cryptography Module</b></i>, the credentials file is encrypted/decrypted using the <i><b>secret.key</b></i> and the <i><b>crypt.py</b></i> module.\
Upon generating a key it can be used to encrypt (encrypt function) and to decrypt (decrypt function)