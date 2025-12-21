import sys
import os

# Ensure the project's virtual environment site-packages directory (if present)
# is first on sys.path so tests use the environment packages instead of global ones.
ROOT = os.path.dirname(__file__)
ENV_SITE = os.path.abspath(os.path.join(ROOT, "env", "Lib", "site-packages"))
if os.path.isdir(ENV_SITE):
    if ENV_SITE in sys.path:
        sys.path.remove(ENV_SITE)
    sys.path.insert(0, ENV_SITE)

# Filter out other site-packages directories to avoid ImportPathMismatchError when
# different Python installations have the same package (e.g., IPython) installed.
filtered = []
for p in sys.path:
    if not p:
        filtered.append(p)
        continue
    # Normalize path for comparison
    ap = os.path.abspath(p)
    if "site-packages" in ap and ap != ENV_SITE:
        # Skip foreign site-packages
        continue
    filtered.append(p)

sys.path[:] = filtered
