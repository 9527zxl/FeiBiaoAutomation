import ddddocr

from tool.tool import ddddocr_ocr
from PIL import Image

ocr1 = ddddocr_ocr('../temporary/patent_Login_code-1.png')
ocr2 = ddddocr_ocr('../temporary/patent_Login_code-2.png')
ocr3 = ddddocr_ocr('../temporary/patent_Login_code-3.png')
ocr4 = ddddocr_ocr('../temporary/patent_Login_code-4.png')
# ocr5 = ddddocr_ocr('../temporary/patent_Login_code-5.png')
print(ocr1, ocr2, ocr3, ocr4)
