from pyfiglet import figlet_format
from pystyle import Write, Colors
from datetime import datetime


def caesarCipherEncryption(plainText: str, key: int) -> str:
    cipherText = ""
    for i in range(len(plainText)):
        char: str = plainText[i]
        if char.islower():
            cipherText += chr((ord(char) - ord("a") + key) % 26 + ord("a"))
        elif char.isupper():
            cipherText += chr((ord(char) - ord("A") + key) % 26 + ord("A"))
        else:
            cipherText += char
    return cipherText


def caesarCipherDecryption(plainText: str, key: int) -> str:
    cipherText = ""
    for i in range(len(plainText)):
        char: str = plainText[i]
        if char.islower():
            cipherText += chr((ord(char) - ord("a") - key) % 26 + ord("a"))
        elif char.isupper():
            cipherText += chr((ord(char) - ord("A") - key) % 26 + ord("A"))
        else:
            cipherText += char
    return cipherText


def vigenereCipherEncrypt(plainText: str, key: str) -> str:
    cipherText = ""
    keyCapital: str = key.upper()
    keySmall: str = key.lower()
    for i in range(len(plainText)):
        if plainText[i].islower():
            ch = keySmall[i % len(key)]
        else:
            ch = keyCapital[i % len(key)]
        cipherText += caesarCipherEncryption(plainText[i], ord(ch))
    return cipherText


def vigenereCipherDecrypt(plainText: str, key: str) -> str:
    cipherText = ""
    keyCapital: str = key.upper()
    keySmall: str = key.lower()
    for i in range(len(plainText)):
        if plainText[i].islower():
            ch = keySmall[i % len(key)]
        else:
            ch = keyCapital[
                i % len(key)
            ]  # if key size less than msg size we take mod to decrypt all msg
        cipherText += caesarCipherDecryption(plainText[i], ord(ch))  # shift it 1 time
    return cipherText


def fence(lst, numrails):
    fence = [
        [None] * len(lst) for n in range(numrails)
    ]  # matrix with row=length of text and col=key
    rails = list(range(numrails - 1)) + list(
        range(numrails - 1, 0, -1)
    )  # list of all indexes from right + list from all indexes from left
    for n, x in enumerate(lst):
        fence[rails[n % len(rails)]][
            n
        ] = x  # store all indexes to encrypt/decrypte in matrix
    return [
        c for rail in fence for c in rail if c is not None
    ]  # retrun list of keys in matrix if we passing decryption else cipherText


def railFenceEncrypt(text, n):
    return "".join(fence(text, n))


def railFenceDecrypt(text, n):
    rng = range(len(text))
    pos = fence(rng, n)
    return "".join(text[pos.index(n)] for n in rng)


def xorCipher(message: str, key: str) -> str:
    text = ""
    for i in range(len(message)):
        if message[i] != " ":
            text += chr(ord(message[i]) ^ ord(key[i % len(key)]))
        else:
            text += " "
    return text


date = str(datetime.now())
date = date[: date.find(".")]
Write.Print(text=figlet_format("Crypto System"), color=Colors.red_to_blue, interval=0.1)
Write.Print(text=f"[*] Start At {date}\n", color=Colors.green_to_blue, interval=0.1)
nameFile = Write.Input(
    text="Enter Absolute Path To your File : ", color=Colors.green_to_blue, interval=0.1
)
try:
    with open(nameFile, "r") as f:
        data = f.read()
except FileNotFoundError as fe:
    Write.Print("Try With Exist File\n")
    exit(0)
mode = Write.Input(
    "For Encryption Enter e For Decryption Enter d : ",
    Colors.green_to_blue,
    interval=0.1,
)
mode = mode.lower()
stages = ["Caesar", "xorCipher", "Vigener", "RailFence"]
keys = list()
for i in stages:
    key = Write.Input(
        f"Enter keys for {i} : ", color=Colors.purple_to_blue, interval=0.1
    )
    keys.append(key)
try:
    keys[0] = int(keys[0])
except ValueError as v:
    Write.Print("Enter Valid key")
    exit(0)
try:
    keys[-1] = int(keys[-1])
except ValueError as v:
    Write.Print("Enter Valid key")
    exit(0)
stagesOut = "\n".join(stages)
if mode == "e":
    Write.Print(
        f"[*] Start Encryption in this order {stagesOut} \n",
        color=Colors.light_blue,
        interval=0.1,
    )
    plainText = data
    cipherText = caesarCipherEncryption(data, keys[0])
    Write.Print(
        f"Data At Stage {stages[0]} : {cipherText}\n",
        color=Colors.purple_to_blue,
        interval=0.1,
    )
    cipherText = xorCipher(cipherText, keys[1])
    Write.Print(
        f"Data At Stage {stages[1]} : {cipherText}\n",
        color=Colors.purple_to_blue,
        interval=0.1,
    )
    cipherText = vigenereCipherEncrypt(cipherText, keys[2])
    Write.Print(
        f"Data At Stage {stages[2]} : {cipherText}\n",
        color=Colors.purple_to_blue,
        interval=0.1,
    )
    cipherText = railFenceEncrypt(cipherText, keys[-1])
    Write.Print(
        f"Data At Stage {stages[3]} : {cipherText}\n",
        color=Colors.purple_to_blue,
        interval=0.1,
    )
    with open("Encryption.txt", "w") as f:
        f.write(cipherText)
    Write.Print(
        "[*] Data saved at Encryption.txt \n", color=Colors.purple_to_blue, interval=0.1
    )
elif mode == "d":
    stagesOut = "\n".join(stages[::-1])
    Write.Print(
        f"[*] Start Decryption in this order {stagesOut} \n",
        color=Colors.light_blue,
        interval=0.1,
    )
    plainText = data
    plainText = railFenceDecrypt(plainText, keys[-1])
    Write.Print(
        f"Data At Stage {stages[-1]} : {plainText}\n",
        color=Colors.purple_to_blue,
        interval=0.1,
    )
    plainText = vigenereCipherDecrypt(plainText, keys[2])
    Write.Print(
        f"Data At Stage {stages[2]} : {plainText}\n",
        color=Colors.purple_to_blue,
        interval=0.1,
    )
    plainText = xorCipher(plainText, keys[1])
    Write.Print(
        f"Data At Stage {stages[1]} : {plainText}\n",
        color=Colors.purple_to_blue,
        interval=0.1,
    )
    plainText = caesarCipherDecryption(plainText, keys[0])
    Write.Print(
        f"Data At Stage {stages[0]} : {plainText}\n",
        color=Colors.purple_to_blue,
        interval=0.1,
    )
    with open("Decryption.txt", "w") as f:
        f.write(plainText)
    Write.Print(
        "[*] Data saved at Decryption.txt \n", color=Colors.purple_to_blue, interval=0.1
    )
else:
    Write.Print("Enter Valid Option !!!\n", color=Colors.white_to_blue, interval=0.1)
