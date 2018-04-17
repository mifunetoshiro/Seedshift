# Seedshift
Seedshift encrypts/decrypts your mnemonic seed words using a date shift cipher. It supports 12, 18 and 24 word seeds (or their numbers) from the English [BIP-39 wordlist](https://github.com/bitcoin/bips/blob/master/bip-0039/english.txt) of 2048 words, which you also need to download and put in the same folder as this script.

## Example usage
Let's say `oppose duck hello neglect reveal key humor mosquito road evoke flock hedgehog` are your MetaMask seed words. You need to write them down somewhere and keep them safe, but writing the original words down is a security risk. If anyone finds your list of words, they can drain your wallet. Instead, use the English BIP-39 wordlist and encrypt them using a date shift cipher (you don't even need this script to do it, just do it by hand instead if you want).

The script takes dates in YYYY-MM-DD format and sorts them from oldest to newest (to use years before 1000, zero-fill them to 4-digit width, e.g. 0966 for year 966). In case of 24 seed words you can use up to 8 dates, in case of 18 seed words you can use up to 6, and in case of 12 seed words you can use up to 4. So let's say you use 3: your mother's birthday is 1963-07-10, your father's birthday is 1956-04-27, and your birthday is 1994-01-31.

The script will automatically sort the dates from oldest to newest (you don't have to input them in that order) and split each in 3 parts (year, month, day) which will be used to right-shift the words' positions in the English BIP-39 wordlist. In the above example:
```1956, 4, 27, 1963, 7, 10, 1994, 1, 31```.
Given the above seed words and dates, the script will shift the words and output a table with the shifted words and their number:

| #  | Original | Number | Shifted | Encrypted | Number |
|----|----------|--------|---------|-----------|--------|
| 1  | oppose   | 1245   | 1956    | mosquito  | 1153   |
| 2  | duck     | 543    | 4       | dust      | 547    |
| 3  | hello    | 855    | 27      | hotel     | 882    |
| 4  | neglect  | 1185   | 1963    | maximum   | 1100   |
| 5  | reveal   | 1476   | 7       | rich      | 1483   |
| 6  | key      | 977    | 10      | kitten    | 987    |
| 7  | humor    | 889    | 1994    | hair      | 835    |
| 8  | mosquito | 1153   | 1       | mother    | 1154   |
| 9  | road     | 1496   | 31      | salute    | 1527   |
| 10 | evoke    | 625    | 1956    | dream     | 533    |
| 11 | flock    | 715    | 4       | flush     | 719    |
| 12 | hedgehog | 853    | 27      | hospital  | 880    |

Write down the encrypted words or their numbers instead of the original seed words and put them in a safe place. To decrypt them and get back your original seed words, the script will accept either the encrypted words or their numbers and the same dates you used to encrypt them (again, you can also do all of this by hand).

Note that the last encrypted word will most likely not be a valid checksum word (in the above example, `hospital` is valid, though). Having a valid checksum last word can provide plausible deniability in that the encrypted words are in fact encrypted, as they are valid BIP-39 seed words. You could even store a small amount of coins there, so if someone ever steals/uses your seed words, that's all they're going to think you have. The script can generate a valid last checksum word for your encrypted words if you want to replace it (if it's already valid, the script will tell you so, and you don't have to replace it), however, it's not possible to decrypt it back to the original checksum word. If you choose to replace it, you will have to remember or write down your original or shifted last word!

## Safe usage
Only run this script if you understand the code and what it does. Anyone can fork it, turn it malicious and trick you into using it if you don't understand the underlying code. This script does not require any networking modules to function. For safety reasons you should only run this script on an air-gapped computer that is not connected to the internet. Make sure to write down the encrypted seed words or numbers by hand, do not print them.

Note that the encrypted words/numbers are not cryptographically secure, as they can be bruteforced to get the original words, but they do give you some protection from the common thief and some extra time to react in case of theft, etc.
