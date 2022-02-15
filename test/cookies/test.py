import requests
import muggle_ocr


def getCode():
    # 验证码地址
    url = 'http://cpquery.cnipa.gov.cn/freeze.main?txn-code=createImgServlet'
    response = requests.get(url)
    # 将图片保存
    with open("code.png", "wb") as f:
        f.write(response.content)

    # 初始化；model_type 包含了 ModelType.OCR/ModelType.Captcha 两种
    sdk = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.OCR)
    # ModelType.OCR 可识别光学印刷文本 这里个人觉得应该是官方文档写错了 官方文档是ModelType.Captcha 可识别光学印刷文本
    with open(r"code.png", "rb") as f:
        b = f.read()
    res = sdk.predict(image_bytes=b)

    # 对ocr识别后的字符串进行处理
    number = list(res.rstrip('=' or '三' or '二' or '"' or '.'))
    code = 0
    if number[1] == '-' or number[1] == '一':
        if number[0] == '了':
            number[0] = 7
        if number[0] == 'G':
            number[0] = 6
        code = int(number[0]) - int(number[2])

    elif number[1] == '+' or number[1] == '十':
        if number[0] == '了':
            number[0] = 7
        if number[0] == 'G':
            number[0] = 6
        code = int(number[0]) + int(number[2])

    return code


if __name__ == '__main__':
    sdk = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.OCR)
    with open(r"code.png", "rb") as f:
        b = f.read()
    res = sdk.predict(image_bytes=b)
    print(res)
    # getCode()
