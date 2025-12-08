import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from cppalgorithm import (
    merge, set_union, set_intersection,
    set_difference, includes
)

def main():
    print("--- Set Operations Demo (Sorted Ranges) ---")
    
    # Must be sorted!
    A = [1, 2, 4, 8, 16]
    B = [2, 3, 5, 8, 13]
    
    print(f"Set A: {A}")
    print(f"Set B: {B}")
    
    # 1. Merge
    merged = []
    merge(A, B, merged.append)
    print(f"Merge:        {merged}")
    
    # 2. Union
    union = []
    set_union(A, B, union.append)
    print(f"Union:        {union}")
    
    # 3. Intersection
    inter = []
    set_intersection(A, B, inter.append)
    print(f"Intersection: {inter}")
    
    # 4. Difference (A - B)
    diff = []
    set_difference(A, B, diff.append)
    print(f"Diff (A-B):   {diff}")
    
    # 5. Includes
    subset = [2, 8]
    print(f"Is {subset} a subset of A? {includes(A, subset)}")

if __name__ == "__main__":
    main()
