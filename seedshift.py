import datetime
import binascii
import hashlib
import sys
import socket

if sys.version_info[0] < 3:
    raise Exception("Python 3.x is required!")

bip39 = {}
bip39_list = []
bip39_cn = {}
input_words = []
input_word_numbers = []
input_codepoints = []
input_dates = []
shift_values = []
input_numbers = []
shifted_words = []
shifted_numbers = []
shifted_value = []
chinese = []
sheet1 = []
sheet2 = []
sheet3 = []
cn_flag = False

with open("english.txt") as wordlist:
    line = wordlist.readline()
    count = 1
    while line:
        bip39[count] = line.strip()
        bip39_list.append(line.strip())
        line = wordlist.readline()
        count += 1
    if len(bip39) != 2048:
        raise ValueError("english.txt has " + str(len(bip39)) + " lines, expected 2048!")

try:
    with open("chinese_traditional.txt", encoding="utf-8") as wordlist:
        line = wordlist.readline()
        count = 1
        while line:
            bip39_cn[count] = line.strip()
            line = wordlist.readline()
            count += 1
        if len(bip39_cn) != 2048:
            raise ValueError("chinese_traditional.txt has " + str(len(bip39_cn)) + " lines, expected 2048!")
except FileNotFoundError:
    cn_flag = True

ip = socket.gethostbyname(socket.gethostname())
if ip != "127.0.0.1":
    print("WARNING! You are connected to the internet!")
print("Do NOT run this script on a computer connected to the internet and"
      "\ndo NOT reconnect this computer to the internet without wiping/reformatting it first!"
      "\nA keylogger can steal your seed words!")
