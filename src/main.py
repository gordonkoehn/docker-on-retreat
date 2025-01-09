""" This is the main script that does the heavy computation """

import os
import numpy as np
import pyfiglet as figlet
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

input_fp = os.getenv("INPUT_FP", "in/input.csv")
output_fp = os.getenv("OUTPUT_FP", "out/output.txt")

def main():
    ### Load the data
    data = np.genfromtxt(input_fp, delimiter=',')
    
    ### Heavy computation
    result = np.sum(data)

    ### Output Wrangling / Formatting (totally useless)
    summation = " + ".join([str(x) for x in data])
    ascii_banner = figlet.figlet_format(summation + f" = {result}")

    #### Save the result - to a file and print it
    print(ascii_banner)
    with open(output_fp, "w") as f:
        f.write(ascii_banner)


if __name__ == "__main__":
    main()