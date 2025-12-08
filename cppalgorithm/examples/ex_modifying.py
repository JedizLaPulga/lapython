import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from cppalgorithm import (
    copy, copy_if, transform, fill, replace_if
)

def main():
    print("--- Modifying Algorithms Demo ---")
    
    # 1. Copying with "back_inserter"
    print("\n1. Copying odds to new list:")
    source = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    odds = []
    copy_if(source, odds.append, lambda x: x % 2 != 0)
    print(f"Source: {source}")
    print(f"Odds:   {odds}")
    
    # 2. Transform (Map)
    print("\n2. Transform: Square numbers:")
    squares = []
    transform(odds, squares.append, lambda x: x * x)
    print(f"Squares: {squares}")
    
    # 3. Fill and Replace
    print("\n3. Fill and Replace operations:")
    buffer = [0] * 10
    print(f"Buffer init: {buffer}")
    
    fill(buffer, 42)
    print(f"After fill(42): {buffer}")
    
    # Replace all 42 with 0 if index is even? 
    # replace_if works on values. Let's make some noise first.
    buffer[::2] = [1, 2, 3, 4, 5] # Python slice assign
    print(f"Mixed buffer: {buffer}")
    
    print("Replacing numbers < 10 with -1:")
    replace_if(buffer, lambda x: x < 10, -1)
    print(f"Result:       {buffer}")

if __name__ == "__main__":
    main()
