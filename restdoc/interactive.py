from cmd import Cmd
from . import client, delegate_http_methods
import shlex
import argparse
from pprint import pprint

@delegate_http_methods('do_')
class Shell(Cmd, object):
    def __init__(self, *args, **kwargs):
        super(Shell, self).__init__(*args, **kwargs)
        self.prompt = '(disconnected) '

        def kv(arg): return tuple(arg.split('='))

        parser = argparse.ArgumentParser(prog='request', add_help=False)
        parser.add_argument('resource', help="A resource id or path")
        parser.add_argument('-template', nargs='*', type=kv)
        parser.add_argument('-body')
        self.request_parser = parser


    def do_server(self, url):
        """
        Retrieve a RestDoc description from a server and use it as the
        default for all further operations.
        """
        self.client = client.Client(url)
        self.prompt = '({0}) '.format(self.client.root)

    def do_reload(self, _):
        """ Reload the resource index from the server """
        self.client.reload_index()

    def do_resources(self, url):
        """ Display a summary of available resources. """
        from prettytable import PrettyTable
        field_names = ('id', 'path', 'methods', 'description')
        t = PrettyTable(field_names)
        for res in self.client._index.get('resources', []):
            row = [res.get(f) for f in field_names]
            row[2] = row[2].keys()
            t.add_row(row)
        print(t)

    def do_request(self, params, method=None):
        """ Send a request and print out the response body. """
        args = self.request_parser.parse_args(shlex.split(params))
        if method is None:
            method = args.X
        tpl_vars = dict(args.template or [])
        res = self.client.request(method, args.resource, tpl_vars)
        print("{0.status} {0.reason}".format(res))
        for header in res.headers.iteritems():
            print("{0}: {1}".format(*header))
        print
        print res.read()

    def help_request(self):
        return self.request_parser.print_help()

    def do_doc(self, resource_id):
        """ Print out the full description of a resource. """
        try:
            pprint(self.client.get_resource(resource_id))
        except KeyError as e:
            print e.message


def main():
    import sys
    import argparse
    from textwrap import dedent
    ic = Shell()
    if len(sys.argv) > 1:
        ic.do_server(sys.argv[1])
    ic.cmdloop(dedent("""
    Welcome to the RestDoc shell!
    Use the 'server' command to specify a server, or 'help' to see all commands."""
    ))


if __name__ == '__main__': main()
