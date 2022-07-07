[![CodeQL](https://github.com/Tony177/UninaDownloader/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/Tony177/UninaDownloader/actions/workflows/codeql-analysis.yml) [![Pytest](https://github.com/Tony177/UninaDownloader/actions/workflows/pytest.yml/badge.svg)](https://github.com/Tony177/UninaDownloader/actions/workflows/pytest.yml)
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

## Testing
It's possible to test the program using ```pytest``` in the main directory.
- Every passed test is represented as a dot <b>.</b>
- Every failed test is represented as an <b>F</b>
- Every test with exception error is represented as an <b>E</b>

## Future Implementation
- Saving only some choosen files or directory instead of all files :o:
- <s>Refractore code for readability and isolation </s> DONE! :heavy_check_mark: 
- Better error and exception handling, such as: 
    - Remote access permission error :o:
    - <s>Credentials error </s> DONE! :heavy_check_mark:
    - Local folder permission error :o:
- Auto restart code :o:
- Terminal inline parsing :o:
- View not accessible folder (don't have enought permissions) :o:
## Cryptography

Using the <b><i>Fernet Cryptography Module</b></i>, the credentials file is encrypted/decrypted using the <i><b>secret.key</b></i> and the <i><b>crypt.py</b></i> module.\
Upon generating a key it can be used to encrypt (encrypt function) and to decrypt (decrypt function)
