import sys
from beam import Beam


def main():
    b = Beam(sys.argv[1:])
    while True:
        b.run()


if __name__ == "__main__":
    main()
