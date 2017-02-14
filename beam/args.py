import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        description='Flexible Docker Service Discovery')
    parser.add_argument('--drivers', nargs='+')
    parser.add_argument('--internal', dest='internal', action='store_true')
    parser.add_argument('--socket', action="store", dest="socket")

    parser.set_defaults(internal=False)
    parser.set_defaults(socket="/tmp/docker.sock")

    return parser.parse_args()
