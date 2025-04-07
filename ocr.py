# import easyocr

# reader = easyocr.Reader(['en'], gpu=True,workers=3,block)  # need to run only once to download the model and load it into memory
# results = reader.readtext('image2.jpg')

# for (bbox, text, prob) in results:
#     print(text)
#     # print(f"Detected text: {text} with probability: {prob}")
import os
from paddleocr import PaddleOCR
import logging

def seedphrase_ocr(image_path):
    logging.getLogger('PaddleOCR').setLevel(logging.CRITICAL)
    if os.path.exists(image_path):
         ocr = PaddleOCR(use_angle_cls=True, lang='en', gpu=True)  # need to run only once to download the model and load it into memory
    else:
        raise FileNotFoundError(f"The file {image_path} does not exist.")     
    result = ocr.ocr(image_path, cls=True)

    word_list = []
    for line in result[0]:
        try:
            if line[1][0][0:2].isnumeric() and line[1][0][2] == '.' and len(line[1][0]) > 3:
                word_list.append(line[1][0].replace(line[1][0][0:3]," ").strip())
            elif line[1][0][0].isnumeric() and line[1][0][1] == '.' and len(line[1][0]) > 3:
                word_list.append(line[1][0].replace(line[1][0][0:2]," ").strip())    
            elif " " in line[1][0]:
                word_list.append(line[1][0].split(' ')[1])
         
            elif line[1][0][0:2].isnumeric() and len(line[1][0]) > 3:
                word_list.append(line[1][0].replace(line[1][0][0:2]," ").strip())
            elif line[1][0][0].isnumeric() and len(line[1][0]) > 3:
                word_list.append(line[1][0].replace(line[1][0][0]," ").strip())
            elif line[1][0].isnumeric() or (line[1][0][0:2].isnumeric() and len(line[1][0]) == 3) or (line[1][0][0].isnumeric() and len(line[1][0]) == 2):
                pass
            else:
                word_list.append(line[1][0])     
        except IndexError:
            pass  
          

    return {i+1:value for i,value in enumerate(word_list)}        
            


if __name__ == "__main__":
    image_path = 'image.jpg'
    seedphrase_dict = seedphrase_ocr(image_path)
    print(seedphrase_dict)


# ocr = PaddleOCR(use_angle_cls=True, lang='en', gpu=True)
# result = ocr.ocr("image4.jpg", cls=True)

# for line in result[0]:
#     if line[1][0][0:2].isnumeric() and line[1][0][2] == '.' and len(line[1][0]) > 3:
#        print(line[1][0].replace(line[1][0][0:3]," ").strip())
#     elif line[1][0][0].isnumeric() and line[1][0][1] == '.' and len(line[1][0]) > 3:
#         print(line[1][0].replace(line[1][0][0:2]," ").strip())
   
     
     

   
