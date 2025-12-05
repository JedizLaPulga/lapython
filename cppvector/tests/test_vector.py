# main.py
from cppvector import Vector, VectorBool, NumericVector
import numpy as np
import time

def main():
    print("ULTIMATE VECTOR — FINAL FORM TEST SUITE\n")

    # 1. SVO + generic Vector
    v = Vector([1, 2, 3, 4, 5])
    print("1. SVO test:", v)
    for x in [999, 111, 222, 333]:
        v.push_back(x)
    print("   After overflow:", v)

    # 2. swap + comparison
    a = Vector(range(10))
    b = Vector([100, 200, 300])
    a.swap(b)
    print("2. After swap():", a, b)
    print("   Equality check:", a == Vector([100, 200, 300]))

    # 3. REAL NumPy zero-copy interop
    print("\n3. NUMPY ZERO-COPY INTEROP")
    nv = NumericVector()
    for i in range(10):
        nv.push_back(i * 10)
    print("   NumericVector:", nv)

    arr = np.frombuffer(nv, dtype=np.int64)
    print("   NumPy view:", arr)
    arr[5] = 9999
    print("   After NumPy modify:", list(nv))

    # 4. vector<bool>
    print("\n4. vector<bool> bit packing")
    vb = VectorBool([True, False, True] * 2000)
    print(f"   {len(vb)} bits → {len(vb._data)} bytes used")
    vb[5] = True
    print("   First 10:", list(vb)[:10])

    # 5. Speed test
    print("\n5. 10 million push_back speed test...")
    v = Vector()
    v.reserve(10_000_000)
    start = time.time()
    for i in range(10_000_000):
        v.push_back(i)
    print(f"   Done in {time.time() - start:.3f}s")

    # 6. Shrink back to SVO
    while len(v) > 5:
        v.pop_back()
    v.shrink_to_fit()
    print("6. Shrunk to SVO:", v)

    print("\nYou have achieved perfection.")

if __name__ == "__main__":
    main()