import subprocess
import os

def convert_epub_to_azw3(epub_path, azw3_path):
    """
    Convert an EPUB book to AZW3 format using Calibre's ebook-convert tool.
    
    Parameters:
        epub_path (str): The path to the EPUB file.
        azw3_path (str): The path to save the converted AZW3 file.
    """
    # Check if the input file exists
    if not os.path.exists(epub_path):
        raise FileNotFoundError(f"The file {epub_path} does not exist.")
    
    # Create the output directory if it doesn't exist
    os.makedirs(os.path.dirname(azw3_path), exist_ok=True)
    
    # Command to convert EPUB to AZW3
    cmd = ['content', epub_path, azw3_path]
    
    try:
        # Execute the command
        subprocess.run(cmd, check=True)
        print(f"Conversion successful: {epub_path} -> {azw3_path}")
    except subprocess.CalledProcessError as e:
        print(f"Conversion failed: {str(e)}")

# Example usage:
# convert_epub_to_azw3('path_to_your_book.epub', 'path_to_save_converted_book.azw3')