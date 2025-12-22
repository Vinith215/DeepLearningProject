"""Compatibility shim to allow imports like `Xray.ml.model` even though
this project stores the package under `Xray/ML` (uppercase).

This module sets a package __path__ pointing to the `ML` directory so that
subpackages such as `model` (case-insensitive on Windows) can be imported.
"""
import os

# Make this module act like a package by giving it a __path__ that points to
# the existing `ML` directory. This allows `import Xray.ml.model.arch` to work.
__path__ = [os.path.join(os.path.dirname(__file__), "ML")]

# For convenience, re-export the Model package if someone imports Xray.ml
try:
    from Xray.ML import Model  # type: ignore
    __all__ = ["Model"]
except Exception:
    __all__ = []
