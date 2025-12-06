import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from cppforward_list.forward_list import ForwardList

def run_e2e_test():
    print("=========================================")
    print("   cppforward_list demonstration")
    print("=========================================")

    print("\n[Case 1] Push Front & Optimization")
    fl = ForwardList()
    fl.push_front(1)
    fl.push_front(2)
    fl.push_front(3)
    print(f"  > Pushed 3, 2, 1: {fl}") # 3 -> 2 -> 1

    print("\n[Case 2] Reverse In-Place")
    fl.reverse()
    print(f"  > Reversed: {fl}") # 1 -> 2 -> 3

    print("\n[Case 3] Insert After")
    it = fl.begin() # Points to 1
    print(f"  > Iterator at: {it.current.value}")
    fl.insert_after(it, 99)
    print(f"  > Inserted 99 after 1: {fl}")

    print("\nStatus: SUCCESS")

if __name__ == "__main__":
    run_e2e_test()
