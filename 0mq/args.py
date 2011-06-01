import sys

def main(argv=None):
    """docstring for main"""
    if argv is None:
        for arg in sys.argv:
            print arg


if __name__ == "__main__":
    main()