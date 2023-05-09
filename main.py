import discord
from discord import app_commands
from discord.ext import commands
from MakingImage import *
import os, asyncio
import traceback
from dotenv import load_dotenv
from discord.app_commands import Choice

intents = discord.Intents.all()
import json

client = commands.Bot(command_prefix='.', intents=intents)
load_dotenv()
MemeList = ["hand", "gunball", "stonks","copium"]
Legendaries = ["rarest goombles of all time", "kespin cone", "powdered peaks", "magic sugar forest", "cavity court", "caramel swamp"]
def AllMeme():
  s=""
  for i in MemeList:
    s+= "`"+i+"`"+" "
  return s  
    
@client.event
async def on_ready():

  print('GoomMeme is running! Currently serving Goomble Holders')
  await client.change_presence(activity=discord.Game(name="Goombles"))
  await client.tree.sync()


async def owner(interaction: discord.Interaction):  # Me or Nash
  if interaction.user.id == 368776198068895745 or interaction.user.id == 175685873520738304:
    return True


async def holder(interaction: discord.Interaction):
  role = interaction.guild.get_role(999378751018246221)
  if role in interaction.user.roles or interaction.user.id == 368776198068895745:
    return True
  await interaction.response.send_message(
    "<@{}> I am sorry only Goomble Holders can use me.".format(
      interaction.user.id),
    ephemeral=True)
  return False


@client.tree.command(name="wallpaper", description="Generates a wallpaper with your Goomble!")
@app_commands.choices(
  color=[ # param name
    Choice(name="Indian Red", value="#E05C5C"),
    Choice(name="Yellow Green", value="#BEE18D"),
    Choice(name="Lemon Yellow", value="#FEF9A8"),
    Choice(name="Melon", value="#FFA49F"),
    Choice(name="Baby Blue Eyes", value="#9CC4FE"),
    Choice(name="Maxiumum Blue", value="#B3A1FB"),
    Choice(name="Raiah", value="#FFB461"),
  ]
)
@commands.check(holder)
@app_commands.checks.cooldown(1, 20.0, key=lambda i: (i.user.id))
async def wallpaper(interaction: discord.Interaction, *, url: str, color: Choice[str]):
    if not ("pool.pm/" in url):
      await interaction.response.send_message(
        "<@{}> Please enter a valid url.".format(interaction.user.id),
        ephemeral=True)
      return
    try:
      await interaction.response.defer(ephemeral=True)
      
      Traits,GID = await client.loop.run_in_executor(None,GetTraits,url)
      if Traits["flavor"] in Legendaries:
        name = Traits["flavor"]
        await client.loop.run_in_executor(None, GenerateWallpaperLegendary, Traits["flavor"],color.value)
        await asyncio.sleep(2)
        await interaction.user.send("Wallpaper",file=discord.File(f"{name}Wallpaper.png"))
        if os.path.exists(f"{name}Wallpaper.png"):
          os.remove(f"{name}Wallpaper.png")
        
        
      else:
        await client.loop.run_in_executor(None, GenerateImage, GID,Traits,'normal')
        await client.loop.run_in_executor(None, GenerateWallpaper, GID,color.value)
        await asyncio.sleep(2)
        await interaction.user.send("Wallpaper",file=discord.File(f"{GID}Wallpaper.png"))
        if os.path.exists(f"{GID}Wallpaper.png"):
          os.remove(f"{GID}Wallpaper.png")
        if os.path.exists(GID + ".png"):
          os.remove(GID+".png")
      await interaction.followup.send("<@{}> I have some sweets in your DMs.:candy:".format(interaction.user.id))        
      
    except IndexError:
      await interaction.followup.send("Pool.pm didn't load properly, please try again.",ephemeral=True)
    except ValueError:
      await interaction.followup.send("Please enter a valid color.",ephemeral=True)
      
    except Exception as e:
          await interaction.followup.send("Something went wrong, please report to Moka#9205. But first make sure that you are using the command properly which is `/wallpaper <your Goomble pool.pm link> <color or #HexaValue>`.",ephemeral=True)
          MOKA = await client.fetch_user("368776198068895745")
          await MOKA.send("".join(traceback.format_exception_only(e)).strip())
      
      
    
  
  

