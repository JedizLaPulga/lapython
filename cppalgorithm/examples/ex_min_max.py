import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from cppalgorithm import (
    min_element, max_element, minmax_element, clamp
)

def main():
    print("--- Min/Max & Clamp Demo ---")
    
    data = [10, 50, 20, 5, 40]
    print(f"Data: {data}")
    
    # 1. Min/Max Element
    min_idx = min_element(data)
    max_idx = max_element(data)
    
    print(f"Min element is at index {min_idx} (Value: {data[min_idx]})")
    print(f"Max element is at index {max_idx} (Value: {data[max_idx]})")
    
    # 2. MinMax
    mi, ma = minmax_element(data)
    print(f"minmax_element: indices ({mi}, {ma}) -> values ({data[mi]}, {data[ma]})")
    
    # 3. Clamp
    val = 150
    lo, hi = 0, 100
    clamped = clamp(val, lo, hi)
    print(f"Clamp({val}, {lo}, {hi}) -> {clamped}")
    
    val2 = -50
    print(f"Clamp({val2}, {lo}, {hi}) -> {clamp(val2, lo, hi)}")

if __name__ == "__main__":
    main()
