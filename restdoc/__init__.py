from textwrap import dedent
METHODS = ['DELETE', 'GET', 'HEAD', 'PATCH', 'POST', 'PUT', 'OPTIONS']

def delegate_http_methods(prefix=''):
    doc = dedent("""
        Make a ``{0}`` request against the server.
        (Delegates to :meth:`%srequest`)
    """ % prefix)


    def make_proxy(cls, name, method):
        request = getattr(cls, prefix+'request')
        def func(*args, **kwargs):
            return request(*args, method=method, **kwargs)
        func.__doc__  = doc.format(method)
        func.__name__ = name
        return func

    def class_decorator(cls):
        for method in METHODS:
            func_name = prefix + method.lower()
            setattr(cls, func_name, make_proxy(cls, func_name, method))
        return cls

    return class_decorator
