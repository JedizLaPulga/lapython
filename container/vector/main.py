from vector import Vector

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        return f"P({self.x},{self.y})"

def main():
    print("FULL STL VECTOR IN PYTHON - LEGENDARY EDITION\n")
    
    v = Vector[int]()
    v.reserve(50)
    print(f"Reserved 50 -> capacity: {v.capacity()}")

    for i in range(15):
        v.push_back(i * 10)
    
    print("After push_back:", v)
    print("front:", v.front(), " back:", v.back())
    print("at(5):", v.at(5), "  v[5]:", v[5], "  v[-1]:", v[-1])

    v.emplace_back()  # default int → 0 (simulated)
    print("After emplace_back():", v)

    v.insert(3, 999)
    print("After insert(3, 999):", v)

    v.erase(0, 3)
    print("After erase(0, 3):  ", v)

    v.resize(20, 777)
    print("After resize(20, 777):", v)

    # Slicing!
    print("v[5:15]:", v[5:15])

    # Range-based loop style
    print("\nRange-based loop:")
    for it in v:
        print("  ", it)

    # Custom type test
    print("\nEmplacing custom objects:")
    vp = Vector[Point]()
    vp.emplace_back(Point, 1, 2)
    vp.emplace_back(Point, 3, 4)
    vp.push_back(Point(5, 6))
    print(vp)

    print("\nIterator arithmetic:")
    it = vp.begin() + 1
    print("begin() + 1 ->", next(it))

    v.shrink_to_fit()
    print(f"\nFinal: {v}")
    print(f"Size: {v.size()}, Capacity: {v.capacity()}")

if __name__ == "__main__":
    main()