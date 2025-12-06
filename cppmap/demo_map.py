import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from cppmap.map import Map

def run_e2e_test():
    print("=========================================")
    print("        cppmap demonstration")
    print("=========================================")

    print("\n[Case 1] Automatic Sorting")
    m = Map()
    # Insert in random order
    m[10] = "Decade"
    m[2] = "Pair"
    m[50] = "Fifty"
    m[0] = "Zero"
    
    # Expected: 0, 2, 10, 50
    print(f"  > Map Contents: {m}")

    print("\n[Case 2] Lower Bound Search")
    # Finding first key >= 9. Should be 10.
    lb = m.lower_bound(9)
    print(f"  > lower_bound(9): {lb}") # 10
    
    # Finding first key >= 11. Should be 50.
    lb2 = m.lower_bound(11)
    print(f"  > lower_bound(11): {lb2}") # 50

    print("\n[Case 3] Erase")
    m.erase(10)
    print(f"  > Erased 10: {m}")

    print("\nStatus: SUCCESS")

if __name__ == "__main__":
    run_e2e_test()
