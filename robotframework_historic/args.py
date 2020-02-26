import argparse

def parse_options():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    general = parser.add_argument_group("General")

    general.add_argument(
        '-s', '--psqlhost',
        dest='psqlhost',
        default='localhost',
        help="PSQL database host address"
    )

    general.add_argument(
        '-u', '--username',
        dest='username',
        default='postgres',
        help="User name of postgres database"
    )

    general.add_argument(
        '-p', '--password',
        dest='password',
        default='123456',
        help="Password of postgres database"
    )

    general.add_argument(
        '-a', '--apphost',
        dest='apphost',
        default='0.0.0.0',
        help="Flask app host address"
    )

    args = parser.parse_args()
    return args