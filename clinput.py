import sys

def no_cast(x):
    """ applies no transformation """
    return x

class CLInput:
    '''
    A class for making command line input more usable
    by converting optional arguments into dictionary
    format and typecasting input automatically.
    
    enums:
    NORMAL: one arg per option, unless the next arg is a
    command. Additional args are pumped into buffer.
    ONE: one arg per option. Additional pumped.
    RUN: Run Until Next command - concats args until next
    command with spaces between
    '''
    [NORMAL,ONE,RUN] = range(3)
    def __init__(self, source = None, formatting = {}, opts = {}, mapping = {}):
        '''parses command line input into usable form'''
        self.args = []
        self.opts = opts
        
        if(source == None):
            source = sys.argv
        i = 1
        len_source = len(source)
        command = None
        cmd = None
        fcmd = None
        while i < len_source:
            cmd = source[i]
            if(cmd[0] == "-"):
                if(cmd[1] == '-'):
                    command = cmd[2:]
                else:
                    command = cmd[1:]
                if(command in formatting):
                    fcmd = formatting[command]
                else:
                    fcmd = self.NORMAL
                convert = no_cast
                method = self.NORMAL
                arg = ''
                if(type(fcmd) == dict):
                    if("type" in fcmd):
                        convert = fcmd["type"]
                    if("in" in fcmd):
                        method = fcmd["in"]
                elif(fcmd != None):
                    method = fcmd
                if(method == self.ONE or (method == self.NORMAL and i + 1 < len_source and source[i + 1][0] != '-')):
                    i += 1
                    arg = source[i]
                elif(method == self.RUN):
                    arg = []
                    while(i + 1 < len_source and source[i+1][0] != '-'):
                        i += 1
                        arg.append(source[i])
                    arg = " ".join(arg)
                self.opts[command] = convert(arg)
            else:
                self.args.append(source[i])       
            i += 1

        if("__fargs" in formatting):
            self.map_args(formatting["__fargs"])
        self.map_bindings(mapping)

    def map_args(self, fargs):
        """ makes sure that the primary mapping is set """
        i = 0
        args = self.args
        alen = len(args)
        flen = min(alen, len(fargs))
        while i < alen:
            for j in range(flen):
                args[i] = fargs[j](args[i])
                i += 1
        
    def map_bindings(self, bindings):
        '''ensures that the master binding is set in self.opts if provided
        with such a master binding list.'''
        opts = self.opts
        for master in bindings:
            if not master in opts:
                for variant in bindings[master]:
                    if variant in opts:
                        opts[master] = opts[variant]
                        opts.pop(variant)
                        break

def FCLInput(CLInput):
    '''
    a fake command line input for when actual command
    line not available, like when running in IDLE
    '''
    def __init__(self, args = [], opts = {}):
        '''purely sets fields'''
        self.args = args
        self.opts = opts
        
def getCommandLineInput(failure_input = [], formatting = {}, default_options = {}, mapping = {}):
    """ simplified call to getting the command line input """
    if(len(sys.argv) <= 1):
        return CLInput(failure_input, formatting, default_options, mapping)
    return CLInput(sys.argv, formatting, default_options, mapping)

def printCommandLineOpts(mapping, optHelp = {}):
    """ prints options prettily from mapping """
    print("Options:")
    for command in mapping:
        altlist = ["-"+command]
        alternates = mapping[command]
        for alternate in alternates:
            altlist.append("--" + alternate)
        comment = "# obvious"
        if command in optHelp:
            comment = optHelp[command]
        print("/".join(altlist)+":",comment)
    print()

    

