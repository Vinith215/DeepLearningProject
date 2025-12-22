import importlib, pkgutil, sys, traceback
try:
    import Xray
    print('Xray', Xray.__file__)
    print('Xray path:', list(Xray.__path__))
    print('submodules in Xray:')
    for m in pkgutil.iter_modules(Xray.__path__):
        print(' -', m.name)
    import Xray.ml
    print('Xray.ml imported', Xray.ml.__file__)
    print('ml subpackages:')
    for m in pkgutil.iter_modules(Xray.ml.__path__):
        print('  -', m.name)
except Exception:
    traceback.print_exc()
