import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from cpppriority_queue.priority_queue import PriorityQueue

def run_e2e_test():
    print("=========================================")
    print("   cpppriority_queue demonstration")
    print("=========================================")

    print("\n[Case 1] Max Heap Behavior")
    pq = PriorityQueue()
    data = [10, 50, 30, 5, 100]
    print(f"  > Pushing: {data}")
    for x in data:
        pq.push(x)

    print("  > Popping (Expect Descending Order):")
    expected = sorted(data, reverse=True)
    count = 0
    while not pq.empty():
        val = pq.top()
        pq.pop()
        print(f"    - {val}")
        if val != expected[count]:
            print("    !!! ERROR: Unexpected value")
        count += 1

    print("\nStatus: SUCCESS")

if __name__ == "__main__":
    run_e2e_test()
