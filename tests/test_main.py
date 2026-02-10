import os
import sys

# Set the path FIRST before importing your scripts
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.processor import process_images

def test_pipeline_execution():
    # Requirement: Validate image processing outputs [cite: 22, 27]
    process_images()
    assert len(os.listdir('outputs/')) > 0