from PIL import Image, ImageOps, ImageChops
from tqdm import tqdm
from colorama import Fore

aligned = False

ChannelA = Image.open("Vegetation_1.png")
ChannelB = Image.open("Vegetation_2.png")
ChannelC = Image.open("Vegetation_3.png")

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
Desert = Image.new('RGB', (ChannelA.width, ChannelA.height))

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
#Desert=================================================================
        R = int(-3.7 * A_value - 0.86 * B_value + 8.7 * C_value)
        G = int(-0.68 * A_value + 3.36 * B_value + 3.37 * C_value)
        B = int(-2.19 * A_value + 16.92 * B_value - 9.45 * C_value)
        Desert.putpixel((x,y), (R, G, B))
print(Fore.GREEN + "Done! Saving images!")
Green.crop((0, 155, ChannelC_width, Green.height - 155)).save("Green.jpg")
RGB.crop((0, 155, ChannelC_width, RGB.height - 155)).save("Cold.jpg")
Water.crop((0, 155, ChannelC_width, Water.height - 155)).save("Water.jpg")
Desert.crop((0, 155, ChannelC_width, Desert.height - 155)).save("Desert.jpg")
