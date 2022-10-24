# PROBA-V Align & False color
This script takes the V1, V2 and V3 channels from PROBA-V's vegetation instrument, overlays them and creates false color images.
It also takes V4, V5 and V6 and combines them to a full-swath image.

# Requirements
For this script to work, you need Python 3 installed and added to PATH. 
After you installed Python on your machine, you need to install Image, Imageops, ImageChops, colorama and tqdm by running
`pip install Pillow tqdm colorama`.

# Feautures
1. Automatically align channels V1/V2/V3
2. Create multiple, different false color composites
3. Automatically align channels V4/V5/V6 to a full swath image
4. Denoise the created full swath image

# Usage
Simply put images named "Vegetation_1.png", "Vegetation_2.png", etc. into the same directory as the script.
Then you just have to run the script. That's it. All results will be saved in the same directory. 
If your inputs are already aligned, you can skip aligning by setting `aligned = True` in the script.

Currently, the script brightens the created 456 swath image a bit. The brightness is beeing controlled by the "gain" variable. 
Gain = 1 means, that the output has the same brightness as the input.

The denoise feauture is enabled per default, but can be disabled by setting `denoise = False` in the script.

# Limits
Currently, the aligning is just a quick image modification (move, stretch, mirror) and might not align images properly. 
If thats the case, please align manually and set `aligned = True` to still get your false color composites.

# Composites
Currently, this script supports 5 different composition:
1. General_Green
2. Cold_Color
3. Water
4. Desert_red
5. Desert_blue

