import sys
import os

# Ensure we can import cppalgorithm from source
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from cppalgorithm import find, count_if, all_of, for_each

def main():
    print("--- Non-Modifying Algorithms Demo ---")
    
    # 1. Working with simple lists
    data = [5, 2, 8, 1, 9, 3, 2, 8]
    print(f"Data: {data}")
    
    # FIND
    target = 9
    idx = find(data, target)
    if idx != -1:
        print(f"Found {target} at index {idx}")
    else:
        print(f"{target} not found")
        
    # COUNT_IF
    threshold = 4
    count = count_if(data, lambda x: x > threshold)
    print(f"Elements greater than {threshold}: {count}")
    
    # ALL_OF
    # Check if all elements are positive
    if all_of(data, lambda x: x > 0):
        print("All elements are positive.")
        
    # FOR_EACH
    print("Printing elements multiplied by 10:")
    for_each(data, lambda x: print(f"{x*10}", end=' '))
    print()

if __name__ == "__main__":
    main()
