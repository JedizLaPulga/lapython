import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from cppalgorithm import (
    iota, accumulate, partial_sum, adjacent_difference
)

def main():
    print("--- Numeric Algorithms Demo ---")
    
    # 1. Iota (Sequence generation)
    data = [0] * 5
    iota(data, 1)
    print(f"Iota(1):      {data}")
    
    # 2. Accumulate (Sum)
    total = accumulate(data, 0)
    print(f"Sum:          {total}")
    
    # 3. Partial Sum (Prefix Sum)
    prefix_sums = []
    partial_sum(data, prefix_sums.append)
    print(f"Prefix Sums:  {prefix_sums}")
    
    # 4. Adjacent Difference
    # Recover original from prefix sums
    diffs = []
    adjacent_difference(prefix_sums, diffs.append)
    print(f"Recovered:    {diffs}")
    
    # 5. Factorial using accumulate
    import operator
    nums = [1, 2, 3, 4, 5]
    factorial = accumulate(nums, 1, operator.mul)
    print(f"5! (Product): {factorial}")

if __name__ == "__main__":
    main()
