import os
import argparse
from .rfhistoricupdate import rfhistoric_update
from robot.api import ExecutionResult


def parse_options():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    general = parser.add_argument_group("Update")

    general.add_argument(
        '-s', '--host',
        dest='host',
        default='localhost',
        help="MySQL hosted address"
    )

    general.add_argument(
        '-u', '--username',
        dest='username',
        default='root',
        help="MySQL root username"
    )

    general.add_argument(
        '-p', '--password',
        dest='password',
        default='123456',
        help="MySQL root password"
    )

    args = parser.parse_args()
    return args


def main():
    args = parse_options()
    rfhistoric_update(args)