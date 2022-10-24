from PIL import Image, ImageOps, ImageChops
from tqdm import tqdm
from colorama import Fore
#User may change these================================================================
aligned = False
denoise = True
gain = 2.0

ChannelA = Image.open("Vegetation_1.png")
ChannelB = Image.open("Vegetation_2.png")
ChannelC = Image.open("Vegetation_3.png")
ChannelD = Image.open("Vegetation_4.png")
ChannelE = Image.open("Vegetation_5.png")
ChannelF = Image.open("Vegetation_6.png")

#Align V1, V2 and V3 and save the aligned images =====================================
if(aligned == False):
    print(Fore.YELLOW + "[Info] Trying to overlay images...")
    print(Fore.GREEN + "Saving Channel 1...")
    ChannelA.save("V1_resized.png")

    ChannelB_width = ChannelB.width + 12
    ChannelB = ChannelB.resize((ChannelB_width, ChannelB.height))
    ChannelB = ImageChops.offset(ChannelB, -6, 104)
    print(Fore.GREEN + "Saving Channel 2...")
    ChannelB.save("V2_resized.png")

    ChannelC = ImageOps.mirror(ChannelC)
    ChannelC_width = ChannelC.width + 16
    ChannelC = ChannelC.resize((ChannelC_width, ChannelC.height))
    ChannelC = ImageChops.offset(ChannelC, -8, 155)
    print(Fore.GREEN + "Saving Channel 3...")
    ChannelC.save("V3_resized.png")
else:
    print(Fore.YELLOW + "[Info] Images are already aligned! Skipping...")

Green = Image.new('RGB', (ChannelA.width, ChannelA.height))
RGB = Image.new('RGB', (ChannelA.width, ChannelA.height))
Water = Image.new('RGB', (ChannelA.width, ChannelA.height))
Desert_red = Image.new('RGB', (ChannelA.width, ChannelA.height))
Desert_blue = Image.new('RGB', (ChannelA.width, ChannelA.height))
Swath = Image.new('I', (2929, ChannelD.height + 55))
#Create and save full swath image ===============================================================
print(Fore.YELLOW + "Aligning Channel 4, 5 and 6 to a full-swath image...")
for x in tqdm(range(ChannelD.width)):
    for y in range(ChannelD.height):
        try:
            Swath.putpixel((x, y + 50), int(ChannelF.getpixel((x, y)) * gain))
            Swath.putpixel((x + 969, y), int(ChannelE.getpixel((x, y)) * gain))
            Swath.putpixel((x + 1906, y + 50), int(ChannelD.getpixel((x, y)) * gain))
        except:
            Swath.putpixel((x, y), 0)
Swath.save("456_swath.png")
#Denoise created 456 Swath======================================================================
if(denoise == True):
    print(Fore.YELLOW + "Denoising 456 swath image...")
    averages = [0 for a in range(Swath.width)]
    for x in range(Swath.width):
        height = 0
        for y in range(Swath.height):
            if(Swath.getpixel((x, y)) != 0):
                averages[x] = averages[x] + Swath.getpixel((x, y))
                height += 1
        averages[x] = int(averages[x] / height)
    lowest = 65535
    highest = 0
    for a in range(Swath.height):
        for b in range(Swath.width):
            value = Swath.getpixel((b, a))
            corrected = value - averages[b]
            Swath.putpixel((b, a), corrected * 10)
            if(corrected < lowest):
                lowest = corrected
            if(corrected > highest):
                highest = corrected
    for i in range(Swath.width):
        for j in range(Swath.height):
            value = Swath.getpixel((i, j))
            normalized = int(65535*((value - lowest) / (highest - lowest)))
            Swath.putpixel((i, j), normalized)
    Swath.save("456_swath_denoised.png")
#Create and save composites ====================================================================
print(Fore.YELLOW + "Creating composites...")
for x in tqdm(range(ChannelA.width)):
    for y in range(ChannelA.height):
        try:
            A_value = ChannelA.getpixel((x,y)) / 65536 * 256 #Convert 16Bit Greyscale to 8 Bit RGB
            B_value = ChannelB.getpixel((x,y)) / 65536 * 256
            C_value = ChannelC.getpixel((x,y)) / 65536 * 256
        except:
            A_value = B_value = C_value = 0
#General Green=========================================================
        R = int(B_value * 6.57 - 0.9 * C_value)
        G = int(C_value * 7.11 - 0.9 * B_value)
        B = int(A_value * 9.27 + 0.9 * B_value)
        Green.putpixel((x, y), (R, G, B))
#Real color============================================================
        R = int(-20.58 * A_value + 3.21 * B_value + 11.39 * C_value)
        G = int(-11.16 * A_value - 2.78 * B_value + 11.78 * C_value)
        B = int(-19.75 * A_value - 3.73 * B_value + 17.33 * C_value)
        RGB.putpixel((x, y), (R, G, B))
#Water=================================================================
        B = int(-18 * A_value + 29.28 * B_value - 13.32 * C_value)
        G = int(2.18 * A_value + 0.91 * B_value + 2.72 * C_value)
        R = int(1.59 * A_value + 6.13 * B_value - 2.78 * C_value)
        Water.putpixel((x,y), (R, G, B))
#Desert_red=================================================================
        R = int(-3.7 * A_value - 0.86 * B_value + 8.7 * C_value)
        G = int(-0.68 * A_value + 3.36 * B_value + 3.37 * C_value)
        B = int(-2.19 * A_value + 16.92 * B_value - 9.45 * C_value)
        Desert_red.putpixel((x,y), (R, G, B))
        Desert_blue.putpixel((x,y), (B, G, R))

print(Fore.GREEN + "Done! Saving images!")
Green.save("Green.jpg")
RGB.save("Cold.jpg")
Water.save("Water.jpg")
Desert_red.save("Desert_red.jpg")
Desert_blue.save("Desert_blue.jpg")
