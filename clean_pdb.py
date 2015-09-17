#! /usr/bin/python3.4

import sys, getopt

def main(argv):
    inputfile = ''
    outputfile = ''
    chain_identifiers = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:c:",["ifile=","ofile=","ident="])
    except getopt.GetoptError:
        print('clean_pdb.py -i <inputfile> -o <outputfile> -c <chain identifiers>')
        print('type: clean_pdb.py -h for help')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('Reads a pdb file and outputs lines with list of record names (ATOM, TER)')
            print('in the order they are found in the file. Record names corresponds to the first 6')
            print('colums of each line, and can be multiple record names if concatenated with a &.')
            print('It takes 3 parameters:')
            print('    1. An input PDB file.')
            print('    2. An output PDB file.')
            print('    3. a string of chain identifiers separated by &')
            print('       Example: A&B&F. Identifiers are case sensitive')
        else:
            if opt in ("-i", "--ifile"):
                inputfile = arg
            elif opt in ("-o", "--ofile"):
                outputfile = arg
            elif opt in ("-c", "--ident"):
                chain_identifiers = arg
    
            print('Procecing',inputfile,'for chains',chain_identifiers)
            readfile(inputfile)

def readfile(inpfile):
    inFile = open(inpfile, 'r')
    lines = [line.rstrip('\n') for line in inFile]
    '''with inFile as f:
        content = f.readlines() content is also a list'''
    inFile.close()

    for i in lines:
        print('This is the line',i)

if __name__ == "__main__":
    main(sys.argv[1:])
