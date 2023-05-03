from PIL import Image, ImageDraw, ImageFont
import sys, os

#                         font_size,file, w_pxl,h_pxl)
fnts = {("Lucida Console",16):("lucon.ttf",10,16)}

font = ("Lucida Console",16)
ffile,w_pxl,h_pxl = fnts[font]

# dir = "./texts"
# fileList = os.listdir(dir)

def toImg(count, maxlen, lines, fname,fileExt):
  #print(maxlen*w_pxl, count*(h_pxl+1))
  img = Image.new('RGB', ((maxlen-1)*w_pxl, count*(h_pxl+1)), color = (50, 50, 50))
  d = ImageDraw.Draw(img)
# d.font = ImageFont.truetype("fonts/FreeMono.ttf",16)
  d.font = ImageFont.truetype("fonts/"+ffile,16)
  i = 0
  for line in lines:
    d.text((0,i*(h_pxl+1)), line, fill=(240,240,240))
    i += 1
  # d.text((0,17), "Prelude >", fill=(240,240,240))
  img.save(fname + fileExt)

def readtxt(fname):
  f = open(fname, 'r', encoding='utf8')
  lines = f.readlines()
  f.close()
  count = len(lines)
  maxlen = 0
  for line in lines:
    length = len(line)
    if length > maxlen: 
      maxlen = length
  return count, maxlen, lines
  
def main():
  if len(sys.argv)<3: 
   print('python thisProg.py path (jpeg|png) [del]') 
   return
  dir = sys.argv[1]
  fileList = os.listdir(dir)
  fileExt = '.'+sys.argv[2]
  for file in fileList:
    fname = dir+'/'+file #+fileExt
    print('---'+fname)
    if os.path.exists(fname) and fname.endswith(fileExt):
      os.remove(fname)
    #else: print(f"The file {fname} does not exist")
  # if len(sys.argv) > 2 and sys.argv[2]== 'delImg':
   # fileExt = sys.argv[3]
   # for file in fileList:
     # fname = dir+'/'+file+fileExt
     # if os.path.exists(fname) and fileName.endswith('.png')::
       # os.remove(fname)
     # else: print(f"The file {fname} does not exist")
   # return
  # fileList = os.listdir(dir)
  fileList = os.listdir(dir)
  #print(fileList)
  for file in fileList:
    fname = dir+'/'+file
  # fname = 'texts/'+sys.argv[1]
    count, maxlen, lines = readtxt(fname)
  # print(count, maxlen, lines)
    toImg(count, maxlen, lines,fname,fileExt)
  print(fileList)
  print(len(sys.argv))
  print(sys.argv[3])  
  if len(sys.argv)>3 and sys.argv[3]=='del': 
    for file in fileList:
      fname = dir+'/'+file
      print(">>---"+file)
      if os.path.exists(fname): # and file.endswith('hs'):
        os.remove(fname)
if __name__=="__main__":
    main()
    
# python txt2im.01.py texts png del