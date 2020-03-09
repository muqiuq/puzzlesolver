import os
import argparse

sqlite_marker_hex_str = "53514c69746520666f726d6174203300"
sqlite_marker = bytes.fromhex(sqlite_marker_hex_str)
mappingtable = {}

filename = "output.pdf.zip"

parser = argparse.ArgumentParser("PuzzleSolver")
parser.add_argument('filename', metavar='F', type=str, help="file of puzzle to solve")
parser.add_argument('--reverse','-r', action='store_true', help="unsolve a solved puzzle")

def encode(filename):
    global sqlite_marker

    new_filename = filename + ".sqlite"

    new_file = open(new_filename, "wb")

    c = 1

    for b in sqlite_marker:
        new_file.write(b.to_bytes(1, byteorder='big'))

    with open(filename, "rb") as f:
        readbytes = f.read(1)
        while readbytes != b"":
            byte = readbytes[0]
            byte = (byte + c) % 256
            c += 1
            if c == 10:
                c = 1
            new_file.write(byte.to_bytes(1, byteorder='big'))
            readbytes = f.read(1)

    new_file.close()

def decode(filename: str):
    global sqlite_marker
    new_filename = filename.replace(".sqlite","",1).replace(".out","")
    new_filename = new_filename + ".out"

    new_file = open(new_filename, "wb")

    markerskip = True
    markercounter = 0
    diderror = False

    c = 1

    with open(filename, "rb") as f:
        readbytes = f.read(1)
        while readbytes != b"":
            byte = readbytes[0]
            if markerskip:
                if byte != sqlite_marker[markercounter]:
                    diderror = True
                    print("Error invalid file signature")
                    break
                markercounter += 1
                if markercounter == len(sqlite_marker):
                    markerskip = False
            else:
                byte = byte - c
                if byte < 0:
                    byte += 256
                c += 1
                if c == 10:
                    c = 1
                new_file.write(byte.to_bytes(1, byteorder='big'))
            # Read next byte
            readbytes = f.read(1)

    new_file.close()
    if diderror:
        os.remove(new_filename)

if __name__ == "__main__":
    args = parser.parse_args()
    if args.reverse:
        decode(args.filename)
    else:
        encode(args.filename)
