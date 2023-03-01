import time
import colorama
from colorama import Fore, Back, Style
import os
import random

# Initialize colorama
colorama.init()
t = 1/30
def color_changer(text : str, start_colors : list[str], end_colors : list[str]) -> None:
    """
    Gradually change the color of a text

    Parameters
    ----------
    text : str
        The text to change the color

    start_colors : list[str]
        The starting colors as RGB tuples for each character

    end_colors : list[str]
        The ending colors as RGB tuples for each character
    """
    # Convert the text to a list of lines
    lines = text.split('\n')

    # Calculate the maximum number of characters in a line
    max_chars = max([len(line) for line in lines])

    # Pad the lines with spaces to have the same number of characters
    for i in range(len(lines)): 
        lines[i] = lines[i].ljust(max_chars)

    # Gradually change the color from start_colors to end_colors for each character
    steps = 20


    for i in range(steps):
        # Clear the previous lines
        os.system('clear')
        for line in lines:
            for j in range(len(line)):
                # Calculate the current color as an RGB tuple for the current character
                r = int((steps - i) / steps * start_colors[j % len(start_colors)][0] + i / steps * end_colors[j % len(end_colors)][0])
                g = int((steps - i) / steps * start_colors[j % len(start_colors)][1] + i / steps * end_colors[j % len(end_colors)][1])
                b = int((steps - i) / steps * start_colors[j % len(start_colors)][2] + i / steps * end_colors[j % len(end_colors)][2])
                current_color = f"\033[38;2;{r};{g};{b}m"

                # Print the colored character without newline
                print(f"{current_color}{line[j]}{Style.RESET_ALL}", end='')

            # Print a newline after each line
            print()
        
        time.sleep(t)  # Add a small delay to slow down the color change


def loop_back_and_forth(text : str, start_colors : list[str], end_colors : list[str]) -> None:
    """
    Gradually change the color of a text and then loop back and forth

    Parameters
    ----------
    text : str
        The text to change the color

    start_colors : list[str]
        The starting colors as RGB tuples for each character

    end_colors : list[str]
        The ending colors as RGB tuples for each character
    """

    while True:
        color_changer(text, start_colors, end_colors)

        # Reverse the start and end colors
        start_colors, end_colors = end_colors, start_colors
    
if __name__ == "__main__":
    text = "ΣΔAΩ" 
    s = [(random.randint(0, 255), 0, 0) for _ in range(len(text))]
    while True:      
        e = [(random.randint(0, 255), 0, 0) for _ in range(len(text))]
        color_changer(text,s,e)
        s = e
        




