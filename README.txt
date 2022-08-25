This program converts images to ascii by mapping pixel brightness to characters,
pixel brightness is calculated by taking the average rgb value of a pixel.

At first the image is resized, so that it's longest side is 69px (by default)
to greatly reduce the processing time

The "codec" variable evenly maps every element to a brightness range, assigning
lower and higher brightness ranges from left to right respectively.
codec = [' ', '.', ',', '+', '/', 'a', '%', '@', '$'] #by default

Running the program:
required args:
     the first argument has to specify image file path
optional args (order is unimportant beyond arg1):
     inverted - reversed codec list
     size - set image longest side, the smaller side will be resized accordingly to preserve resolution
     codec=<char[]> - set codec
     to_file - creates an output file in the same directory

Special behaviour, if the specified file is an animated gif,
the program will output a json file with each frame converted.
This json file is compatible with tti.