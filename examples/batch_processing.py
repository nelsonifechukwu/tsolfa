#!/usr/bin/env python3
"""
Example of batch processing multiple sheet music files.
"""

import os
from pathlib import Path
from tsolfa import SheetTranscriber

def main():
    # Initialize transcriber
    transcriber = SheetTranscriber()
    
    # Directory containing sheet music images
    sheets_dir = Path("data/sheets")
    
    # Supported image extensions
    image_extensions = {".png", ".jpg", ".jpeg", ".tiff", ".bmp"}
    
    # Find all image files
    image_files = [
        str(f) for f in sheets_dir.iterdir() 
        if f.is_file() and f.suffix.lower() in image_extensions
    ]
    
    if not image_files:
        print(f"No image files found in {sheets_dir}")
        return
    
    print(f"Processing {len(image_files)} sheet music files...")
    
    # Process all files in batch
    results = transcriber.transcribe_batch(image_files)
    
    # Display results
    for i, (file_path, result) in enumerate(zip(image_files, results), 1):
        filename = os.path.basename(file_path)
        print(f"\n[{i}/{len(image_files)}] {filename}")
        print(f"  Key: {result.key_signature}")
        print(f"  Time: {result.time_signature}")
        print(f"  Solfa: {' '.join(result.solfa_notation)}")
        print(f"  Confidence: {result.confidence_score:.2f}")
        print(f"  Time: {result.processing_time:.3f}s")

if __name__ == "__main__":
    main()