import time
import os

# ASCII art digits as lists of strings (each string is a line)
digits = {
    '0': ["  ___  ",
          " / _ \\ ",
          "| | | |",
          "| | | |",
          "| |_| |",
          " \\___/ "],
    '1': [" __ ", 
          "/_ |",
          " | |",
          " | |",
          " | |",
          " |_|"],
    '2': [" ___  ",
          "|__ \\ ",
          "   ) |",
          "  / / ",
          " / /_ ",
          "|____|"],
    '3': [" ____  ",
          "|___ \\ ",
          "  __) |",
          " |__ < ",
          " ___) |",
          "|____/ "],
    '4': [" _  _   ",
          "| || |  ",
          "| || |_ ",
          "|__   _|",
          "   | |  ",
          "   |_|  "],
    '5': [" _____ ",
          "| ____|",
          "| |__  ",
          "|___ \\ ",
          " ___) |",
          "|____/ "],
    '6': ["   __  ",
          "  / /  ",
          " / /_  ",
          "| '_ \\ ",
          "| (_) |",
          " \\___/ "],
    '7': [" ______",
          "|____  |",
          "    / / ",
          "   / /  ",
          "  / /   ",
          " /_/    "],
    '8': ["  ___  ",
          " ( _ ) ",
          " / _ \\ ",
          "| (_) |",
          " > _ < ",
          "|____/ "],
    '9': ["  ___  ",
          " / _ \\ ",
          "| (_) |",
          " \\__, |",
          "   / / ",
          "  /_/  "],
    ':': ["   ",
          " _ ",
          "(_)",
          " _ ",
          "(_)",
          "   "]
}

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_ascii_time(t):
    # t is a string like "00:10"
    lines = ['' for _ in range(6)]
    for char in t:
        for i in range(6):
            lines[i] += digits[char][i] + '  '
    print('\n'.join(lines))

def timer(seconds):
    for remaining in range(seconds, -1, -1):
        clear()
        mins, secs = divmod(remaining, 60)
        time_str = f"{mins:02}:{secs:02}"
        print_ascii_time(time_str)
        time.sleep(1)

if __name__ == "__main__":
    duration = 65  # countdown 10 seconds for demo; change as needed
    timer(duration)
