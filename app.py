#!/usr/bin/env python3
"""
Entry point for Hugging Face Spaces deployment
"""

import os
import sys

# Ensure prod_rag package is importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import and launch the Gradio app
from prod_rag.gradio.app import demo

if __name__ == "__main__":
    demo.launch()
