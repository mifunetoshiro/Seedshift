## Safe usage
Only run this script if you understand the code and what it does. Anyone can fork it, turn it malicious and trick you into using it if you don't understand the underlying code. This script does not require any networking modules to function. For safety reasons you should only run this script on an air-gapped computer that is not connected to the internet (do NOT reconnect this computer to the internet without wiping/reformatting it first). A better option would be to just do it manually with the "mapping_table.txt" file, but do not use Ctrl-F to find your words, as even that can be a security risk. Make sure to write down the encrypted seed words, numbers or codepoints by hand, do not print them. Even better, stamp or engrave them on titanium plates to protect from fire or water damage. 

Note that the encrypted words/numbers are not cryptographically secure, as they can be bruteforced to get the original words, but they do give you some protection from the common thief and some extra time to react in case of theft, etc.

# Seedshift
Seedshift encrypts/decrypts your mnemonic seed words using a date shift cipher. It supports 12, 18 and 24 word seeds (or their numbers) from the [BIP-39](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki) English [wordlist](https://github.com/bitcoin/bips/blob/master/bip-0039/english.txt) ([raw file](https://raw.githubusercontent.com/bitcoin/bips/master/bip-0039/english.txt)) of 2048 words, which you also need to download and put in the same folder as this script. Additionally, to further obfuscate your encrypted seed words, also download the BIP-39 Traditional Chinese [wordlist](https://github.com/bitcoin/bips/blob/master/bip-0039/chinese_traditional.txt) ([raw file](https://raw.githubusercontent.com/bitcoin/bips/master/bip-0039/chinese_traditional.txt)) (don't worry, you don't need to know or learn Chinese), to map your encrypted English words' positions in the wordlist to the [Unicode](https://en.wikipedia.org/wiki/Unicode) codepoints of the characters at the same positions in the Traditional Chinese wordlist (you could also use [bip39_obfuscator](https://github.com/mifunetoshiro/bip39_obfuscator) to obfuscate-only your seed words without encrypting them with a date shift cipher). The script also accepts Unicode codepoints as input so you can later decrypt your seed words. To run the script, you need [Python 3.x](https://www.python.org/downloads/) installed on your system. Best of all, you don't even need this script or Python at all, you can do everything by hand if you want (use modulo 2048 to "wrap around" the wordlist, e.g. 2032 shifted by 1999 is 4031, 4031 mod 2048 = 1983; 1983 unshifted by 1999 is -16, -16 mod 2048 = 2032), "mapping_table.txt" can help you a bit with this.

## Purpose
The purpose of this is to be able to safely write down your mnemonic seed words, not having to worry about a thief stealing your private keys, and in case something happens to you, allow your family to regain access to your wallet without needing to know a complex passphrase (TREZOR/Ledger), as all they need to know is the dates you used and the method to decrypt the words (pretty easy if it's in-family birthdays). Gather them around the table and do a couple of examples by hand. If you have a TREZOR or Ledger hardware wallet, having a complex passphrase as the "25th" word is more secure, but the more complex the passphrase is, the easier it is for your family or even you to not remember it at all (unless you wrote it down, which is a security risk in itself). If something were to happen to you, having a simpler passphrase (such as names or birthdates) would make it easier for your family to remember and access your wallet, and you could use both a passphrase *and* encrypt the seed words with a date shift cipher for extra security.

The script optionally splits the encrypted seed words into "2-out-of-3" recovery sheets, where each sheet stores two thirds of your encrypted seed words. You need to combine any two sheets to recover your full encrypted mnemonic phrase, a single sheet is not enough. Store each at a different safe place or hand out to your family members or attorney. Remember, you need at least two sheets, if you lose them, you will not be able to recover your wallet.

## Example usage
Let's say `oppose duck hello neglect reveal key humor mosquito road evoke flock hedgehog` are your MetaMask seed words. You need to write them down somewhere and keep them safe, but writing the original words down is a security risk. If anyone finds your list of words, they can drain your wallet. Instead, use the English BIP-39 wordlist and encrypt them using a date shift cipher (remember, you don't need this script to do it, just do it by hand instead if you want).

The script takes dates in YYYY-MM-DD format and sorts them from oldest to newest (to use years before 1000, zero-fill them to 4-digit width, e.g. 0966 for year 966). In case of 24 seed words you can use up to 8 dates, in case of 18 seed words you can use up to 6, and in case of 12 seed words you can use up to 4. So let's say you use 3: your mother's birthday is 1963-07-10, your father's birthday is 1956-04-27, and your birthday is 1994-01-31.

The script will automatically sort the dates from oldest to newest (you don't have to input them in that order) and split each in 3 parts (year, month, day) which will be used to right-shift the words' positions in the English BIP-39 wordlist. In the above example:
`1956, 4, 27, 1963, 7, 10, 1994, 1, 31`.
Given the above seed words and dates, the script will shift the words and output a table with the shifted words, their number and the Unicode codepoint of the Chinese counterpart character in the Traditional Chinese wordlist (if present):

| #  | Original | Number | Shifted | Encrypted | Number | Chinese |
|----|----------|--------|---------|-----------|--------|---------|
| 1  | oppose   | 1245   | 1956    | mosquito  | 1153   | 5BF6    |
| 2  | duck     | 543    | 4       | dust      | 547    | 5B57    |
| 3  | hello    | 855    | 27      | hotel     | 882    | 6162    |
| 4  | neglect  | 1185   | 1963    | maximum   | 1100   | 7238    |
| 5  | reveal   | 1476   | 7       | rich      | 1483   | 6C2E    |
| 6  | key      | 977    | 10      | kitten    | 987    | 6FC3    |
| 7  | humor    | 889    | 1994    | hair      | 835    | 4E4E    |
| 8  | mosquito | 1153   | 1       | mother    | 1154   | 5348    |
| 9  | road     | 1496   | 31      | salute    | 1527   | 95CA    |
| 10 | evoke    | 625    | 1956    | dream     | 533    | 52E2    |
| 11 | flock    | 715    | 4       | flush     | 719    | 932F    |
| 12 | hedgehog | 853    | 27      | hospital  | 880    | 4E95    |

Write down the encrypted words, their numbers or the Chinese Unicode codepoints instead of the original seed words and put them in a safe place. To decrypt them and get back your original seed words, the script will accept the encrypted words, their numbers or the Unicode codepoints and the same dates you used to encrypt them (again, you can also do all of this by hand).

Note that the last encrypted word will most likely not be a valid checksum word (in the above example, `hospital` is valid, though). Having a valid checksum last word can provide plausible deniability in that the encrypted words are in fact encrypted, as they are valid BIP-39 seed words. You could even store a small amount of coins there, so if someone ever steals/uses your seed words, that's all they're going to think you have. The script can generate a valid last checksum word for your encrypted words if you want to replace it (if it's already valid, the script will tell you so, and you don't have to replace it), however, it's not possible to decrypt it back to the original checksum word. If you choose to replace it, you will have to remember or write down your original or encrypted last word as well!

You can store the Chinese Unicode codepoints in multiple ways, since each is 4 characters long (just remember this fact when you want to rebuild your original seed words). You could write it unchanged: `5BF6 5B57 6162 7238 6C2E 6FC3 4E4E 5348 95CA 52E2 932F 4E95`, or, to make it look even more random, as a bunch of hexadecimal characters that return useless nonsense when converted back to text (*[ö[Wabr8l.oÃNNSHÊRâ/N*), you could write it without spaces: `5BF65B57616272386C2E6FC34E4E534895CA52E2932F4E95`, you could write it with a space every 2 characters: `5B F6 5B 57 61 62 72 38 6C 2E 6F C3 4E 4E 53 48 95 CA 52 E2 93 2F 4E 95`, you could group two or more together: `5BF65B57 61627238 6C2E6FC3 4E4E5348 95CA52E2 932F4E95`, etc. The script accepts Unicode codepoints in any format (with or without spaces) to later convert back into English words.

I included "mapping_table.txt" and "mapping_table_unicode_sorted.txt" files for manually looking up and converting the Unicode codepoints.

Optionally, you can split the encrypted seed words into 2-out-of-3 recovery sheets. The script will output a table:

| Sheet 1                    | Sheet 2                    | Sheet 3                    |
|----------------------------|----------------------------|----------------------------|
| #1: mosquito / 1153 / 5BF6 | #1: mosquito / 1153 / 5BF6 | #2: dust / 547 / 5B57      |
| #2: dust / 547 / 5B57      | #3: hotel / 882 / 6162     | #3: hotel / 882 / 6162     |
| #4: maximum / 1100 / 7238  | #4: maximum / 1100 / 7238  | #5: rich / 1483 / 6C2E     |
| #5: rich / 1483 / 6C2E     | #6: kitten / 987 / 6FC3    | #6: kitten / 987 / 6FC3    |
| #7: hair / 835 / 4E4E      | #7: hair / 835 / 4E4E      | #8: mother / 1154 / 5348   |
| #8: mother / 1154 / 5348   | #9: salute / 1527 / 95CA   | #9: salute / 1527 / 95CA   |
| #10: dream / 533 / 52E2    | #10: dream / 533 / 52E2    | #11: flush / 719 / 932F    |
| #11: flush / 719 / 932F    | #12: hospital / 880 / 4E95 | #12: hospital / 880 / 4E95 |


Write down and store each sheet separately at a different location. Please remember that if you replaced the last encrypted seed word with a valid checksum word, you will have to remember or write down your original or encrypted last word somewhere as well!
