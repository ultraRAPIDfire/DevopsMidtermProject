import os
import sys
# This adds the current directory to the system path so it can find 'scripts'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.processor import process_images

def test_if_outputs_exist():
    # Requirement: Automatically detect image files [cite: 17]
    process_images()
    assert len(os.listdir('outputs/')) > 0