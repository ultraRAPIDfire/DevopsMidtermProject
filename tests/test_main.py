import os
from scripts.processor import process_images

def test_pipeline_execution():
    # Requirement: Validate automated tests 
    process_images()
    files = os.listdir('outputs/')
    assert len(files) > 0