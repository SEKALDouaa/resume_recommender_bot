import pytesseract as pt
from PIL import Image
import layoutparser as lp

pt.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
ocr_agent = lp.TesseractAgent(languages="eng")

def extract_text_from_image(image_path: str) -> str:
    image = Image.open(image_path)
    return ocr_agent.detect(image)
