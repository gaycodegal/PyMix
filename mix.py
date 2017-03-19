from clinput import getCommandLineInput, printCommandLineOpts

OPTS = {"o":"dest.bin",
        "i":"target.bin"}

def read():
    """ Reads in a file. """
    my_file = open(OPTS["i"],"rb")
    contents = bytearray(my_file.read())
    my_file.close()
    return [len(contents), contents]

def write(contents):
    """ Writes contents to the dst file. 
    Note: applies bytemask if available. """
    flen = len(contents)
    chnk = flen // 20 + 1
    j = 0
    nm = 0
    byte_mask = None
    if("b" in OPTS):
        byte_mask = OPTS["b"]
        while j < flen:
            nm = min(flen, j+chnk)
            print(str(j*100//flen) + "%")
            for i in range(j,nm):
                contents[i] ^= byte_mask
            j += chnk
    print("100%")
    my_file = open(OPTS["o"],"wb")
    my_file.write(contents)
    my_file.close()

def mix():
    """ Puts the first half of the file after the second half
    Note: we'll need an unmix function call for odd length files
    due to flooring. """
    [f_len, contents] = read()
    f_len = f_len // 2
    write(contents[f_len:] + contents[:f_len])
    
def unmix():
    """ Undoes the mix transformation """
    [f_len, contents] = read()
    f_len = f_len - (f_len // 2)
    write(contents[f_len:] + contents[:f_len])

def byte_int(x):
    """ Converts any string of 0s and 1s into an 8 bit number"""
    return int(x,2) & 0xFF
    
def main():
    """ Mixes a file up non-cryptographically 
    so that it can pass cursory checks of filetype.
    1: No bytemask will greatly aid speed, but
    a bytemask will disguise plaintext for you.
    2: Currently only works with files that can
    fit in your computer's ram. Could (and will eventually)
    be modified to work on any size.
    """
    b_in = {"type": byte_int}
    mapping = {
        "h":["help"],
        "i":["src"],
        "o":["dst"],
        "b":["bytemask"]
    }
    inp = getCommandLineInput(formatting = {"b":b_in, "bytemask":b_in}, default_options = OPTS, mapping=mapping)
    if(len(inp.args) <= 1 or 'h' in inp.opts):
        print('Usage: python3 mix.py mix/unmix')
        print('\nDescription:')
        print(main.__doc__)
        printCommandLineOpts(mapping, {
            "b":"<xor byte mask 8 bits> #eg 10010100",
            "i":"<file input path>",
            "o":"<file output path>",
            "h":"#this help"
        })
        return None
    if(inp.args[0].lower() == "mix"):
        mix()
        print("mixed")
    elif(inp.args[0].lower() == "unmix"):
        unmix()
        print("unmixed")
    else:
        print("bad option" + inp.args[1] + " try: -h")

main()
