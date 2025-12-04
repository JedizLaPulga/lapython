#!/usr/bin/env python3
# Pure stdlib tiny curses text editor
import curses
import sys
from pathlib import Path

def main(stdscr):
    curses.curs_set(1)
    stdscr.keypad(True)
    curses.raw()
    
    file_path = Path(sys.argv[1] if len(sys.argv) > 1 else "untitled.txt")
    lines = file_path.read_text().splitlines() if file_path.exists() else [""]
    
    y, x = 0, 0
    status = f" {file_path} - {len(lines)} lines "
    
    while True:
        stdscr.erase()
        for i, line in enumerate(lines):
            stdscr.addstr(i, 0, line[:curses.COLS-1])
        stdscr.addstr(curses.LINES-1, 0, status.ljust(curses.COLS), curses.A_REVERSE)
        stdscr.move(y, x)
        
        key = stdscr.getch()
        
        if key in (curses.KEY_EXIT, 24):  # Ctrl-X
            if curses.flash(): pass
            break
        elif key in (curses.KEY_ENTER, 10, 13):
            lines.insert(y + 1, lines[y][x:])
            lines[y] = lines[y][:x]
            y += 1
            x = 0
        elif key == curses.KEY_BACKSPACE or key == 127:
            if x > 0:
                lines[y] = lines[y][:x-1] + lines[y][x:]
                x -= 1
            elif y > 0:
                x = len(lines[y-1])
                lines[y-1] += lines[y]
                del lines[y]
                y -= 1
        elif key == curses.KEY_DC:  # Delete
            lines[y] = lines[y][:x] + lines[y][x+1:]
        elif key == curses.KEY_LEFT:  x = max(0, x-1)
        elif key == curses.KEY_RIGHT: x = min(len(lines[y]), x+1)
        elif key == curses.KEY_UP:    y = max(0, y-1)
        elif key == curses.KEY_DOWN:  y = min(len(lines)-1, y+1)
        elif 32 <= key <= 126:
            lines[y] = lines[y][:x] + chr(key) + lines[y][x:]
            x += 1
    
    if input("\nSave? (y/N): ").strip().lower() == 'y':
        file_path.write_text('\n'.join(lines) + '\n')
        status += "Saved!"

if __name__ == "__main__":
    curses.wrapper(main)