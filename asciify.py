from PIL import Image

#[' ', '.', ',', '+', '/', 'a', '%', '@', '$']
def to_string(image, size = None, inverted = False, codec = None):
    if size == None:
        size = 69
    if codec == None:
        codec = [' ', '.', ',', '+', '/', 'a', '%', '@', '$']
    if inverted: codec.reverse()

    #resize image
    image_size = ()
    if image.size[0] > image.size[1]:
        image_size = (size, int(image.size[1] * (size / image.size[0])))
    else:
        image_size = (int(image.size[0] * (size / image.size[1])), size)
    image = image.resize(image_size)

    image = image.convert("RGB")
    pixel_data = image.load()

    #map pixel brightness to codec
    asciified_image = ""
    for y in range(image.size[1]):
        for x in range(image.size[0]):
            rgb = pixel_data[x, y]
            brightness = (rgb[0] + rgb[1] + rgb[2]) / 3

            index = int((brightness-1) / (255 / len(codec)))
            asciified_image += codec[index] + ' '
        asciified_image += '\n'

    return asciified_image

if __name__ == "__main__":
    import sys
    import os
    from PIL import Image
    from moviepy.editor import VideoFileClip
    import time
    import json

    size = None
    inverted = False
    codec = None
    to_file = False

    for argument in sys.argv[2:]:
        argument = argument.lower()
        if argument == "inverted" or argument == "inv":
            inverted = True
        if argument == "to_file":
            to_file = True
        elif argument.find("="):
            parts = argument.split('=')
            if parts[0] == "size":
                size = int(parts[1])
            elif parts[0] == "codec":
                codec = []
                code = ""
                ignore = False
                for char in parts[1][1:-1]:
                    if char == ',' and not ignore:
                        codec.append(code)
                        code = ""
                    elif char == "'" or char == '"':
                        ignore = not ignore
                    elif ignore:
                        code += char
                codec.append(code)

    if sys.argv[1].split('.')[-1] == "gif":
        animated_image = VideoFileClip(sys.argv[1])
        interval = animated_image.duration / animated_image.reader.nframes / 10
        image_array = []
        for frame in animated_image.iter_frames():
            image = Image.frombuffer("RGB", animated_image.size, frame)
            image_array.append(to_string(image, size, inverted, codec))

        if not to_file:
            frame = 0
            running = True
            while running:
                os.system("cls")

                print(image_array[frame])

                frame += 1
                frame %= len(image_array)
                time.sleep(interval)
        else:
            jsonData = { "frames": image_array, "interval": interval}
            file = open(sys.argv[1].split('.')[0]+".json", "wt")
            file.write(json.dumps(jsonData))
            file.close()
    else:
        asciified_image = to_string(Image.open(sys.argv[1]), size, inverted, codec)
        if to_file:
            path_parts = sys.argv[1].replace('\\', '/').split('/')
            path_parts[-1] = path_parts[-1][:path_parts[-1].find('.')] + "_asciified.txt"
            path = '/'.join(path_parts)

            file = open(path, "wt")
            file.write(asciified_image)
            file.close()
        else:
            print(asciified_image)
