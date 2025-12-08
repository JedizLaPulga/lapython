import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from cppalgorithm import sort, is_sorted, binary_search, lower_bound, upper_bound

def main():
    print("--- Sorting & Binary Search Demo ---")
    
    # 1. Sorting
    data = [42, 10, 5, 100, 3, 22]
    print(f"Original: {data}")
    print(f"Is sorted? {is_sorted(data)}")
    
    sort(data)
    print(f"Sorted:   {data}")
    print(f"Is sorted? {is_sorted(data)}")
    
    # 2. Binary Search
    target = 22
    if binary_search(data, target):
        print(f"Found {target} using binary search!")
    
    # 3. Bounds
    # Insert new element maintaining order
    new_val = 15
    idx = lower_bound(data, new_val)
    print(f"To insert {new_val} while keeping order, place at index {idx}")
    
    data.insert(idx, new_val)
    print(f"Inserted: {data}")

if __name__ == "__main__":
    main()
