#!/usr/bin/env python3
"""
Basic example of transcribing sheet music to solfa notation.
"""

from tsolfa import SheetTranscriber

def main():
    # Initialize the transcriber
    transcriber = SheetTranscriber()
    
    # Example sheet music path (replace with actual path)
    sheet_path = "data/sheets/example_sheet.png"
    
    try:
        # Transcribe the sheet music
        print(f"Transcribing: {sheet_path}")
        result = transcriber.transcribe(sheet_path)
        
        # Display results
        print(f"Key Signature: {result.key_signature}")
        print(f"Time Signature: {result.time_signature}")
        print(f"Solfa Notation: {' '.join(result.solfa_notation)}")
        print(f"Confidence: {result.confidence_score:.2f}")
        print(f"Processing Time: {result.processing_time:.3f}s")
        
    except Exception as e:
        print(f"Transcription failed: {e}")

if __name__ == "__main__":
    main()