import importlib, traceback
try:
    m = importlib.import_module('Xray.ml')
    print('imported Xray.ml ->', m)
    print('ml path:', getattr(m, '__path__', None))
except Exception:
    traceback.print_exc()
