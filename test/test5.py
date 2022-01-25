import muggle_ocr

# 初始化sdk；model_type 包含了 ModelType.OCR/ModelType.Captcha 两种模式,分别对应常规图片与验证码
sdk = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.Captcha)

with open(r"E:\code\code.png", "rb") as f:
    img = f.read()

text = sdk.predict(image_bytes=img)
print(text)
