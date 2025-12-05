from vector import Vector

def main():
    v = Vector()
    
    print("=== Vector Tests ===")
    print("Empty:", v.empty(), "| Size:", v.size(), "| Capacity:", v.capacity())
    
    # Push some values
    for i in range(10):
        v.push_back(i * 10)
        print(f"push_back({i*10}) -> size: {v.size()}, capacity: {v.capacity()}")

    print("Vector contents:", v)
    print("v[5]:", v[5])
    print("v[-1]:", v[-1])  # supports negative indexing

    # Modify
    v[3] = 999
    print("After v[3] = 999:", v)

    # Pop
    print("Popped:", v.pop_back())
    print("After pop ->", v)

    # Iteration
    print("Iterating:")
    for value in v:
        print("  ", value)

    # Clear
    v.clear()
    print("After clear -> size:", v.size(), "empty:", v.empty())

if __name__ == "__main__":
    main()