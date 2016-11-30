#!/usr/bin/env python

import sys

def main():
    if len(sys.argv) > 1:
        print(sys.argv[1:])
    else:
        std_in = sys.stdin.readline().split()
        if len(std_in) > 1:
            print(std_in)
        else:
            print("no arguments")

if __name__ == "__main__":
    main()