@client.tree.command(name="rename", description="Changing bot username")
@app_commands.check(owner)
async def rename(interaction: discord.Interaction, name: str):
  await interaction.client.user.edit(username=name)
  await interaction.response.send_message(
    "Bot username has been changed to %s" % name)


@client.tree.command(name="goomeme",
                     description="Turning your Goomble to a meme.")
@commands.check(holder)
@app_commands.checks.cooldown(1, 20.0, key=lambda i: (i.user.id))
async def goomeme(interaction: discord.Interaction, *, url: str, meme: str):
  meme = meme.lower()
  if not ("pool.pm/" in url):
    await interaction.response.send_message(
      "<@{}> Please enter a valid url.".format(interaction.user.id),
      ephemeral=True)
    return
  try:
    await interaction.response.defer(ephemeral=True)
    Traits,GID = await client.loop.run_in_executor(None,GetTraits,url)
    if meme == "all":
      for meme in MemeList:
          if Traits["flavor"] in Legendaries:
            await interaction.user.send("{} Meme".format(meme),file=discord.File("legendary/{} {}.png".format(meme,Traits["flavor"])))
          else:
              await client.loop.run_in_executor(None, GenerateImage, GID,Traits,meme)
              if meme == "stonks":
                await client.loop.run_in_executor(None, MoveGoomble, GID)
              await client.loop.run_in_executor(None, GenerateMeme, GID, Traits, meme)
              await asyncio.sleep(2)
              if not os.path.exists("{}.png".format(GID)):
                await interaction.followup.send("<@{}> Someone else just generated on same Goomble, please try again later.".format(interaction.user.id))
              else:
                await interaction.user.send("{} Meme".format(meme),file=discord.File("{}.png".format(GID)))
                if os.path.exists(meme+GID+".png"):
                  os.remove(meme + GID + ".png")
                if os.path.exists(GID + ".png"):
                  os.remove(GID+".png")
      await interaction.followup.send(
        "<@{}> I have some sweets in your DMs.:candy:".format(
          interaction.user.id))        
    else:
        if Traits["flavor"] in Legendaries:
           await interaction.user.send("{} Meme".format(meme),file=discord.File("legendary/{} {}.png".format(meme,Traits["flavor"])))  
        else:
          await client.loop.run_in_executor(None, GenerateImage, GID,Traits,meme)   
          if meme == "stonks":
            await client.loop.run_in_executor(None, MoveGoomble, GID)
            
          await client.loop.run_in_executor(None, GenerateMeme, GID, Traits, meme)
          await asyncio.sleep(2)
          if not os.path.exists("{}.png".format(GID)):
            await interaction.followup.send(
              "<@{}> Someone else just generated on same Goomble, please try again later."
              .format(interaction.user.id))
          else:
            await interaction.user.send("{} Meme".format(meme),
                                        file=discord.File("{}.png".format(GID)))
            if os.path.exists(meme+GID+".png"):
              os.remove(meme + GID + ".png")
            if os.path.exists(GID + ".png"):
              os.remove(GID+".png")
        await interaction.followup.send(
          "<@{}> I have sent something sweet in your DMs.:candy:".format(
            interaction.user.id))

    #Update the Database
    file = open('GoombleMemesGenerated.json', 'r')
    GoomblesDic = json.loads(file.read())
    if GID not in GoomblesDic.keys():
      GoomblesDic[GID] = 0
    GoomblesDic[GID] += 1
    file = open('GoombleMemesGenerated.json', 'w')
    file.write(json.dumps(GoomblesDic))
  except IndexError:
    await interaction.followup.send("Pool.pm didn't load properly, please try again.")
  except Exception as e:
    await interaction.followup.send(
      "Something went wrong, please report to Moka#9205. But first make sure that you are using the command properly which is `/goomeme <your Goomble pool.pm link> <meme name>` Available memes are: {} and `all` will get you all available memes at once.".format(AllMeme()),
      ephemeral=True)
    MOKA = await client.fetch_user("368776198068895745")
    await MOKA.send("".join(traceback.format_exception_only(e)).strip())


@goomeme.error
async def on_test_error(interaction: discord.Interaction,error: app_commands.AppCommandError):
  if isinstance(error, app_commands.CommandOnCooldown):
    await interaction.response.send_message("Please wait for {}".format(
      error.retry_after),ephemeral=True)



  


client.run(os.getenv('TOKEN'))

