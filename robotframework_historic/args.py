import argparse

def parse_options():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    general = parser.add_argument_group("General")

    general.add_argument(
        '-H', '--host',
        dest='host',
        default='0.0.0.0',
        help="MySQL database URL"
    )

    general.add_argument(
        '-U', '--username',
        dest='username',
        default='superuser',
        help="User name of MySQL database"
    )

    general.add_argument(
        '-P', '--password',
        dest='password',
        default='passw0rd',
        help="Password of MySQL database"
    )

    args = parser.parse_args()
    return args