q = input("Type \"yes\" if you understand the risks, made precautions and want to proceed: ")
if q.lower() == "yes":
    while True:
        print("\nEnter '1' to encrypt your seed words.")
        print("Enter '2' to decrypt your seed words.")
        print("Enter '3' to decrypt your seed word numbers.")
        print("Enter '4' to decrypt your Traditional Chinese Unicode codepoints.")
        try:
            x = int(input("Input: "))
            if x not in [1, 2, 3, 4]:
                print("Invalid input.")
                continue
            else:
                break
        except ValueError:
            print("Invalid input.")
            continue
    
    if x == 1 or x == 2:
        while True:
            flag = False
            if x == 1:
                words = input("\nEnter your 12, 15, 18 or 24 seed words in \"cat dad jar...\" format: ").lower().split()
            elif x == 2:
                words = input("\nEnter your 12, 15, 18 or 24 encrypted seed words in \"cat dad jar...\" format: ").lower().split()
            if len(words) not in [12, 15, 18, 24]:
                print(str(len(words)) + " words entered, please enter 12, 15, 18 or 24 words.")
                continue
            else:
                if not flag:
                    for word in words:
                        if word not in bip39.values():
                            flag = True
                            input_words.clear()
                            print("'" + word + "' is not a valid BIP-39 word.")
                            continue
                        else:
                            input_words.append(word)
                if flag:
                    continue
                break
    elif x == 3:
        while True:
            flag = False
            numbers = input("\nEnter your 12, 15, 18 or 24 encrypted seed word numbers in \"1 2 3...\" format: ").split()
            if len(numbers) not in [12, 15, 18, 24]:
                print(str(len(numbers)) + " numbers entered, please enter 12, 15, 18 or 24 numbers.")
                continue
            else:
                if not flag:
                    for number in numbers:
                        try:
                            if int(number) not in bip39:
                                flag = True
                                input_word_numbers.clear()
                                print("'" + number + "' is not a valid BIP-39 seed word number.")
                                continue
                            else:
                                input_word_numbers.append(number)
                        except ValueError:
                            flag = True
                            input_word_numbers.clear()
                            print("'" + number + "' is not a valid BIP-39 seed word number.")
                            continue
                if flag:
                    continue
                for n in input_word_numbers:
                    input_words.append(bip39[int(n)])
                words = input_words
                break
    elif x == 4:
        if cn_flag:
            raise FileNotFoundError("chinese_traditional.txt not found!")
        else:
            while True:
                flag = False
                codepoints = input("\nEnter your 12, 15, 18 or 24 Traditional Chinese codepoints in any format: ").replace(" ", "")
                parts = [codepoints[i:i + 4] for i in range(0, len(codepoints), 4)]
                if len(parts) not in [12, 15, 18, 24]:
                    print(str(len(parts)) + " codepoints entered, please enter 12, 15, 18 or 24 codepoints.")
                    continue
                else:
                    if not flag:
                        for cp in parts:
                            try:
                                if chr(int(cp, 16)) not in bip39_cn.values():
                                    flag = True
                                    input_codepoints.clear()
                                    print("'" + cp + "' is not a valid Traditional Chinese BIP-39 seed word Unicode codepoint.")
                                    continue
                                else:
                                    input_codepoints.append(cp.upper())
                            except ValueError:
                                flag = True
                                input_codepoints.clear()
                                print("'" + cp + "' is not a valid Traditional Chinese BIP-39 seed word Unicode codepoint.")
                                continue
                    if flag:
                        continue
                    for n in input_codepoints:
                        input_words.append(bip39[list(bip39.keys())[list(bip39_cn.values()).index(chr(int(n, 16)))]])
                    words = input_words
                    break
    
    while True:
        try:
            if len(words) == 12:
                n = int(input("\nInput the number of dates you want to use (max 4): "))
                if n < 1 or n > 4:
                    print("Please enter a valid number (1-4).")
                    continue
                else:
                    break
            elif len(words) == 15:
                n = int(input("\nInput the number of dates you want to use (max 5): "))
                if n < 1 or n > 5:
                    print("Please enter a valid number (1-5).")
                    continue
                else:
                    break
            elif len(words) == 18:
                n = int(input("\nInput the number of dates you want to use (max 6): "))
                if n < 1 or n > 6:
                    print("Please enter a valid number (1-6).")
                    continue
                else:
                    break
            elif len(words) == 24:
                n = int(input("\nInput the number of dates you want to use (max 8): "))
                if n < 1 or n > 8:
                    print("Please enter a valid number (1-8).")
                    continue
                else:
                    break
        except ValueError:
            if len(words) == 12:
                print("Please enter a valid number (1-4).")
            elif len(words) == 15:
                print("Please enter a valid number (1-5).")
            elif len(words) == 18:
                print("Please enter a valid number (1-6).")
            elif len(words) == 24:
                print("Please enter a valid number (1-8).")
            continue
    
    count = 1
    while count <= n:
        while True:
            try:
                date = input("\nEnter date " + str(count) + " in YYYY-MM-DD format: ")
                tmp = date.split("-")
                if len(tmp[0]) < 4:
                    while len(tmp[0]) < 4:
                        tmp[0] = ''.join(('0',tmp[0]))
                    date = tmp[0] + "-" + tmp[1] + "-" + tmp[2]
                input_dates.append(datetime.datetime.strptime(date, "%Y-%m-%d"))
            except ValueError:
                print("Incorrect date format, please use YYYY-MM-DD.")
                continue
            count += 1
            break
    input_dates.sort()
    dates_sorted = [datetime.datetime.strftime(d, "%Y-%m-%d") for d in input_dates]
    for d in dates_sorted:
        shift_values.extend(map(int, d.split("-")))
    
    def encrypt(words):
        count = 0
        for word in words:
            if count == len(shift_values):
                count = 0
            number = list(bip39.keys())[list(bip39.values()).index(word)]
            input_numbers.append(number)
            try:
                number += shift_values[count]
                shifted_words.append(bip39[number])
                shifted_numbers.append(number)
                shifted_value.append(shift_values[count])
                if not cn_flag:
                    chinese.append(hex(ord(bip39_cn[number])).upper()[2:])
                else:
                    chinese.append("")
                count += 1
            except KeyError:
                index = number % 2048
                if index == 0:
                    index = 2048
                shifted_words.append(bip39[index])
                shifted_numbers.append(index)
                shifted_value.append(shift_values[count])
                if not cn_flag:
                    chinese.append(hex(ord(bip39_cn[index])).upper()[2:])
                else:
                    chinese.append("")
                count += 1
    
    def decrypt(words):
        count = 0
        for word in words:
            if count == len(shift_values):
                count = 0
            number = list(bip39.keys())[list(bip39.values()).index(word)]
            input_numbers.append(number)
            try:
                number -= shift_values[count]
                shifted_words.append(bip39[number])
                shifted_numbers.append(number)
                shifted_value.append(shift_values[count])
                count += 1
            except KeyError:
                index = number % 2048
                if index == 0:
                    index = 2048
                shifted_words.append(bip39[index])
                shifted_numbers.append(index)
                shifted_value.append(shift_values[count])
                count += 1
    
    pos = range(1, len(input_words) + 1)
    if x == 1:
        encrypt(input_words)
        headers = ["#", "Original", "Number", "Shifted", "Encrypted", "Number", "Chinese"]
        table = [headers] + list(zip(pos, input_words, input_numbers, shifted_value, shifted_words, shifted_numbers, chinese))
    elif x == 2 or x == 3:
        decrypt(input_words)
        headers = ["#", "Encrypted", "Number", "Shifted", "Decrypted", "Number"]
        table = [headers] + list(zip(pos, input_words, input_numbers, shifted_value, shifted_words, shifted_numbers))
    elif x == 4:
        decrypt(input_words)
        headers = ["#", "Chinese", "English", "Number", "Shifted", "Decrypted", "Number"]
        table = [headers] + list(zip(pos, input_codepoints, input_words, input_numbers, shifted_value, shifted_words, shifted_numbers))
    print("\n")
    for a, b in enumerate(table):
        line = "| ".join(str(c).ljust(10) for c in b)
        print(line)
        if a == 0:
            print("-" * len(line))
    
    # check checksum function code from https://github.com/trezor/python-mnemonic, Copyright (c) 2013-2018 Pavol Rusnak
    def check(mnemonic):
        mnemonic = mnemonic.split(' ')
        try:
            idx = map(lambda x: bin(bip39_list.index(x))[2:].zfill(11), mnemonic)
            b = ''.join(idx)
        except:
            return False
        l = len(b)
        d = b[:l // 33 * 32]
        h = b[-l // 33:]
        nd = binascii.unhexlify(hex(int(d, 2))[2:].rstrip('L').zfill(l // 33 * 8))
        nh = bin(int(hashlib.sha256(nd).hexdigest(), 16))[2:].zfill(256)[:l // 33]
        return h == nh
    
    if x == 1:
        wordstring = " ".join(shifted_words)
        if check(wordstring):
            flag = False
            print("\n" + str(shifted_words[-1]) + " / " + str(shifted_numbers[-1]) + " is a valid " + str(len(words)) + "th checksum word!")
        else:
            print("\n" + str(shifted_words[-1]) + " / " + str(shifted_numbers[-1]) + " is not a valid " + str(len(words)) + "th checksum word. Generate a new valid word to replace it? (y/n)")
            while True:
                    x = input("Input: ").lower()
                    if x != "y" and x != "n":
                        print("Invalid input.")
                        continue
                    else:
                        if x == "n":
                            break
                        else:
                            flag = True
                            wordstring = " ".join(shifted_words[:-1])
                            for w in bip39_list:
                                test = wordstring + " " + w
                                if check(test):
                                    print("\nNew valid " + str(len(words)) + "th checksum word: " + w + " / " + str(list(bip39.keys())[list(bip39.values()).index(w)]))
                                    print("\nPlease note that if you replace the last encrypted word with a valid checksum word,"
                                          "\nthere is NO WAY to get back the original word by using the decrypt function of this script,"
                                          "\nyou will have to remember or write down your original or encrypted last word as well!")
                                    break
                    break
        print("\nSplit the encrypted seed words into '2-out-of-3' recovery sheets? (y/n)")
        while True:
                x = input("Input: ").lower()
                if x != "y" and x != "n":
                    print("Invalid input.")
                    continue
                else:
                    if x == "n":
                        break
                    else:
                        count = 1
                        while count <= len(words):
                            if count % 3 != 0:
                                string = "#" + str(count) + ": " + str(shifted_words[count - 1]) + " / " + str(shifted_numbers[count - 1]) + " / " + str(chinese[count - 1])
                                sheet1.append(string)
                            if (count + 1) % 3 != 0:
                                string = "#" + str(count) + ": " + str(shifted_words[count - 1]) + " / " + str(shifted_numbers[count - 1]) + " / " + str(chinese[count - 1])
                                sheet2.append(string)
                            if (count - 1) % 3 != 0:
                                string = "#" + str(count) + ": " + str(shifted_words[count - 1]) + " / " + str(shifted_numbers[count - 1]) + " / " + str(chinese[count - 1])
                                sheet3.append(string)
                            if count == len(words):
                                if flag:
                                    sheet1.append("")
                                    string = "#" + str(count) + " (replaced): " + w + " / " + str(list(bip39.keys())[list(bip39.values()).index(w)])
                                    sheet2.append(string)
                                    sheet3.append(string)
                            count += 1
                        headers2 = ["Sheet 1", "Sheet 2", "Sheet 3"]
                        table2 = [headers2] + list(zip(sheet1, sheet2, sheet3))
                        print("\n")
                        for a, b in enumerate(table2):
                            line = "| ".join(str(c).ljust(33) for c in b)
                            print(line)
                            if a == 0:
                                print("-" * len(line))
                        print("\nEach sheet has two thirds of your encrypted seed words."
                              "\nYou need any two sheets to recover your full encrypted mnemonic phrase."
                              "\nStore each at a different safe place or hand out to your family members or attorney."
                              "\nA single sheet cannot give access to your wallet, if you lose the other two, your funds are lost forever!")
                        if flag:
                            print("\nPlease don't forget that if you replaced the last word with a valid checksum word,"
                                  "\nyou will have to remember or write down your original or encrypted last word somewhere as well!")
                break
    
    input('\nPress enter to exit.')
