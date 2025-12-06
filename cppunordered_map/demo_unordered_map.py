import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from cppunordered_map.unordered_map import UnorderedMap

def run_e2e_test():
    print("=========================================")
    print("    cppunordered_map demonstration")
    print("=========================================")

    print("\n[Case 1] Bucket Visualization")
    # Small bucket count to force collisions
    m = UnorderedMap(bucket_count=5)
    
    keys = ["apple", "banana", "cherry", "date", "elderberry", "fig", "grape"]
    print(f"  > Inserting {len(keys)} keys into 5 buckets...")
    for k in keys:
        m[k] = len(k)
        
    print(f"  > Load Factor: {m.load_factor():.2f}")
    
    # Show distribution
    for i in range(m.bucket_count()):
        sz = m.bucket_size(i)
        print(f"    Bucket {i}: {sz} items")

    print(f"\n[Case 2] Access: apple -> {m['apple']}")

    print("\nStatus: SUCCESS")

if __name__ == "__main__":
    run_e2e_test()
