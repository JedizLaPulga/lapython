import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from cppalgorithm import (
    remove, remove_if, unique, reverse, rotate, 
    shuffle, partition, stable_partition,
    next_permutation
)

def main():
    print("--- Modifying Algorithms Demo ---")

    # 1. Remove & Unique (Shift logic)
    data = [1, 2, 3, 1, 2, 3, 1, 2, 3]
    print(f"\nOriginal: {data}")
    
    # Remove all 1s
    new_end = remove(data, 1)
    print(f"After remove(1): {data[:new_end]} (logical end: {new_end})")
    
    # Remove odds
    data2 = [1, 2, 3, 4, 5, 6]
    new_end2 = remove_if(data2, lambda x: x % 2 != 0)
    print(f"After remove_if(odd): {data2[:new_end2]}")
    
    # Unique
    data3 = [1, 1, 2, 2, 3, 1, 1]
    new_end3 = unique(data3)
    print(f"Original with dupes: [1, 1, 2, 2, 3, 1, 1]")
    print(f"After unique: {data3[:new_end3]}")
    
    # 2. Reordering
    data4 = [1, 2, 3, 4, 5]
    rotate(data4, 2)
    print(f"\nRotated by 2: {data4}")
    
    reverse(data4)
    print(f"Reversed: {data4}")
    
    shuffle(data4)
    print(f"Shuffled: {data4}")
    
    # 3. Partitioning
    data5 = [1, 2, 3, 4, 5, 6, 7, 8]
    print(f"\nTo Partition (evens first): {data5}")
    split = partition(data5, lambda x: x % 2 == 0)
    print(f"Partitioned: {data5} (split at {split})")
    print(f"Evens: {data5[:split]}, Odds: {data5[split:]}")
    
    # 4. Permutations
    p = [1, 2, 3]
    print(f"\nPermutations of {p}:")
    # Start loop
    while True:
        print(p)
        if not next_permutation(p):
            break

if __name__ == "__main__":
    main()
