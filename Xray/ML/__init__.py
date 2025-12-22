# Compatibility shim to make `Xray.ml` available regardless of dir name casing.
# The real package lives in `Xray.ML` (uppercase); this file ensures imports using
# `Xray.ml` (lowercase) succeed on all platforms.

# Nothing to expose here; the presence of this file makes `Xray.ml` a package
# and enables `Xray.ml.model` (created separately) to be importable.
