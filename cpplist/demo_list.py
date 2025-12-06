import sys
import os

# Ensure we can import the local package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from cpplist.list import List

def run_e2e_test():
    print("=========================================")
    print("      cpplist demonstration Test")
    print("=========================================")

    print("\n[Case 1] Initialization & Pushing")
    my_list = List()
    print(f"  > Created empty list: {my_list}")
    
    print("  > push_back(10)")
    my_list.push_back(10)
    print("  > push_back(20)")
    my_list.push_back(20)
    print(f"  > Current List: {my_list} (Size: {my_list.size()})")
    
    print("  > push_front(5)")
    my_list.push_front(5)
    print(f"  > Current List: {my_list}")

    print("\n[Case 2] Accessors")
    print(f"  > front(): {my_list.front()}")
    print(f"  > back():  {my_list.back()}")

    print("\n[Case 3] Modification (Insert/Erase)")
    print("  > insert(1, 99) -> Insert 99 at index 1")
    my_list.insert(1, 99)
    print(f"  > Result: {my_list}")
    
    print("  > erase(1) -> Erase element at index 1")
    my_list.erase(1)
    print(f"  > Result: {my_list}")

    print("\n[Case 4] Popping")
    val = my_list.pop_back()
    print(f"  > pop_back() -> returned {val}")
    print(f"  > List after pop: {my_list}")

    print("\n[Case 5] Swapping with another list")
    other_list = List(['A', 'B', 'C'])
    print(f"  > List A (mine):  {my_list}")
    print(f"  > List B (other): {other_list}")
    print("  > Performing swap...")
    my_list.swap(other_list)
    print(f"  > List A (mine):  {my_list}")
    print(f"  > List B (other): {other_list}")

    print("\n[Case 6] Iteration Loop")
    print("  > Elements in List A: ", end="")
    for item in my_list:
        print(f"[{item}]", end="->")
    print("END")

    print("\nStatus: SUCCESS - All print tests completed.")

if __name__ == "__main__":
    run_e2e_test()
