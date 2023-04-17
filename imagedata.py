import argparse
from PIL import Image
from PIL.ExifTags import TAGS
from stegano import lsb



def getMetaData(image_file, out):
    try:
        #Empty Dict
        metaData = {}
        imgFile = Image.open(image_file)
        print ("Getting meta data...")
        info = imgFile._getexif()
        # print(info)
        if info:
            print ("found meta data!")
            for (tag, value) in info.items():
                tagname = TAGS.get(tag, tag)
                metaData[tagname] = value
                if not out:
                    print (tagname, value)

            if out:
                print ("Outputting to file...")
                with open(out, 'w') as f:
                    for (tagname, value) in metaData.items():
                        f.write(str(tagname)+"\t"+\
                            str(value)+"\n")
        
    except:
        print ("Failed")

def hide(image_file, message):
    try:
        secret = lsb.hide(image_file, message)
        secret.save("./hidden.png")
    except :
        print("Error in hiding data")
        


def show(image_file):
    try:
        clear_message = lsb.reveal("./hidden.png")
        print(clear_message)
    except:
        print("Error in showing data")

def Main():
    parser = argparse.ArgumentParser(
        description="Image metadata and steganography tool")
    subparsers = parser.add_subparsers(title="subcommands", dest="command")

    metadata_parser = subparsers.add_parser(
        "metadata", help="get metadata from an image file")
    metadata_parser.add_argument("image_file", help="path to image file")
    metadata_parser.add_argument("-o", "--output", help="output file path")

    hide_parser = subparsers.add_parser(
        "hide", help="hide a message in an image file")
    hide_parser.add_argument("image_file", help="path to image file")
    hide_parser.add_argument("message", help="message to hide in the image")

    show_parser = subparsers.add_parser(
        "show", help="retrieve a hidden message from an image file")
    show_parser.add_argument("image_file", help="path to image file")

    args = parser.parse_args()

    if args.command == "metadata":
        getMetaData(args.image_file, args.output)
    elif args.command == "hide":
        hide(args.image_file, args.message)
    elif args.command == "show":
        show(args.image_file)


if __name__ == "__main__":
    Main()
