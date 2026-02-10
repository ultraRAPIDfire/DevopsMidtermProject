import os
import sys
# Ensures the 'scripts' module is findable by the test runner
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.processor import process_images

def test_pipeline_execution():
    # Requirement: Practice automated tests 
    process_images()
    # Check if the output directory contains processed files [cite: 19, 27]
    files = os.listdir('outputs/')
    assert len(files) > 0