from .func_registry import add_func

class Var:
    def __init__(self, context, ssa_val):
        self._context = context
        self._ssa_val = ssa_val

    @property
    def shape(self):
        return self._shape(self._context, self._ssa_val)

    @property
    def dtype(self):
        return self._dtype(self._context, self._ssa_val)

    def __len__(self):
        return self._len(self._context, self._ssa_val)

    def __getitem__(self, index):
        return self._getitem(self._context, self._ssa_val, index)

    def __mul__(self, o): return self._binop(self._context, self._ssa_val, o, '*')
    def __rmul__(self, o): return self._binop(self._context, self._ssa_val, o, '*')

class Type:
    def __init__(self, mlir_type, eq):
        self._mlir_type = mlir_type
        self._eq = eq

    def __eq__(self, other):
        return self._eq(self._mlir_type, other._mlir_type)

def is_literal(val):
    return not isinstance(val, Var)

class Builder:
    def __init__(self, context):
        self._context = context

    def broadcast(self, *args):
        return self._broadcast(self._context, args)

    def init_tensor(self, shape, dtype, init_val=None):
        return self._init_tensor(self._context, shape, dtype, init_val)

    def fill_tensor(self, tensor, value):
        return self._fill_tensor(self._context, tensor, value)

    def generic(self, inputs, outputs, iterators, maps, body):
        return self._generic(self._context, inputs, outputs, iterators, maps, body)

    def from_elements(self, values, dtype):
        return self._from_elements(self._context, values, dtype)

    def extract(self, value, indices):
        return self._extract(self._context, value, indices)

    def reshape(self, src, num_dims, affine_maps):
        return self._reshape(self._context, src, num_dims, affine_maps)

def compile_func(*args, **kwargs):
    import numba.mlir.inner_compiler
    return numba.mlir.inner_compiler.compile_func(*args, **kwargs)

_func_registry = {}

def register_func(name, orig_func = None):
    def _decorator(func):
        global _func_registry
        mangled_name = name + '()'
        assert not mangled_name in _func_registry
        _func_registry[mangled_name] = func
        if not orig_func is None:
            add_func(orig_func, name)
        return func
    return _decorator

def register_attr(name):
    def _decorator(func):
        global _func_registry
        assert not name in _func_registry
        _func_registry[name] = func
        return func
    return _decorator

def lookup_func(name):
    global _func_registry
    return _func_registry.get(name)