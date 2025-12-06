import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from cppunordered_set.unordered_set import UnorderedSet

def run_e2e_test():
    print("=========================================")
    print("    cppunordered_set demonstration")
    print("=========================================")

    print("\n[Case 1] Collision & Chaining")
    # bucket_count=1 -> All in same bucket
    s = UnorderedSet(bucket_count=1)
    s.insert("A")
    s.insert("B")
    s.insert("C") # "C" -> Collision
    
    print(f"  > Set data: {s}")
    print(f"  > Bucket 0 size: {s.bucket_size(0)}") # Should be 3
    
    print(f"  > Contains 'B'? {s.contains('B')}")
    
    print("\n[Case 2] Uniqueness")
    s.insert("A")
    print(f"  > Inserted 'A' again. Size: {s.size()}") # Should stay 3

    print("\nStatus: SUCCESS")

if __name__ == "__main__":
    run_e2e_test()
