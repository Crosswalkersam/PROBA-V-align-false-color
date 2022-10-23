# PROBA-V Align & False color
This script takes three channels from PROBA-V's vegetation instrument, overlays them and creates false color images.

# Requirements
For this script to work, you need Python 3 installed and added to PATH. 
After you installed Python on your machine, you need to install Image, Imageops, ImageChops and tqdm by running
`pip install Pillow tqdm colorama`.

# Usage
Simply put images named "Vegetation_1.png", "Vegetation_2.png" and "Vegetation_3.png" into the same directory as the script.
Then you just have to run the script. That's it. All results will be saved in the same directory. 
If your inputs are already aligned, you can skip aligning by setting `aligned = True` in the script

# Limits
Currently, the aligning is just a quick image modification (move, stretch, mirror) and might not align images properly. 
If thats the case, please align manually and set `aligned = True` to still get your false color composites.

#Composites
Currently, this script supports 3 different composition:
1. General Green
2. Cold color
3. Water

