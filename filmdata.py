#!/usr/bin/python

"""Data backend for film canon program"""

import itertools
import operator

class FilmDatabase:
    def __init__(self, canons, listoflistoftuplesofdata):
        """ make into dict, with canon name as key, and tuple of data as value"""
        self.filmdict = dict(zip(canons, listoflistoftuplesofdata))

    def break_into_yes_and_no(self, filenameforcanon):
        """Scans through a particular film canon (given by filename)
        and looks through second token: Y or N, returning a list of 
        films corresponding to each"""
        yeslist = []
        nolist = []
        try:
            listoftuplesoffilmdata = self.filmdict[filenameforcanon][1]
            #print len(listoftuplesoffilmdata) # lozenge-- add to label
            sorteddata = sorted(listoftuplesoffilmdata, key=operator.itemgetter(1))
        except:
            #print filenameforcanon
            print 'Error pulling from database'
            sorteddata = []
        try:        
            for key, yesnogroup in itertools.groupby(sorteddata,operator.itemgetter(1)):
                if key == 'Y':
                    yeslist = list(yesnogroup)
                elif key == 'N':
                    nolist = list(yesnogroup)
                elif key == '':
                    print 'Still need to process ' + str(len(list(yesnogroup))) + ' entries.'
                else:
                    print 'What is this?' + str(list(yesnogroup))
        except:
            print 'Error in grouping'
        return yeslist, nolist

    def get_description_from_filename(self, filename):
        return self.filmdict[filename][0]

    def get_numfilms_from_filename(self, filename):
        return len(self.filmdict[filename][1])

def process_film_canon_file(filename):
    """Open file, read header, process body into list of tuples"""
    f = open(filename)
    # top 4 lines contain special information
    # only first line important here:
    shortdescription = f.readline()
    for ii in range(3):
        # burn the other three header lines
        f.readline()
    listincanon = []
    for ii, line in enumerate(f):
        (ranking,yesno,filmtitle,extrametainfo) = process_film_line(line)
        listincanon.append((ranking,yesno,filmtitle,extrametainfo))
    return shortdescription, listincanon

def process_film_line(filmline):
    '''break on underscores, process Y or N, and return 
    Y/N, film title (corrected for terminal "the" etc),
    ranking on page, plus extrametadata'''
    # get leftmost: ranking (delimited by first space)
    try:
        [ranking,yesno,filmandinfo] = filmline.split(' ', 2)
    except:
        filmandinfo = 'FIXLINEFIXLINE'
        ranking = ''
        yesno = 'N'
        print 'Fix line: ' + filmline
    if ranking == '~':
        ranking = ''
    yesno = yesno.upper()
    if yesno != 'Y' and yesno != 'N':
        yesno = ''
    try:
        [filmtitle, extrametainfo] = filmandinfo.split('_',1)
    except:
        # put it all as the title:
        filmtitle = filmandinfo
        extrametainfo = ''
    return (ranking,yesno,put_the_at_end(filmtitle.rstrip()),extrametainfo)

def sort_into_boxes(listboxofcanons, filmdb, comparisonwidget, labelswidget):
    filenamelist = listboxofcanons.get_selection()
    if len(filenamelist) == 1:
        filename = filenamelist[0]
        yeslist,nolist = filmdb.break_into_yes_and_no(filename)
        comparisonwidget.fill_yes_and_no(yeslist,nolist)
        updateinfo = filename
        description = filmdb.get_description_from_filename(filename).rstrip()
        filmno = filmdb.get_numfilms_from_filename(filename)
        labelswidget.update_labels(fname = filename, desc = description, filmnum = str(filmno))
    else: # if more than one list is selected, merge:
        mergedyestitles = []
        mergednotitles = []
        for filename in filenamelist:
            yeslist,nolist = filmdb.break_into_yes_and_no(filename)
            mergedyestitles.extend([film[2] for film in yeslist])
            mergednotitles.extend([film[2] for film in nolist])
        comparisonwidget.clear()
        labelswidget.clear()
        labelswidget.update_labels(fname = 'MULTIPLE LIST MERGE')
        comparisonwidget.fill_merged_lists(mergedyestitles,mergednotitles)


# STUFF ABOUT READABILITY:

def put_the_at_end(stringtocheck):
    correctedstring = stringtocheck
    tocheck = ['The ', 'A ', 'La ', 'L\'','Il ', 'An ']
    for substring in tocheck:
        if stringtocheck.startswith(substring):
            # move from the end to the beginning
            correctedstring = correctedstring[len(substring):] + ', ' + substring[:-1]
            # if substring was L', we've just severed the apostrophe. Add it back.
            if substring == 'L\'':
                correctedstring += '\''
    return correctedstring

def put_the_at_start(stringtocheck):
    # if there is a ", the" clause at end,
    # put at start, for readability
    correctedstring = stringtocheck
    tocheck = [', The', ', A', ', La', ', L\'', ', Il', ', An']
    for substring in tocheck:
        if stringtocheck.endswith(substring):
            # move from the end to the beginning
            correctedstring = substring[2:] + ' ' + correctedstring[:-len(substring)]
    return correctedstring

def processnumber(numberforfilm):
    """Return empty string is None, and string with space if not"""
    if not numberforfilm:
        return ''
    return str(numberforfilm + ' ')

def process_extra_info(extrainfo):
    if extrainfo:
        return '   ' + extrainfo.rstrip()                
    return ''

# (this is way too specific... needs to be generalized)
def processfilmtitle(filminfolist):
    """Make it look nice in the two boxes"""
    try:
        [titleforfilm,extrainfo] = filminfolist
    except:
        titleforfilm = filminfolist
        extrainfo = ''
    try:
        return put_the_at_start(titleforfilm.rstrip().encode("unicode_escape")) + process_extra_info(extrainfo).encode("unicode_escape")
    except:
        return put_the_at_start(titleforfilm.rstrip().encode("string_escape")) + process_extra_info(extrainfo).encode("string_escape")
    # lozenge - work with spacing to make it look nicer

def yesnolistintoreadable(yesnolist):
    """Save # (if any) and film title, boot rest"""
    readablelist = [processnumber(row[0]) + processfilmtitle(row[2:]) for row in yesnolist]
    return readablelist

def mergesyesnointoreadable(groupedyesno):
    # they're lists of lists of movie titles. If len > 1, they all match.
    readablelist = [str(len(row)) + '     ' + processfilmtitle(row[0]) for row in groupedyesno]
    return readablelist

def group_yes_and_no(mergedyestitles, mergednotitles):
    sortedyes = sorted(mergedyestitles)
    sortedno = sorted(mergednotitles)
    listofgroupedyes = []
    listofgroupedno = []
    for key, group in itertools.groupby(sortedyes,key=str.lower):
        listofgroupedyes.append(list(group))
    for key, group in itertools.groupby(sortedno,key=str.lower):
        listofgroupedno.append(list(group))
    return (mergesyesnointoreadable(sorted(listofgroupedyes, key=len, reverse=True)),
            mergesyesnointoreadable(sorted(listofgroupedno, key=len, reverse=True)))

if __name__ == '__main__':
    pass
