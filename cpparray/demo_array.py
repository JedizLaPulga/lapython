import sys
import os

# Ensure we can import the local package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from cpparray.array import Array

def run_e2e_test():
    print("=========================================")
    print("      cpparray demonstration Test")
    print("=========================================")

    print("\n[Case 1] Creation & Access")
    a = Array(5, init_value=0)
    print(f"  > Created Array(5): {a}")
    
    a[0] = 10
    a[4] = 99
    print(f"  > Modified [0]=10, [4]=99: {a}")
    
    try:
        a[5] = 100
    except IndexError as e:
        print(f"  > Accessing [5] (OutOfBounds): Caught expected error '{e}'")

    print("\n[Case 2] Fill")
    a.fill(7)
    print(f"  > After fill(7): {a}")

    print("\n[Case 3] Swap")
    b = Array(5, init_value=2)
    print(f"  > Array A: {a}")
    print(f"  > Array B: {b}")
    print("  > Swapping...")
    a.swap(b)
    print(f"  > Array A: {a}")
    print(f"  > Array B: {b}")

    print("\nStatus: SUCCESS")

if __name__ == "__main__":
    run_e2e_test()
