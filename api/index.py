import os
import sys

# Ensure root directory is on Python path for serverless invocation
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from main import app, handler

# Export for Vercel Serverless
__all__ = ["app", "handler"]
