from typing import IO
from .string import String

def getline(input_stream: IO[str], s: String, delimiter: str = '\n') -> IO[str]:
    """
    Reads characters from input_stream and stores them into string s until delimiter is found.
    The delimiter is NOT included in s.
    Returns the input_stream.
    """
    s.clear()
    
    # Read char by char to handle custom delimiter
    # This might be slow but mimics generic getline behavior
    
    while True:
        char = input_stream.read(1)
        if not char:
            break
        if char == delimiter:
            break
        s.push_back(char)
        
    return input_stream
