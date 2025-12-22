import importlib, traceback
try:
    m = importlib.import_module('Xray.ml.model.arch')
    print('imported', m)
except Exception:
    traceback.print_exc()
