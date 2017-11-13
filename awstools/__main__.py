import sys
import argparse
from ecs import ECS

def main(args=None):
    if args is None:
        parser = argparse.ArgumentParser(description="awstools")
        subparsers = parser.add_subparsers(help='sub-command help')
        # add subcommmands by importing class and adding subparser
        ECS.config_parser(subparsers)
        # ...
        args = parser.parse_args()
        args.func(args)

if __name__ == "__main__":
    main()
