""" Main declaration of function
"""

from nolang.objects.root import W_Root
from nolang.frameobject import Frame
from nolang.error import ArgumentMismatchError


class W_Function(W_Root):
    def __init__(self, name, bytecode):
        self.name = name
        self.bytecode = bytecode

    def setup(self, space):
        self.bytecode.setup(space)

    def call(self, space, interpreter, args_w):
        frame = Frame(self.bytecode, interpreter.topframeref)
        if len(self.bytecode.arglist) != len(args_w):
            raise ArgumentMismatchError()
        frame.populate_args(args_w)
        return interpreter.interpret(space, self.bytecode, frame)

    def bind(self, space, w_obj):
        return W_BoundMethod(w_obj, self)


class W_BuiltinFunction(W_Root):
    def __init__(self, name, callable, num_args):
        self.name = name
        self.num_args = num_args
        self.callable = callable

    def setup(self, space):
        pass

    def call(self, space, interpreter, args_w):
        if self.num_args != -1 and self.num_args != len(args_w):
            raise ArgumentMismatchError()
        return self.callable(space, args_w)

    def __repr__(self):
        return "<BuiltinFunction %s/%d>" % (self.name, self.num_args)


class W_Property(W_Root):
    def __init__(self, name, getter, setter):
        self.name = name
        self.getter = getter
        self.setter = setter

    def bind(self, space, w_obj):
        return self.getter(w_obj, space)

    def setup(self, space):
        pass


class W_BoundMethod(W_Root):
    def __init__(self, w_self, w_function):
        self.w_self = w_self
        self.w_function = w_function

    def call(self, space, interpreter, args_w):
        return space.call(self.w_function, [self.w_self] + args_w)
