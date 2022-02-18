import ddddocr
from PIL import Image

from tool.tool import ddddocr_ocr


def inquire_auth_code(img_location):
    det = ddddocr.DdddOcr(det=True)

    # 读取验证码并返回坐标
    with open(img_location, 'rb') as f:
        image = f.read()
    poses = det.detection(image)

    print(poses[0][0])

    code = []
    count = 0
    for coord in poses:
        count += 1
        coord = (coord[0], coord[1], coord[2], coord[3])
        i = Image.open(img_location)
        frame4 = i.crop(coord)
        # 扣除文字图片并重命名保存
        name = '../temporary/patent_Login_code-' + str(count) + '.png'
        frame4.save(name)
        # 识别单个图片
        ocr = ddddocr_ocr(name)
        a = dict(code=ocr, X=coord[0], Y=coord[1])
        code.append(a)

    return code


if __name__ == '__main__':
    code = inquire_auth_code('./code.png')
