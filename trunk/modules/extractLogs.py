# receive a list of files, zipped or unzipped,
# extract zipped files, determine which logs are which, and
# return a tuple with (el152, el155, el68)

import re
import zipfile
# these three boolean functions could be implemented in the
# data structure classes instead...
def is_68(fh):
    # TODO implement this function
    return False

def is_152(fh):
    # check first couple of lines
    pattern = r"^(\d*?)\s+(\d*?)\s+(\w+?)\s+(\d+?/\d+?/\d+?\s+\d+?:\d+?:\d+?)\s+(\d+?)\s+(.*?)\s+$"
    lineRe = re.compile(pattern)
    i = 0
    for l in fh:
        if lineRe.match(l):
            return True
        elif i >= 10:
            break
        i += 1

    return False

def is_155(fh):
    # check header...
    precinctPattern = r"PRECINCT\s*(\d+)\s*-\s*(.*)ELECTION"
    precinctRe = re.compile(precinctPattern, re.IGNORECASE)
    i = 0
    for l in fh:
        if precinctRe.search(l):
            return True
        elif i >= 10:
            break
        i += 1

    return False

def extractLogs(files):
    totalReceivedFiles = []
    for f in files:
        if zipfile.is_zipfile(f):
            # extract
            z = zipfile.ZipFile(f, 'r')
            for member in z.infolist():
                m = z.open(member)
                totalReceivedFiles.append(m)
        else:
            totalReceivedFiles.append(f)

    # now determine what each file is
    first68 = None
    first152 = None
    first155 = None
    for f in totalReceivedFiles:
        if is_68(f):
            if first68 != None:
                # TODO Create different exception for this
                raise Exception('More than one el68 files were given')
            else:
                first68 = f
        elif is_152(f):
            if first152 != None:
                # TODO same as above
                raise Exception('More than one el152 files were given')
            else:
                first152 = f
        elif is_155(f):
            if first155 != None:
                # TODO same as above
                raise Exception('more than one el155 files were given')
            else:
                first155 = f
        else:
            # the file is not recognized, ignore it
            pass

    return (first152, first155)
    # TODO uncomment next line after implementing el68 stuff...
    #return (first68, first152, first155)

    
