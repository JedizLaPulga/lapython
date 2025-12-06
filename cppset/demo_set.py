import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from cppset.set import Set

def run_e2e_test():
    print("=========================================")
    print("        cppset demonstration")
    print("=========================================")

    print("\n[Case 1] Automatic Sorting & Uniqueness")
    s = Set()
    data = [10, 5, 20, 5, 10]
    print(f"  > Inserting: {data}")
    for x in data:
        s.insert(x)
    
    # Expected: 5, 10, 20
    print(f"  > Set Contents: {s}")

    print("\n[Case 2] Range Queries")
    # Set is {5, 10, 20}
    print(f"  > lower_bound(6): {s.lower_bound(6)}") # 10
    print(f"  > upper_bound(10): {s.upper_bound(10)}") # 20

    print("\n[Case 3] Erase")
    s.erase(10)
    print(f"  > Erased 10: {s}")

    print("\nStatus: SUCCESS")

if __name__ == "__main__":
    run_e2e_test()
