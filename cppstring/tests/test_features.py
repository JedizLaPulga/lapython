import pytest
import io
from cppstring import String, StringView, to_string, stoi, stof, getline

def test_comparisons():
    s1 = String("apple")
    s2 = String("banana")
    s3 = String("apple")
    
    assert s1 == s3
    assert s1 != s2
    assert s1 < s2
    assert s2 > s1
    assert s1 <= s3
    assert s1 >= s3
    
    # Compare with native str
    assert s1 == "apple"
    assert s1 < "banana"
    assert s1 != "banana"

def test_predicates():
    s = String("hello world")
    
    assert s.starts_with("hello")
    assert s.starts_with(String("hel"))
    assert not s.starts_with("world")
    
    assert s.ends_with("world")
    assert s.ends_with(String("rld"))
    assert not s.ends_with("hello")
    
    assert s.contains("lo wo")
    assert s.contains("hello")
    assert not s.contains("bloop")

def test_string_view():
    s = String("hello world")
    sv = StringView(s)
    
    assert len(sv) == 11
    assert str(sv) == "hello world"
    assert sv.at(0) == 'h'
    
    # Substring view
    sv2 = StringView(s, 6)
    assert str(sv2) == "world"
    
    sv3 = StringView(s, 0, 5)
    assert str(sv3) == "hello"
    
    # Modifying string view
    sv3.remove_prefix(1)
    assert str(sv3) == "ello"
    
    sv3.remove_suffix(1)
    assert str(sv3) == "ell"
    
    # View over native string
    sv_nat = StringView("native")
    assert str(sv_nat) == "native"
    assert sv_nat.starts_with("nat")
    
    # Slicing
    sv_slice = sv[0:5]
    assert str(sv_slice) == "hello"

def test_conversions():
    s = to_string(123)
    assert s == "123"
    assert isinstance(s, String)
    
    val = stoi(String("456"))
    assert val == 456
    
    f = stof("3.14")
    assert abs(f - 3.14) < 0.0001
    
    f2 = stof(String("2.5"))
    assert f2 == 2.5

def test_getline():
    data = "line1\nline2\nline3"
    stream = io.StringIO(data)
    
    s = String()
    getline(stream, s)
    assert s == "line1"
    
    getline(stream, s)
    assert s == "line2"
    
    # custom delimiter
    stream2 = io.StringIO("part1;part2")
    s2 = String()
    getline(stream2, s2, ';')
    assert s2 == "part1"
    
    getline(stream2, s2, ';') # Should match end of file logic
    assert s2 == "part2"

def test_advanced_searches():
    s = String("hello world")
    
    # find_first_of
    assert s.find_first_of("aeiou") == 1 # 'e'
    assert s.find_first_of("xyz") == -1
    assert s.find_first_of("rl", 5) == 8 # 'r' at 8 in "world" (pos 6 is 'w', 7 'o', 8 'r')
    
    # find_last_of
    assert s.find_last_of("aeiou") == 7 # 'o' in world
    assert s.find_last_of("l") == 9 # 'l' in world
    assert s.find_last_of("l", 5) == 3 # 'l' in hello
    
    # find_first_not_of
    s2 = String("look")
    assert s2.find_first_not_of("ol") == 3 # 'k'
    
    # find_last_not_of
    assert s2.find_last_not_of("ok") == 0 # 'l'

def test_case_conversions():
    s = String("Hello World")
    s.to_lower()
    assert s == "hello world"
    
    s.to_upper()
    assert s == "HELLO WORLD"
    
    # Test expansion
    s_german = String("mß")
    s_german.to_upper()
    assert s_german == "MSS" # 'ß' -> 'SS'
    assert len(s_german) == 3
