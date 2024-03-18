import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--width", type=int, default=960)
    parser.add_argument("--height", type=int, default=540)
    parser.add_argument("--fps", type=int, default=30)
    parser.add_argument("--save", type=bool, default=False)
    parser.add_argument("--lookup", type=bool, default=True)
    parser.add_argument("--display", type=bool, default=False)
    return parser.parse_args()