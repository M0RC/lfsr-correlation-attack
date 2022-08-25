# Correlation Attacks of an LFSR based Stream Cipher
![](https://raw.githubusercontent.com/M0RC/lfsr-correlation-attack/main/demo.gif)

## Getting started
To recover the key, we need to generate the part of key with the help of the keystream and
polynomials. Each polynomial generates a part of the key.

## Steps
1. Calcul LFSR
    * The first step is calculating the LFSR of the polynomial to get all periods.
    * Number of periods are number of possibilities.
2. Generate bits stream for all possibilities
    * The second step is generating bits stream for each period.
    * To proceed, for each period, loop from the current period and get the last bit of each period until you have same number of bits than keystream size.
3. Compare generated bits stream with the keystream
    * For each generated bits stream, compare them with the keystream and count the number of occurrences of each same bit.
    * The generated bits stream with the best occurrences contains the possible key in the beginning (the possible key has the same number of bits than number of bits of polynomial).
4. Repeat previous steps for all polynomials
5. Recover the key
    * Put all possible key together to get the key

## How to run the program
The program uses argparse. You need to pass a value for each following parameter:
* **-S, --polynomialsize**: Number of bits of the polynomial.
* **-k, --keystream**: Keystream in hexadecimal.
* **-s, --keystreamsize**: Number of bits of the keystream.
* **-p, --xorposition**: Positions of the bits to be xor, separated by spaces (start at 0 from the right)

For example: python3 lfsr.py --polynomialsize <size> --keystream <keystream> --keystreamsize <size> --xorposition <pos pos 
