from PIL import Image
from glob import glob

images = glob("./images/*")
mockups = glob("./mockups/*")
mockupList = []
for m in mockups:
    mockupList.append(m.split('/')[-1].split('.')[0])
m1={"x1":820, "y1":560, "x2":1300, "y2":1200, "angle":0}
m2={"x1":680, "y1":450, "x2":1160, "y2":1210, "angle":-3}
m4={"x1":740, "y1":500, "x2":1350, "y2":1210, "angle":0}
m5={"x1":700, "y1":560, "x2":1210, "y2":1220, "angle":0}
m7={"x1":840, "y1":540, "x2":1360, "y2":1210, "angle":0}
positions = {"mockup1":m1,"mockup2":m2,"mockup4":m4,"mockup5":m5,"mockup7":m7}
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
        img1.convert(img1.mode).save("./output/" + outputName)
