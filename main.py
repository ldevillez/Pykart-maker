import json
import os
import codecs
import sys
from PIL import Image, ImageFont, ImageDraw

# Base name
name = 'deck.json'
# if a name is given
if len(sys.argv) >= 2:
  name = sys.argv[1]

try:
  # On ouvre le fichier
  with codecs.open(name,'r','utf-8') as json_file:
    # On load le json
    data = json.load(json_file)

  # On crée le dossier pour le deck
  os.mkdir('decks/' + data['name'] + 'V' + str(data['version']))

  # On parcourt les cartes
  for card in data["cartes"]:
    #On ouvre le template
    img = Image.open(data['imgCarte'])
    #On le dessine
    draw = ImageDraw.Draw(img)
    #Pour chaque zone on va la dessiner sur la carte si elle existe
    for zones in data['zone']:
      if(card[zones["id"]] != None):

        # Zone de type texte
        if zones["type"] == "text":
          font = ImageFont.truetype(zones["font"], zones["size"])
          draw.text((zones["xtop"], zones["ytop"]+ 1* zones["size"]),card[zones["id"]],(zones["R"],zones["G"],zones["B"]),font=font)

        # Zone de type image
        elif zones["type"] == "img":
          im= Image.open(card[zones["id"]])
          region = im.crop((0,0,zones["ybot"] - zones["ytop"],zones["xbot"] - zones["xtop"]))
          img.paste(region,(zones["ytop"],zones["xtop"],zones["ybot"],zones["xbot"]))

    #On sauvegarde la carte
    img.save('decks/' + data['name'] + 'V' + str(data['version']) + '/' + card['nom'] + '.png')

  data['version'] = int(data['version']) + 1

  with codecs.open(name,'w') as outfile:
    json.dump(data, outfile,ensure_ascii=False)

# Gestion d'erreurs
except IOError:
    print('Le fichier \"' + name + '\" n\'a pas pu être ouvert')
