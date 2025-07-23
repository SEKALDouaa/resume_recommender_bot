from PIL import Image
import numpy as np
import layoutparser as lp
import pytesseract as pt


image = Image.open(r"../resume_recommender_bot/data/raw_cvs/Image_88.jpg")
image_np =np.array(image)
model1 = lp.Detectron2LayoutModel(config_path=r"C:\Dev\resume_recommender_bot\models\publaynet_x101\config.yaml" ,
                                  model_path=r"C:\Dev\resume_recommender_bot\models\publaynet_x101\model_final.pth",
                                 extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.8],
                                 label_map={0: "Text", 1: "Title", 2: "List", 3:"Table", 4:"Figure"})

model3 = lp.Detectron2LayoutModel(config_path=r"C:\Dev\resume_recommender_bot\models\primalayout_r50\config.yaml" ,
                                  model_path=r"C:\Dev\resume_recommender_bot\models\primalayout_r50\model_final.pth",
                                 extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.8],
                                 label_map={1:"TextRegion", 2:"ImageRegion", 3:"TableRegion", 4:"MathsRegion", 5:"SeparatorRegion", 6:"OtherRegion"})

model2 = lp.Detectron2LayoutModel(config_path=r"C:\Dev\resume_recommender_bot\models\publaynet_r50\config.yml" ,
                                  model_path=r"C:\Dev\resume_recommender_bot\models\publaynet_r50\model_final.pth",
                                 extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.8],
                                 label_map={0: "Text", 1: "Title", 2: "List", 3:"Table", 4:"Figure"})



layout1 = model1.detect(image)
layout2 = model2.detect(image)
layout3 = model3.detect(image)

all_blocks = layout1 + layout2 + layout3


image_combined = lp.draw_box(image.copy(), all_blocks, box_width=5, box_alpha=0.2, show_element_type=True)
#image_combined.show()

# image1 = lp.draw_box(image.copy(), layout1, box_width=5, box_alpha=0.2, show_element_type=True)
# image2 = lp.draw_box(image.copy(), layout2, box_width=5, box_alpha=0.2, show_element_type=True)
# image3 = lp.draw_box(image.copy(), layout4, box_width=5, box_alpha=0.2, show_element_type=True)

# image1.show()
# image2.show()
# image3.show()

pt.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe" 
ocr_agent = lp.TesseractAgent(languages="eng")

ocr_results = []

for block in all_blocks:
    segment_image = block.crop_image(image_np)
    text = ocr_agent.detect(segment_image)
    ocr_results.append((block, text))

for block, text in ocr_results:
    print(f"[{block.type}] {text}")