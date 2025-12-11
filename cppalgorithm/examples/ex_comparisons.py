import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from cppalgorithm import (
    mismatch, equal, is_permutation, lexicographical_compare
)

def main():
    print("--- Comparison Algorithms Demo ---")
    
    seq1 = [1, 2, 3, 4, 5]
    seq2 = [1, 2, 9, 4, 5]
    
    # Mismatch
    idx1, idx2 = mismatch(seq1, seq2)
    print(f"\nMismatch between {seq1} and {seq2}:")
    print(f"Indices: {idx1}, {idx2}")
    print(f"Values: {seq1[idx1]}, {seq2[idx2]}")
    
    # Equal
    print(f"\nEqual [1,2,3] vs [1,2,3]: {equal([1,2,3], [1,2,3])}")
    print(f"Equal [1,2,3] vs [1,2]:   {equal([1,2,3], [1,2])}")
    
    # Is Permutation
    p1 = [1, 2, 3]
    p2 = [3, 1, 2]
    p3 = [1, 2, 2]
    print(f"\nIs {p2} a permutation of {p1}? {is_permutation(p1, p2)}")
    print(f"Is {p3} a permutation of {p1}? {is_permutation(p1, p3)}")
    
    # Lexicographical Compare
    s1 = [1, 2, 3]
    s2 = [1, 2, 4]
    print(f"\nLexicographical Compare {s1} < {s2}: {lexicographical_compare(s1, s2)}")
    print(f"Lexicographical Compare {s2} < {s1}: {lexicographical_compare(s2, s1)}")

if __name__ == "__main__":
    main()
