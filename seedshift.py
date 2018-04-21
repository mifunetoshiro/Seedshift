import datetime
import binascii
import hashlib

bip39 = {}
bip39_list = []
input_words = []
input_word_numbers = []
input_dates = []
shift_values = []
input_numbers = []
shifted_words = []
shifted_numbers = []
shifted_value = []

with open("english.txt") as wordlist:
    line = wordlist.readline()
    count = 1
    while line:
        bip39[count] = line.strip()
        bip39_list.append(line.strip())
        line = wordlist.readline()
        count += 1
    if len(bip39) != 2048:
        raise ValueError("Wordlist has " + str(len(bip39)) + " lines, expected 2048!")

while True:
    print("Enter '1' to encrypt your seed words.")
    print("Enter '2' to decrypt your seed words.")
    print("Enter '3' to decrypt your seed word numbers.")
    try:
        x = int(input("Input: "))
        if x not in [1, 2, 3]:
            print("Invalid input.")
            continue
        else:
            break
    except ValueError:
        print("Invalid input.")
        continue

if x != 3:
    while True:
        flag = False
        if x == 1:
            words = input("Enter your 12, 18 or 24 seed words in \"cat dad jar...\" format: ").lower().split()
        elif x == 2:
            words = input("Enter your 12, 18 or 24 encrypted seed words in \"cat dad jar...\" format: ").lower().split()
        if len(words) not in [12, 18, 24]:
            print(str(len(words)) + " words entered, please enter 12, 18 or 24 words.")
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
else:
    while True:
        flag = False
        numbers = input("Enter your 12, 18 or 24 encrypted seed word numbers in \"1 2 3...\" format: ").split()
        if len(numbers) not in [12, 18, 24]:
            print(str(len(numbers)) + " numbers entered, please enter 12, 18 or 24 numbers.")
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

while True:
    try:
        if len(words) == 12:
            n = int(input("Input the number of dates you want to use (max 4): "))
            if n < 1 or n > 4:
                print("Please enter a valid number (1-4).")
                continue
            else:
                break
        elif len(words) == 18:
            n = int(input("Input the number of dates you want to use (max 6): "))
            if n < 1 or n > 6:
                print("Please enter a valid number (1-6).")
                continue
            else:
                break
        elif len(words) == 24:
            n = int(input("Input the number of dates you want to use (max 8): "))
            if n < 1 or n > 8:
                print("Please enter a valid number (1-8).")
                continue
            else:
                break
    except ValueError:
        if len(words) == 12:
            print("Please enter a valid number (1-4).")
        elif len(words) == 18:
            print("Please enter a valid number (1-6).")
        elif len(words) == 24:
            print("Please enter a valid number (1-8).")
        continue

count = 1
while count <= n:
    while True:
        try:
            date = input("Enter date " + str(count) + " in YYYY-MM-DD format: ")
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
            count += 1
        except KeyError:
            index = number % 2048
            if index == 0:
                index = 2048
            shifted_words.append(bip39[index])
            shifted_numbers.append(index)
            shifted_value.append(shift_values[count])
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

if x == 1:
    encrypt(input_words)
    headers = ["#", "Original", "Number", "Shifted", "Encrypted", "Number"]
elif x == 2 or x == 3:
    decrypt(input_words)
    headers = ["#", "Encrypted", "Number", "Shifted", "Decrypted", "Number"]

pos = range(1, len(input_words) + 1)
table = [headers] + list(zip(pos, input_words, input_numbers, shifted_value, shifted_words, shifted_numbers))
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
        print("\n" + str(shifted_words[-1]) + " : " + str(shifted_numbers[-1]) + " is a valid " + str(len(words)) + "th checksum word!")
    else:
        print("\n" + str(shifted_words[-1]) + " : " + str(shifted_numbers[-1]) + " is not a valid " + str(len(words)) + "th checksum word. Generate a new valid word to replace it? (y/n)")
        while True:
                x = input("Input: ").lower()
                if x != "y" and x != "n":
                    print("Invalid input.")
                    continue
                else:
                    if x == "n":
                        break
                    else:
                        wordstring = " ".join(shifted_words[:-1])
                        for w in bip39_list:
                            test = wordstring + " " + w
                            if check(test):
                                print("\nNew valid " + str(len(words)) + "th checksum word: " + w + " : " + str(list(bip39.keys())[list(bip39.values()).index(w)]))
                                print("\nPlease note that if you replace the last encrypted word with a valid checksum word, "
                                      "\nthere is no way to get back the original word by using the decrypt function of this script, "
                                      "\nyou will have to remember or write down your original or shifted last word!")
                                break
                break

input('\nPress enter to exit.')
