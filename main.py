import json
import os
import codecs
import sys
from PIL import Image, ImageFont, ImageDraw
import PyPDF2
import fitz    

WIDTH = 595
HEIGHT = 842

# Base name
name = "deck_phi.json"
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

  # Creation du pdf
  create_pdf = 'pdf' in data
  if create_pdf:
    # counter of card
    num = 0

    #Max card / page
    num_page = data['pdf']['nb_h'] * data['pdf']['nb_v']

    #Create pdf file
    output_pdf = PyPDF2.PdfFileWriter()

    #get size of the image
    (x_img, y_img) = Image.open(data['imgCarte']).size

    #Compute coef to print the card
    coef_x = WIDTH /(x_img*data['pdf']['nb_h'] + (data['pdf']['nb_h']-1)*data['pdf']['hmargin'])
    coef_y = HEIGHT /(y_img*data['pdf']['nb_v']+ (data['pdf']['nb_v']-1)*data['pdf']['vmargin'])

    # Number of (x,y) card already drawn
    nb_x = 0
    nb_y = 0

    # Save the pdf and open it
    with open('decks/' + data['name'] + 'V' + str(data['version']) + '/' + 'deck.pdf', "wb") as out_file:
      output_pdf.write(out_file)
    doc = fitz.open('decks/' + data['name'] + 'V' + str(data['version']) + '/' + 'deck.pdf')

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

    if create_pdf:
      #If the last page was complete
      if num == 0:
        # Draw a new page
        page = doc.newPage(pno=-1,width=WIDTH,height=HEIGHT)

      # We draw the image
      page.insertImage(fitz.Rect(coef_x*(nb_x)*(x_img + data['pdf']['hmargin']), coef_y*(nb_y)*(y_img + data['pdf']['vmargin']), coef_x*((nb_x + 1)*(x_img)+nb_x * data['pdf']['hmargin']), coef_y*((nb_y + 1)*(y_img)+nb_y * data['pdf']['vmargin'])), filename = 'decks/' + data['name'] + 'V' + str(data['version']) + '/' + card['nom'] + '.png')
      
      # We increment the number of card drawn
      nb_x += 1
      if nb_x >= data['pdf']['nb_h']:
        nb_x = 0
        nb_y += 1

      num += 1
      if num >= num_page:
        num = 0
        nb_x = 0
        nb_y = 0

  # we create the pdf
  if create_pdf:
    doc.saveIncr()

  data['version'] = int(data['version']) + 1

  with codecs.open(name,'w') as outfile:
    json.dump(data, outfile,ensure_ascii=False)

# Gestion d'erreurs
except IOError:
    print('Le fichier \"' + name + '\" n\'a pas pu être ouvert')
