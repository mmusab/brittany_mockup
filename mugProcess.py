from PIL import Image
from glob import glob

images = glob("./mugImages/*")
mockups = glob("./mugMockups/*")
mockupList = []
for m in mockups:
    mockupList.append(m.split('/')[-1].split('.')[0])
m1={"x1":640, "y1":490, "x2":1500, "y2":1340, "angle":0}
m2={"x1":680, "y1":730, "x2":1460, "y2":1510, "angle":0}
positions = {"mugmockup1":m1,"mugmockup2":m2}
totalMockups = len(positions)
for index,m in enumerate(mockupList):
    for im in images:
        img1 = Image.open(mockups[index])
        img = Image.open(im)

        # The values used to crop the original image (will form a bbox)
        # x1, y1, x2, y2 = 740, 500, 1350, 1210

        # The angle at which the cropped Image must be rotated
        angle = 0

        # cropping the original image
        # img = img1.crop((x1, y1, x2, y2))
        # img = img2
        # Firstly converting the Image mode to RGBA, and then rotating it
        img = img.convert("RGBA").rotate(positions[m]['angle'], resample=Image.BICUBIC)

        # calibrating the bbox for the beginning and end position of the cropped image in the original image
        # i.e the cropped image should lie in the center of the original image
        x1 = positions[m]['x1']
        y1 = positions[m]['y1']
        x2 = positions[m]['x2']
        y2 = positions[m]['y2']

        # pasting the cropped image over the original image, guided by the transparency mask of cropped image
        img = img.resize((x2-x1,y2-y1))
        img1.paste(img, box=(x1, y1, x2, y2), mask=img)

        # converting the final image into its original color mode, and then saving it
        outputName = im.split('/')[-1].split('.')[0] + '-' + m + '.png'
        img1.convert(img1.mode).save("./mugOutput/" + outputName)
