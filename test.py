MemeList = ["hand", "gunball", "stonks"]

def AllMeme():
  s=""
  for i in MemeList:
    s+= "`"+i+"`"+" "
  return s  

print(AllMeme())