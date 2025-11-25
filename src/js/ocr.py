import pytesseract
from PIL import Image
import sys

if len(sys.argv) < 2:
    print('Usage: python ocr.py <image_path>')
    sys.exit(1)

image_path = sys.argv[1]
text = pytesseract.image_to_string(Image.open(image_path), lang='por')
print(text)