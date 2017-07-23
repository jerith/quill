
""" This is the main interpreter file that contains bytecode
dispatch loop.
"""

from nolang import opcodes

class InvalidOpcode(Exception):
    def __init__(self, opcode):
        self.opcode = opcode

    def __str__(self):
        try:
            return "<UnimplementedOpcode %s>" % opcodes.opcodes[self.opcode].name
        except IndexError:
            return "<InvalidOpcode %d>" % self.opcode

class UninitializedVariable(Exception):
    pass # XXX add logic to present the error

class Interpreter(object):
    def __init__(self):
        pass

    def interpret(self, space, bytecode, frame):
        index = 0
        arg0 = 0
        arg1 = 0
        bc = bytecode.bytecode
        # make annotator happy
        while True:
            op = ord(bc[index])
            numargs = opcodes.opcodes[op].numargs
            if numargs >= 1:
                arg0 = (ord(bc[index + 1]) << 8) + ord(bc[index + 2])
            elif numargs >= 2:
                arg1 = (ord(bc[index + 3]) << 8) + ord(bc[index + 4])

            if op == opcodes.LOAD_NONE:
                frame.push(space.w_None)
            elif op == opcodes.LOAD_CONSTANT:
                frame.push(bytecode.constants[arg0])
            elif op == opcodes.LOAD_VARIABLE:
                self.load_variable(space, frame, index, arg0)
            elif op == opcodes.LOAD_GLOBAL:
                self.load_global(space, frame, index, arg0)
            elif op == opcodes.LOAD_TRUE:
                frame.push(space.w_True)
            elif op == opcodes.LOAD_FALSE:
                frame.push(space.w_False)
            elif op == opcodes.DISCARD:
                frame.pop()
            elif op == opcodes.ADD:
                self.binop_add(space, frame)
            elif op == opcodes.SUB:
                self.binop_sub(space, frame)
            elif op == opcodes.MUL:
                self.binop_mul(space, frame)
            elif op == opcodes.TRUEDIV:
                self.binop_truediv(space, frame)
            elif op == opcodes.LT:
                self.binop_lt(space, frame)
            elif op == opcodes.EQ:
                self.binop_eq(space, frame)
            elif op == opcodes.STORE:
                frame.store_var(arg0)
            elif op == opcodes.SETATTR:
                self.setattr(space, frame, bytecode, arg0)
            elif op == opcodes.GETATTR:
                self.getattr(space, frame, bytecode, arg0)
            elif op == opcodes.JUMP_IF_FALSE:
                if not space.is_true(frame.pop()):
                    index = arg0
                    continue
            elif op == opcodes.JUMP_IF_TRUE_NOPOP:
                if space.is_true(frame.peek()):
                    index = arg0
                    continue
            elif op == opcodes.JUMP_IF_FALSE_NOPOP:
                if not space.is_true(frame.peek()):
                    index = arg0
                    continue
            elif op == opcodes.JUMP_ABSOLUTE:
                index = arg0
                continue
            elif op == opcodes.CALL:
                self.call(space, frame, index, arg0)
            elif op == opcodes.RETURN:
                return frame.pop()
            else:
                raise InvalidOpcode(op)

            if numargs == 0:
                index += 1
            elif numargs == 1:
                index += 3
            else:
                index += 5

    def load_variable(self, space, frame, bytecode_index, no):
        w_res = frame.locals_w[no]
        if w_res is None:
            raise UninitializedVariable()
        frame.push(w_res)

    def load_global(self, space, frame, bytecode_index, no):
        frame.push(frame.globals_w[no])

    def call(self, space, frame, bytecode_index, no):
        args = [None] * no
        for i in range(no - 1, -1, -1):
            args[i] = frame.pop()
        w_callable = frame.pop()
        frame.push(space.call(w_callable, args))

    def setattr(self, space, frame, bytecode, no):
        w_arg = frame.pop()
        w_lhand = frame.pop()
        space.setattr(w_lhand, space.utf8_w(bytecode.constants[no]), w_arg)

    def getattr(self, space, frame, bytecode, no):
        w_lhand = frame.pop()
        frame.push(space.getattr(w_lhand, space.utf8_w(bytecode.constants[no])))

    def binop_lt(self, space, frame):
        w_right = frame.pop()
        w_left = frame.pop()
        frame.push(space.binop_lt(w_left, w_right))

    def binop_eq(self, space, frame):
        w_right = frame.pop()
        w_left = frame.pop()
        frame.push(space.binop_eq(w_left, w_right))

    def binop_add(self, space, frame):
        w_right = frame.pop()
        w_left = frame.pop()
        frame.push(space.binop_add(w_left, w_right))

    def binop_sub(self, space, frame):
        w_right = frame.pop()
        w_left = frame.pop()
        frame.push(space.binop_sub(w_left, w_right))

    def binop_mul(self, space, frame):
        w_right = frame.pop()
        w_left = frame.pop()
        frame.push(space.binop_mul(w_left, w_right))

    def binop_truediv(self, space, frame):
        w_right = frame.pop()
        w_left = frame.pop()
        frame.push(space.binop_truediv(w_left, w_right))
