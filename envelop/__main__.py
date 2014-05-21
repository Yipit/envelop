import argparse
from envelop import Environment

def main():
    parser = argparse.ArgumentParser(description='Manage your environment.')
    parser.add_argument(
        '-f', '--file', metavar='<FILE>', type=str, action='store',
        help='File to load variables from')
    parser.add_argument(
        '-d', '--directory', metavar='<DIR>', type=str, action='store',
        help='Directory to load variables from, works just like `envparse\'')

    subparsers = parser.add_subparsers(title='subcommands', metavar='COMMAND')
    get_parser = subparsers.add_parser(
        'get',
        help='Get and print out the value of the variable <VAR>')
    get_parser.add_argument('cmd_get')

    get_uri_parser = subparsers.add_parser(
        'get-uri', help='Exposes the URI parser API')
    get_uri_parser.add_argument('cmd_get_uri', nargs=2)

    args = parser.parse_args()

    if args.file:
        env = Environment.from_file(args.file)
    if args.directory:
        env = Environment.from_folder(args.directory)

    if hasattr(args, 'cmd_get'):
        return env.get(args.cmd_get)

    if hasattr(args, 'cmd_get_uri'):
        part, variable = args.cmd_get_uri
        return getattr(env.get_uri(variable), part)


if __name__ == '__main__':
    # Module interface, you can use this function by calling this module using
    # the module launcher of python: `python -m envelop`
    print(main() or '')
