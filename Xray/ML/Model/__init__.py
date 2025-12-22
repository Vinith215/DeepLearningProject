# Compatibility shim: expose the contents of the original `Model` package
# so imports using `Xray.ml.model` (lowercase) continue to work on all platforms.
from Xray.ml.Model.arch import Net

__all__ = ["Net"]
