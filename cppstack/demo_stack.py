import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from cppstack.stack import Stack

def run_e2e_test():
    print("=========================================")
    print("      cppstack demonstration Test")
    print("=========================================")

    print("\n[Case 1] LIFO Behavior")
    s = Stack()
    s.push(1)
    print("  > Pushed: 1")
    s.push(2)
    print("  > Pushed: 2")
    s.push(3)
    print("  > Pushed: 3")
    
    print(f"  > Top: {s.top()} (Should be 3)")
    s.pop()
    print("  > Popped")
    print(f"  > Top: {s.top()} (Should be 2)")
    s.pop()
    print("  > Popped")
    print(f"  > Top: {s.top()} (Should be 1)")
    
    print(f"  > Size: {s.size()}")

    print("\nStatus: SUCCESS")

if __name__ == "__main__":
    run_e2e_test()
