from PIL import Image
import numpy as np
from scipy.spatial import KDTree
import sys

VGA_COLORS_16 = [
	(   0,   0,   0 ),
	( 170,   0,   0 ),
	(   0, 170,   0 ),
	( 170,  85,   0 ),
	(   0,   0, 170 ),
	( 170,   0, 170 ),
	(   0, 170, 170 ),
	( 170, 170, 170 ),
	(  85,  85,  85 ),
	( 255,  85,  85 ),
	(  85, 255,  85 ),
	( 255, 255,  85 ),
	(  85,  85, 255 ),
	( 255,  85, 255 ),
	(  85, 255, 255 ),
	( 255, 255, 255 )
]

X = Y = 0

def calculateY(image):
    global X, Y

    aspectRatio = image.height / image.width
    Y = int(X * aspectRatio)

def imageToPixelsArray(image, outputTxt, outputImage):
    global X, Y

    try:
        img = Image.open(image)
        img = img.convert('RGB')

        if (Y < 0):
            calculateY(img)

        if (X):
		# Resize the image to fit within the target size while maintaining aspect ratio
		img.thumbnail((X, Y), Image.Resampling.LANCZOS)

        pixel_array = np.array(img)
        color_tree = KDTree(VGA_COLORS_16)
        h, w, _ = pixel_array.shape
        vga_pixels = pixel_array.reshape(-1, 3)
        _, nearest_indices = color_tree.query(vga_pixels)
        vga_array = nearest_indices.reshape(h, w)
        
        with open(outputTxt, 'w') as f:
            f.write("{\n")
            for row in vga_array:
                f.write("{ " + ','.join(map(str, row)) + " },\n")
            f.write("};\n")
            
        print(f"VGA pixels array saved to {outputTxt}.")
        
        vga_pixel_array = np.array(VGA_COLORS_16)[nearest_indices].reshape(h, w, 3)
        vga_image = Image.fromarray(vga_pixel_array.astype('uint8'))
        vga_image.save(outputImage)
        print(f"VGA image saved to {outputImage}.")
    except Exception as e:
        print(f"Error: {e}")

def main():
    global X, Y
    size = len(sys.argv)

    if (size < 2):
        print("Usage: python3 convert.py <arg1:image path> [<arg2: width> <arg3: height>]")
        return

    image = sys.argv[1]

    if (size > 2):
        X = int(sys.argv[2], 10)
        if (size > 3):
            Y = int(sys.argv[3], 10)
        else:
            Y = -1

    outputTxt   = f"pixelsArray_{image}.txt"
    outputImage = f"vga_image_{image}.png"
    
    imageToPixelsArray(image, outputTxt, outputImage)

if __name__ == "__main__":
    main()
