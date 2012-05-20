import re
from textwrap import dedent

import urllib3

from . import delegate_http_methods

try:
    import simplejson as json
except ImportError:
    import json

from .uritemplate import expand_template

@delegate_http_methods()
class Client(object):
    """
    A client reads the JSON RestDoc index on instantiation and
    installs methods on itself for each named route.
    """
    def __init__(self, root, index=None, **kw):
        if root[-1] == '/': root = root[:-1]
        self.root = root
        headers = kw.setdefault('headers', {})
        headers.setdefault('Content-Type', 'application/json')
        self.reload_index(**kw)

    def reload_index(self, **kw):
        self.conn = urllib3.connection_from_url(self.root, **kw)
        c = self.conn._get_conn()
        c.request('OPTIONS', '/*', headers={'Accept': 'application/json'})
        res = c.getresponse()
        body = res.read()
        self._index = json.loads(body)
        self.conn._put_conn(c)

    def request(self, method, resource, template_vars=None, **kw):
        href = self.resolve_href(resource, template_vars)
        res = self.conn.request(method, href, **kw)
        return res

    def resolve_href(self, resource_id, template_vars):
        if resource_id[0] == '/':
            path = expand_template(resource_id, template_vars)
        else:
            path = self.get_resource(resource_id).get('path')
        return expand_template(path, template_vars)

    def get_resource(self, resource_id):
        for resource in self._index.get('resources', []):
            if resource.get('id') == resource_id:
                return resource
        raise KeyError("Unknown resource id: %s" % resource_id)
