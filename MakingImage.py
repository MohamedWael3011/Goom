from scrapper import GetTraits
import os
from PIL import Image, ImageOps

# Constants
STRONK_X = 2800
STRONK_Y = 1200
SKIPPABLE_TRAITS_FOLDERS = ["0background", "7lefthand", "8righthand"]
CROPS = {"guball": (600, 600, 2850, 2850)}

class Deformer:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_mesh(self, img):
        w, h = img.size
        source_shape = (w-self.x, 0, w-self.x, h-self.y, w, h-self.y, w, 0)
        target_rectangle = (0, 0, w, h)
        return [(target_rectangle, source_shape)]

def generate_image(url, meme):
    traits, goomble_id = GetTraits(url)
    rendering_traits = []
    body_path = "{}".format(traits["body"])
    for att in sorted(os.listdir(body_path)):
        if att not in SKIPPABLE_TRAITS_FOLDERS:
            if traits["clothes"] == "sour mummy onesie" and "mouth" in att:
              continue
            layer = os.path.join(body_path, att)
            attribute_name = att[1:]  # Removing the sort number
            if traits[attribute_name] != 'none':
                attribute_path = os.path.join(layer, traits[attribute_name] + ".png")
                rendering_traits.append(attribute_path)

    transparent_image = Image.new("RGBA", (4096, 4096))

    for layer in rendering_traits:  # Without Background
        layer_image = Image.open(layer)
        if meme == "hand" and traits["flavor"] in layer:
            if traits["body"] == "round":
                img_mask = Image.open('maskR.png').convert('L')
            else:
                img_mask = Image.open('maskT.png').convert('L')
            layer_image.putalpha(img_mask)
        transparent_image = Image.alpha_composite(transparent_image, layer_image)

    transparent_image.save(goomble_id + ".png")
    return goomble_id, traits

def generate_meme(goomble_id, traits, meme):
    # Meme path
    if meme == "gunball":
        # Handling Soda flavor in tall and round as they have different colors
        if traits["body"] == "tall" and traits["flavor"] == 'soda':
            traits["flavor"] = "sodaT"
        meme_path = "{}/{}.png".format(meme, traits["flavor"])
    else:
        meme_path = "{}.png".format(meme)

    meme_trait = Image.open(meme_path)
    goomble = Image.open("{}.png".format(goomble_id))
    if meme == "gunball" or meme == "hand":
        goomble = goomble.crop(CROPS[meme])
    goomble = goomble.resize((2048, 2048), resample=Image.NEAREST)

    if meme == "stonks":
        goomble = Image.alpha_composite(meme_trait, goomble)
    else:
        goomble = Image.alpha_composite(goomble, meme_trait)

    goomble.save(meme + goomble_id + ".png")

def move_goomble(goomble_id):
    im = Image.open("{}.png".format(goomble_id))
    deform = ImageOps.deform(im, Deformer(STRONK_X, STRONK_Y))
    deform.save(goomble_id + ".png")