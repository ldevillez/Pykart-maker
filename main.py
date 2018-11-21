import json
import os
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw


with open('deck.json') as json_file:
    data = json.load(json_file)

os.mkdir(data['name'] + 'V' + str(data['version']))

for card in data["cartes"]:
    img = Image.open(data['imgCarte'])
    draw = ImageDraw.Draw(img)
    for zones in data['zone']:
        if(card[zones["id"]] != None):
            if zones["type"] == "text":
                font = ImageFont.truetype(zones["font"], zones["size"])
                draw.text((zones["xtop"], zones["ytop"]+ 1* zones["size"]),card[zones["id"]],(zones["R"],zones["G"],zones["B"]),font=font)

            elif zones["type"] == "img":
                im= Image.open(card[zones["id"]])
                region = im.crop((0,0,zones["ybot"] - zones["ytop"],zones["xbot"] - zones["xtop"]))
                img.paste(region,(zones["ytop"],zones["xtop"],zones["ybot"],zones["xbot"]))


    img.save(data['name'] + 'V' + str(data['version']) + '/' + card['nom'] + '.png')





data['version'] = int(data['version']) + 1
with open('deck.json', 'w') as outfile:
    json.dump(data, outfile)
