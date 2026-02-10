import os
import sys
# Ensures the root directory is in the path so 'scripts' is recognized
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.processor import process_images

def test_pipeline_execution():
    # Requirement: Validate image processing logic [cite: 15]
    process_images()
    # Check if the output directory has at least one processed image [cite: 19]
    assert len(os.listdir('outputs/')) > 0