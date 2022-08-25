import time
import argparse
    
def get_possible_key(periods, initial_state_len, keystream):
    """From all periods, generate bits stream based on the size of the keystream
    and compare number of occurrence with him. Return a dict of the possible key """

    best_occurrence = 0

    # For each period, we will generate bits stream and compare occurrences with keystream to get best possible key
    for i in range(len(periods)):
        print(f'Checking key : {i+1} / {len(periods)}', end='\r')
        
        period_finish = False
        
        bits_stream = ""
        nb_generated_bit = 0
        
        # Generating bits stream for current period and compare with the keystream
        while not period_finish:
            if nb_generated_bit == 0:
                next_index = i
            
            if next_index == len(periods):
                next_index = 0
            
            # Generating a new bit
            bits_stream += str(int(periods[next_index], 2) & 1)
            
            nb_generated_bit+=1
            next_index+=1
    
            # All bits is generated for the period
            if nb_generated_bit == len(keystream):
                # Get occurrences between generated bits stream and keystream
                occurrence = sum(a == b for a,b in zip(bits_stream, keystream))
                
                # If generated bits stream from this period have best occurrences than old periods, replace it
                if occurrence > best_occurrence:
                    best_occurrence = occurrence
                    possible_key = {"key": bits_stream[:initial_state_len], "occurrence": best_occurrence}
                
                period_finish = True

    return possible_key


def calcul_lfsr(initial_state, initial_state_len, xor_bit_pos):
    """Calcul LFSR from an initial_state. Return a list of all periods."""

    periods = []
    periods.append(initial_state)

    finish = False

    while not finish:
        for period in periods:
            xor_bits = []

            # Gets bits for xor
            for pos in xor_bit_pos:
                xor_bits.append(bin(int(period, 2) >> pos & 1))

            xor_result = "0b0"

            # Doing xor
            for xor_bit in xor_bits:
                xor_result = bin(int(xor_result, 2) ^ int(xor_bit, 2))
                
            # Shift one bit to the right
            shifted_bin = bin(int(period, 2) >> 1)
            shifted_bin = f'{int(shifted_bin, 2):#0{initial_state_len+2}b}'

            # Add result of xor before shifted bits to get new period
            result = bin(int(shifted_bin, 2) | (int(xor_result, 2) << initial_state_len-1))
            result = f'{int(result, 2):#0{initial_state_len+2}b}'

            # If new period is same than initial state, LFSR is done
            if initial_state == result:
                finish = True
            else:
                periods.append(result)
    
    print(f'Number of possibilities : {len(periods)}')
    
    return periods


def check_args(parser, args):
    """Check all arguments from the parser and prepare all variables required by the program
    Return a list of all arguments"""

    # Get arguments and create initial_state with the number of bits of polynomial
    initial_state = f'{1:0{args.polynomialsize}b}'
    initial_state_len = args.polynomialsize
    initial_state = f'{int(initial_state, 2):#0{len(initial_state)+2}b}'

    # Get keystream and keystreamsize
    keystream_size = args.keystreamsize
    keystream = args.keystream

    # Check if keystream is a valid hexadecimal
    try:
        keystream = f"{int(keystream, 16):0{keystream_size}b}"
    except ValueError:
        parser.error("Error: Please enter a valid hexadecimal keystream.")

    # Check if at least 2 xor bit positions
    if(len(args.xorposition) >= 2):
        xor_bit_pos = tuple(args.xorposition)
    else:
        parser.error("Error: You need to specify minimum 2 bits to xor.")

    return [initial_state, initial_state_len, keystream, xor_bit_pos]


def get_args(parser):
    """Create arguments for the program and return parser"""

    parser.add_argument("--polynomialsize", "-S", type=int, required=True, help="Number of bits of the polynomial.")
    parser.add_argument("--keystream", "-k", type=str, required=True, help="Keystream in hexadecimal.")
    parser.add_argument("--keystreamsize", "-s", type=int, required=True, help="Number of bits of the keystream.")
    parser.add_argument("--xorposition", "-p", type=int, required=True, help="Positions of bit to be xor separed by space (start at 0 from the right).", nargs="+")
    args = parser.parse_args()
	
    return args


def main():
    start_time = time.time()

    parser = argparse.ArgumentParser()
    args = get_args(parser)
    initial_state, initial_state_len, keystream, xor_bit_pos = check_args(parser, args)

    print("""
     _____     ____
    /      \  |  o |
   |        |/ ___\|  Correlation Attacks of an LFSR based Stream Cipher
   |_________/        by Morc
   |_|_| |_|_| 
    """)

    periods = calcul_lfsr(initial_state, initial_state_len, xor_bit_pos)
    possible_key = get_possible_key(periods, initial_state_len, keystream)
    
    print(f"\n\nPossible key: {possible_key['key']} | Occurrences: {possible_key['occurrence']}/{len(keystream)}")
    print(f"\n--- {(time.time() - start_time)} seconds ---")


if __name__ == "__main__":
    main()
