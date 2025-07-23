import pytesseract as pt 
from PIL import Image
import layoutparser as lp

image_path = r"../resume_recommender_bot/data/raw_cvs/d0d0c5822ac40ffe.png"
image = Image.open(image_path)

pt.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
ocr_agent = lp.TesseractAgent(languages="eng")
ocr_results = []
text = ocr_agent.detect(image)
ocr_results.append(text)
print(f"OCR Results: {ocr_results}")