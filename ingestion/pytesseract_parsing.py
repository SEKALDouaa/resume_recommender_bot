import pytesseract
from PIL import Image

print("Converting PDF to images...")
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
image = Image.open(r"C:\Dev\resume_recommender_bot\data\raw_cvs\e9b8968eaf92c36e.png")

full_text = ""
text = pytesseract.image_to_string(image)
full_text += f"{text}"

print("Text extraction complete.")
print(full_text)