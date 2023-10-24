import os
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

def save_to_file(file_obj, folder='content/temp'):
    # Ensure the folder exists
    os.makedirs(folder, exist_ok=True)

    # Create a file path based on the file object's name attribute
    # or use a default name if the name attribute does not exist
    file_name = getattr(file_obj, 'name', 'temp_file.epub')
    file_path = os.path.join(folder, os.path.basename(file_name))

    # Ensure the file object is at the beginning of the file
    file_obj.seek(0)

    # Write the content of the file object to the file path
    with open(file_path, 'wb') as f:
        f.write(file_obj.read())

    return file_path

blacklist = [
	'[document]',
	'noscript',
	'header',
	'html',
	'meta',
	'head', 
	'input',
	'script',
	# there may be more elements you don't want, such as "style", etc.
]

def epub2thtml(epub_path):
    book = epub.read_epub(epub_path)
    chapters = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            chapters.append(item.get_content())
    return chapters

def chap2text(chap):
    output = ''
    soup = BeautifulSoup(chap, 'html.parser')
    text = soup.find_all(text=True)
    for t in text:
        if t.parent.name not in blacklist:
            output += '{} '.format(t)
    return output

def thtml2ttext(thtml):
    Output = []
    for html in thtml:
        text =  chap2text(html)
        Output.append(text)
    return Output

def epub2text(epub_path):
    chapters = epub2thtml(epub_path)
    print(f"num of chapters {len(chapters)}")
    ttext = thtml2ttext(chapters)
    return ttext

from epub_conversion.utils import open_book

def epub_2_txt_file(input):
    # Check if input_arg is a file object
    if isinstance(input, (str, os.PathLike)):
        # input_arg is a file path
        epub_path = input
    else:
        # Assume input_arg is a file object
        epub_path = save_to_file(input)
    # Open the ePub book
    ebook = epub.read_epub(epub_path)
    book_title = ebook.title

    # Convert the ePub book to lines of text
    lines = epub2text(epub_path)

    # Write the lines of text to a file
    output_file_path = f"content/{book_title}.txt"
    with open(output_file_path, "w") as f:
        for line in lines:
            f.write(line + '\n')
    
    return output_file_path

