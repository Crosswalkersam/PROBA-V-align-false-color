# ASCATdenoise
This project aims to get rid of the vertical lines that occur on metOp ASCAT images.

# Requirements
For this script to work, you need Python 3 installed and added to PATH. 
After you installed Python on your machine, you need to install Image and matplotlib by running
`pip install Image` and `pip install matplotlib`.

# Usage
Simply put an ASCAT-image named `input.png` into the same directory as the script.
Then you just have to run the script. That's it. All results will be saved in the same directory.

# How it works
The script first calculates the average pixel-brightness of each column by adding all values up and dividing by the height.
After we did this, we can see the average brightness of each column in the `noisepattern.png` file created by the script. 
We then substract this noisepattern from every row, normalize the result and get `ASCAT_denoised.png`. 
As an optional 4th step, the script uses matplotlib.pyplot to colorize the image.

![How_it_works](https://user-images.githubusercontent.com/50832240/162627473-8ec708cb-8985-4a3c-87aa-44c9d4116392.png)

# Limits
Currently, each channel has to be treated seperately. The script is still WIP and unable to do batch-proccessing.
The algorithm can theoretically handle the `ASCAT-ALL.png` image created by [satDump](https://github.com/altillimity/SatDump),
but the result for single-channel proccessing is better. Since this uses the average over each row, higher images should give a better result.

