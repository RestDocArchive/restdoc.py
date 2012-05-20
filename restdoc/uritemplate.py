from urllib import quote
op_table = {}

def expand_template(source, context):
    end = len(source)
    ret = ""
    i = 0
    while i < end:
        c = source[i]
        if c == '{':
            j = i
            while source[j] != '}':
                j += 1
            ret += expand_expression(source[i + 1:j], data)
            i = j
        else:
            ret += c
        i += 1
    return ret

def expand_expression(expr, data):
    if expr[0] in op_table:
        expr_type = op_table[expr[0]]
        expr = expr[1:]
    else:
        expr_type = SimpleExpr
    
    return expr_type.expand(expr.split(','), data)
    

class SimpleExpr(object):
    glue   = ','
    leader = ''

    @classmethod
    def expand(cls, names, data):
        expanded = []
        for name in names:
            explode = name[-1] == '*'
            if explode: name = name[:-1] 
            if name in data:
                expanded.append(cls.expand_name(name, data[name], explode))
        return cls.leader + cls.glue.join(expanded)

    @classmethod
    def expand_name(cls, name, data, explode):
        # Expand keys types
        try:
            if hasattr(data, 'items'): items = data.items()
            else: items = data
            return cls.expand_pairs(name, items, explode)
        except TypeError: pass
        except ValueError: pass

        # Expand list types
        if not isinstance(data, basestring):
            try:
                return cls.expand_list(name, data, explode)
            except TypeError: pass
            except ValueError: pass

        return cls.expand_one(name, data)

    @classmethod
    def expand_one(cls, name, data):
        return cls.escape(data)

    @classmethod
    def expand_pairs(cls, name, data, explode):
        glue = explode and cls.glue or ','
        pairglue = explode and '=' or ','
        #import pdb; pdb.set_trace();
        return glue.join(pairglue.join([k, cls.escape(v)]) for k, v in data)
    
    @classmethod
    def expand_list(cls, name, data, explode):
        items = (cls.escape(v) for v in data)
        glue = explode and cls.glue or ','
        return glue.join(cls.escape(i) for i in items)

    @staticmethod
    def escape(value):
        return quote(str(value), safe=",")

class ReservedExpr(SimpleExpr):
    @staticmethod
    def escape(value): return str(value)

class FragmentExpr(SimpleExpr):
    leader = "#"

class LabelExpr(SimpleExpr):
    glue   = '.'
    leader = '.'

class PathSegmentExpr(SimpleExpr):
    glue   = '/'
    leader = '/'

class KeepNameMixin(object):
    @classmethod
    def expand_one(cls, name, data):
        return name + '=' + cls.escape(data)
    
    @classmethod
    def expand_list(cls, name, data, explode):
        expanded = super(KeepNameMixin, cls).expand_list(name, data, explode)
        if explode: return expanded
        return name + '=' + expanded

    @classmethod
    def expand_pairs(cls, name, data, explode):
        expanded = super(KeepNameMixin, cls).expand_pairs(name, data, explode)
        if explode: return expanded
        return name + '=' + expanded

class PathParamExpr(KeepNameMixin, SimpleExpr):
    leader = ';'
    glue   = ','

class QueryExpr(KeepNameMixin, SimpleExpr):
    leader = '?'
    glue   = '&'

class QueryContinuationExpr(QueryExpr):
    leader = '&'

for cls in (QueryContinuationExpr, QueryExpr, PathParamExpr, PathSegmentExpr, LabelExpr, SimpleExpr):
    op_table[cls.leader] = cls

op_table['+'] = ReservedExpr
