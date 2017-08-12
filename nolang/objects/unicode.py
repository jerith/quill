from rpython.rlib.objectmodel import compute_hash
from rpython.rlib.rstring import StringBuilder

from nolang.error import AppError
from nolang.objects.root import W_Root
from nolang.builtins.spec import TypeSpec, unwrap_spec


class W_StrObject(W_Root):
    def __init__(self, utf8val):
        self.utf8val = utf8val

    def utf8_w(self, space):
        return self.utf8val

    def str(self, space):
        return self.utf8_w(space)

    def hash(self, space):
        return compute_hash(self.utf8val)

    def eq(self, space, w_other):
        try:
            other = space.utf8_w(w_other)
        except AppError as ae:
            if space.type(ae.w_exception) is space.w_typeerror:
                return space.w_NotImplemented
            raise
        return space.newbool(self.utf8val == other)

    def join(self, space, w_list):
        list_w = space.listview(w_list)
        if len(list_w) == 0:
            return space.newtext("")
        sb = StringBuilder()
        sb.append(space.utf8_w(list_w[0]))
        for s in list_w[1:]:
            sb.append(self.utf8val)
            sb.append(space.utf8_w(s))
        return space.newtext(sb.build())


@unwrap_spec(value='str')
def allocate(space, value):
    return space.newtext(value)


W_StrObject.spec = TypeSpec(
    'String',
    allocate,
    methods={
        'join': W_StrObject.join,
    },
    set_cls_w_type=True
)
