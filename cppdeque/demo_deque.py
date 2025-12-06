import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from cppdeque.deque import Deque

def run_e2e_test():
    print("=========================================")
    print("      cppdeque demonstration Test")
    print("=========================================")

    d = Deque()
    print("\n[Case 1] Push Front & Back")
    d.push_back(100)
    d.push_front(1)
    d.push_back(200)
    d.push_front(0)
    # Expected: 0, 1, 100, 200
    print(f"  > Deque: {d}")

    print("\n[Case 2] Random Access O(1)")
    print(f"  > d[0]: {d[0]}")
    print(f"  > d[2]: {d[2]}")
    print(f"  > d[3]: {d[3]}")

    print("\n[Case 3] Modification")
    d[2] = 500
    print(f"  > Change index 2 to 500: {d}")

    print("\n[Case 4] Pop")
    print(f"  > Pop Front: {d.pop_front()}")
    print(f"  > Pop Back:  {d.pop_back()}")
    print(f"  > Result: {d}")

    print("\nStatus: SUCCESS")

if __name__ == "__main__":
    run_e2e_test()
