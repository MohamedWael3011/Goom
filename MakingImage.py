from scrapper import GetTraits
import os
from PIL import Image, ImageOps,ImageDraw,ImageFont
StronkX = 2800
StronkY = 1200
class Deformer():
    def __init__(self, x, y):
      self.x = x
      self.y = y
    def getmesh(self,img):
        w,h = img.size
        source_shape = (w-self.x,0, w-self.x,h-self.y, w,h-self.y,w,0)
        target_rectange = (0,0,w,h)
        return [(target_rectange,source_shape)]

SkippableTraitsFolders = ["0background","7left hand","8right hand"]
Crops = {
  "guball":(600, 600, 2850, 2850)
}
#Background Back Flavor Clothes Eye Mouth Head  RHand LHand
# Setting the Path for Layers
def GenerateImage(GoombleID,Traits,meme):  #Will need to add a new argument for choices when provided
    RenderingTraits = []
    BodyPath = "{}".format(Traits["body"])
    if meme =='normal':
      for att in sorted(os.listdir(BodyPath)):
        if att != "0background":
          if Traits["clothes"] == "sour mummy onesie" and "mouth" in att:
              continue
          layer = os.path.join(BodyPath,att)
          AttributeName = att[1:]  #Removing the sort number
          if Traits[AttributeName] != 'none':
              AttributePath = os.path.join(layer,Traits[AttributeName]+".png")
              RenderingTraits.append(AttributePath)    
                  
    else:   
      for att in sorted(os.listdir(BodyPath)):  # Getting the attributes in right order
        if not (att in SkippableTraitsFolders) :
            if Traits["clothes"] == "sour mummy onesie" and "mouth" in att:
                continue
            layer = os.path.join(BodyPath,att)
            AttributeName = att[1:]  #Removing the sort number
            if Traits[AttributeName] != 'none':
                AttributePath = os.path.join(layer,Traits[AttributeName]+".png")
                RenderingTraits.append(AttributePath)

    TransparentImage = Image.new("RGBA", (4096,4096))

    for layer in RenderingTraits:  #Without Background
      LayerImage = Image.open(layer)
      if meme =="hand" and Traits["flavor"] in layer:
        if Traits["body"] =="round":
          img_mask = Image.open('maskR.png')
          img_mask = img_mask.convert('L')
          LayerImage.putalpha(img_mask)
        else:
          img_mask = Image.open('maskT.png')
          img_mask = img_mask.convert('L')    
          LayerImage.putalpha(img_mask)
      TransparentImage = Image.alpha_composite(TransparentImage,LayerImage)
    TransparentImage.save( GoombleID  +".png")
    return GoombleID,Traits

def GenerateMeme(GoombleID,Traits,meme):
    #Meme path
  MemePath=""
  if meme =="gunball": # Handling Soda flavor in tall and round as they have different colors
    if (Traits["body"] == "tall" and Traits["flavor"] == 'soda'):
      Traits["flavor"] = "sodaT"
    MemePath= "{}/{}.png".format(meme,Traits["flavor"])
  else:
      MemePath = "{}.png".format(meme)
  MemeTrait = Image.open(r"{}".format(MemePath))
  Goomble = Image.open(r"{}.png".format(GoombleID))
  if meme =="gunball" or meme =="hand":
    Goomble = Goomble.crop((600, 600, 2850, 2850))
 
  Goomble =Goomble.resize((2048,2048),resample=Image.NEAREST)

    

  if meme == "stonks":
    Goomble = Image.alpha_composite(MemeTrait,Goomble)
  else:
    Goomble = Image.alpha_composite(Goomble,MemeTrait)
  Goomble.save(GoombleID+".png")


    
def MoveGoomble(GoombleID):
  im = Image.open(r"{}.png".format(GoombleID))
  deform = ImageOps.deform(im,Deformer(StronkX,StronkY))
  deform.save(GoombleID + ".png")
  


def GenerateWallpaper(GoombleID,color):
    Goomble = Image.open(r"{}.png".format(GoombleID))
    Goomble = Goomble.resize((537, 537), resample=Image.NEAREST)
    alpha_mask = Goomble.convert('RGBA').split()[-1]
    Wallpaper = Image.new('RGBA', (1080, 1920), color)
    Font = ImageFont.truetype('BubbleboddyNeue-ExtraBold Trial.ttf', 70)
    Draw = ImageDraw.Draw(Wallpaper)
    Draw.text((217, 1097), "Today is a good day.", (0, 0, 0), font=Font)
    Wallpaper.paste(Goomble, (272, 598), mask=alpha_mask)
    Wallpaper.save(f"{GoombleID}Wallpaper.png")
    
def GenerateWallpaperLegendary(Legendary,color):
    Goomble = Image.open(r"legendary/{}.png".format(Legendary))
    Goomble = Goomble.resize((537, 537), resample=Image.NEAREST)
    alpha_mask = Goomble.convert('RGBA').split()[-1]
    Wallpaper = Image.new('RGBA', (1080, 1920), color)
    Font = ImageFont.truetype('BubbleboddyNeue-ExtraBold Trial.ttf', 70)
    Draw = ImageDraw.Draw(Wallpaper)
    Draw.text((217, 1097), "Today is a good day.", (0, 0, 0), font=Font)
    Wallpaper.paste(Goomble, (272, 598), mask=alpha_mask)
    Wallpaper.save(f"{Legendary}Wallpaper.png")
    
