import importlib
import env

def super_getattr(structure, *attr_name):
    name = attr_name[0]

    try:
        v = structure.__getattribute__(name)
    except AttributeError:
        v = structure.__getattr__(name)
    
    if len(attr_name) == 1:
        return v
    else:
        return super_getattr(v, *attr_name[1:])

def python_env() -> env.Env:
    e = env.Env()
    e.update({
        "py": eval,
        ".": super_getattr,
        ".=": lambda x, y, v: x.__setattr__(y, v),
        "[]": lambda x, y: x.__getitem__(y),
        "[]=": lambda x, y, v: x.__setitem__(y, v),
        "py_import": importlib.import_module
    })
    return e