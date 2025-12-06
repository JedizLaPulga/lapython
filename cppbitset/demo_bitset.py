import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from cppbitset.bitset import Bitset

def run_e2e_test():
    print("=========================================")
    print("      cppbitset demonstration Test")
    print("=========================================")

    print("\n[Case 1] Initialization")
    b = Bitset(8, "01010101")
    print(f"  > Bitset<8>: {b}")
    print(f"  > ULong val: {b.to_ulong()} (Decimal)")

    print("\n[Case 2] Modification")
    print(f"  > b[0] is {b[0]}")
    print("  > Flipping b[0]")
    b.flip(0)
    print(f"  > b[0] is now {b[0]}")
    print(f"  > New state: {b}")

    print("\n[Case 3] Logic Ops")
    b1 = Bitset(4, "1100")
    b2 = Bitset(4, "1010")
    print(f"  > b1: {b1}")
    print(f"  > b2: {b2}")
    print(f"  > b1 & b2: {b1 & b2}")
    print(f"  > b1 | b2: {b1 | b2}")
    print(f"  > b1 ^ b2: {b1 ^ b2}")

    print("\nStatus: SUCCESS")

if __name__ == "__main__":
    run_e2e_test()
