#!/usr/bin/python

from Tkinter import *
import os
import itertools
import operator
import random

class CanonListbox(Frame):
	def __init__(self, master, canonlist):
 		Frame.__init__(self, master)
		frame = Frame(self)
		frame.pack()
		self.lb = Listbox(frame,borderwidth=0, selectborderwidth=0,relief=FLAT, 
				  selectmode=EXTENDED, exportselection=FALSE)
		#self.lb.bind('<B1-Motion>', lambda e, s=self: s._select(e.y))
		#self.lb.bind('<Button-1>', lambda e, s=self: s._select(e.y))
		self.lb.bind('<Control-a>', lambda e, s=self: s._selectall())
		self.lb.bind('<Control-A>', lambda e, s=self: s._selectall())
		self.lb.pack(side=LEFT, fill=BOTH, expand=YES)
		s = Scrollbar(frame, orient=VERTICAL, command=self.lb.yview)
		s.pack(side=RIGHT, fill=Y)
		self.lb['yscrollcommand'] = s.set
		random.shuffle(listofcanons) # randomize the order of appearance...
		fill_list_box(listofcanons,self.lb)

	def get_selection(self):
		try:
			filenamestoreturn = []
			selecteditems = map(int,self.lb.curselection())
			for index in selecteditems:
				filenamestoreturn.append(self.lb.get(index))
			return filenamestoreturn
		except:
			# lozenge - restrict to the right exception... that nothing
			# has been selected
			return None

	def _selectall(self):
		return [self.lb.select_set(ii) for ii in range(self.lb.size())]


class ComparisonWidget(Frame):
	"""two listboxes (yes and no) and label with count"""
	
	#seenstring = StringVar()
	#notseenstring = StringVar()

	def __init__(self, master):
 		Frame.__init__(self, master)
		frameyes = Frame(master,width = 500, height = 300)
		frameyes.pack(side=LEFT, expand=YES, fill=BOTH)
		frameno = Frame(master,width = 500, height = 300)
		frameno.pack(side=LEFT, expand=YES, fill=BOTH)

		self.seenstring = StringVar()
		self.notseenstring = StringVar()

		self.seenstring.set('SEEN: ')
		self.notseenstring.set('NOT SEEN: ')
		yes_label = Label(frameyes, textvariable=self.seenstring, borderwidth=1)
		yes_label.pack(fill=X)
		no_label = Label(frameno, textvariable=self.notseenstring, borderwidth=1)
		no_label.pack(fill=X)


		self.lbyes = Listbox(frameyes,borderwidth=0, selectborderwidth=0,relief=FLAT, 
				  selectmode=EXTENDED, exportselection=TRUE)
		syes = Scrollbar(frameyes, orient=VERTICAL, command=self.lbyes.yview)
		self.lbyes['yscrollcommand'] = syes.set
		self.lbno = Listbox(frameno,borderwidth=0, selectborderwidth=0,relief=FLAT, 
				  selectmode=EXTENDED, exportselection=TRUE)
		sno = Scrollbar(frameno, orient=VERTICAL, command=self.lbno.yview)
		self.lbyes.pack(side=LEFT, fill=BOTH, expand=YES)
		syes.pack(side=LEFT, fill=Y)
		self.lbno.pack(side=LEFT, fill=BOTH, expand=YES)
		sno.pack(side=LEFT, fill=Y)
		self.lbno['yscrollcommand'] = sno.set
		self.lbyes.bind('<Control-a>', lambda e, s=self: s._selectall())
		self.lbno.bind('<Control-a>', lambda e, s=self: s._selectall())

	def fill_yes_and_no(self, yeslist, nolist):
		fill_list_box(self._yesnolistintoreadable(yeslist),self.lbyes)
		fill_list_box(self._yesnolistintoreadable(nolist),self.lbno)
		self.seenstring.set('SEEN: ' + str(len(yeslist)))
		self.notseenstring.set('NOT SEEN: ' + str(len(nolist)))

	def _selectall(self):
		return [self.lbyes.select_set(ii) for ii in range(self.lbyes.size())]


	def clear(self):
		empty_list_box(self.lbyes)
		empty_list_box(self.lbno)
		self.seenstring.set('')
		self.notseenstring.set('')

	def fill_merged_lists(self, mergedyestitles, mergednotitles):
		sortedyes = sorted(mergedyestitles)
		sortedno = sorted(mergednotitles)
		listofgroupedyes = []
		listofgroupedno = []
		for key, group in itertools.groupby(sortedyes,key=str.lower):
			listofgroupedyes.append(list(group))
		for key, group in itertools.groupby(sortedno,key=str.lower):
			listofgroupedno.append(list(group))
		fill_list_box(self._mergesyesnointoreadable(sorted(listofgroupedyes, key=len, reverse=True)),self.lbyes)
		fill_list_box(self._mergesyesnointoreadable(sorted(listofgroupedno, key=len, reverse=True)),self.lbno)
		#fill_list_box(self._mergesyesnointoreadable(sorted(listofgroupedyes)),self.lbyes)
		#fill_list_box(self._mergesyesnointoreadable(sorted(listofgroupedno)),self.lbno)# alphabetical, for checking for near-misses in strings
		
	def _mergesyesnointoreadable(self, groupedyesno):
		# they're lists of lists of movie titles. If len > 1, they all match.
		readablelist = [str(len(row)) + '     ' + self._processfilmtitle(row[0]) for row in groupedyesno]
		return readablelist

	def _yesnolistintoreadable(self,yesnolist):
		"""Save # (if any) and film title, boot rest"""
		readablelist = [self._processnumber(row[0]) + self._processfilmtitle(row[2:]) for row in yesnolist]
		return readablelist

	def _processnumber(self, numberforfilm):
		"""Return empty string is None, and string with space if not"""
		if not numberforfilm:
			return ''
		return str(numberforfilm + ' ')				

	def _processfilmtitle(self, filminfolist):
		"""Make it look nice in the two boxes"""
		try:
			[titleforfilm,extrainfo] = filminfolist
		except:
			titleforfilm = filminfolist
			extrainfo = ''
		try:
			return put_the_at_start(titleforfilm.rstrip().encode("unicode_escape")) + self._process_extra_info(extrainfo).encode("unicode_escape")
		except:
			return put_the_at_start(titleforfilm.rstrip().encode("string_escape")) + self._process_extra_info(extrainfo).encode("string_escape")
		# lozenge - work with spacing to make it look nicer

	def _process_extra_info(self, extrainfo):
		if extrainfo:
			return '   ' + extrainfo.rstrip()				
		return ''

class Dashboard(Frame):
	"""Contains button for sorting and also text information on canon."""
	def __init__(self, master,listboxofcanons, filmdb, comparisonwidget,labelswidget):
 		Frame.__init__(self, master)
		frame = Frame(self)
		sortbutton = Button(frame, text="SHOW", command=lambda: self._sort_into_boxes(listboxofcanons, filmdb, comparisonwidget,labelswidget))
		sortbutton.pack()#.grid(row=0,column=0)
		frame.pack(side=LEFT, expand=YES)

                #self.label.configure(text= format_time_integer(self.remainingfull))


	def _sort_into_boxes(self, listboxofcanons, filmdb, comparisonwidget, labelswidget):
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
			

class FilmDatabase:
	def __init__(self,listofcanons,listoflistoftuplesofdata):
		# make into dict, with canon name as key, and tuple of data as value
		self.filmdict = dict(zip(listofcanons,listoflistoftuplesofdata))

	def break_into_yes_and_no(self, filenameforcanon):
		yeslist = []
		nolist = []
		try:
			listoftuplesoffilmdata = self.filmdict[filenameforcanon][1]
			#print len(listoftuplesoffilmdata) # lozenge-- add to label
			sorteddata = sorted(listoftuplesoffilmdata, key=operator.itemgetter(1))
		except:
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
	
class LabelSetFilm(Frame):
	"""List of labels for film canon information"""
	def __init__(self, master):
 		Frame.__init__(self, master)
		frame = Frame(self)
		self.labeltitle = Label(frame, text='Film canon selected:')
		self.labeldescription = Label(frame, text='')
		self.labeltotal = Label(frame, text='')
		self.labeltitle.grid(row=1,column=0)
		self.labeldescription.grid(row=2,column=0)
		self.labeltotal.grid(row=3,column=0)
		frame.pack()

	def clear(self):
		self.labeltitle.configure(text = '')		
		self.labeldescription.configure(text = '')
		self.labeltotal.configure(text = '')

	def update_labels(self, fname = '', desc = '', filmnum = ''):
		self.labeltitle.configure(text = 'Film canon selected: ' + fname)		
		self.labeldescription.configure(text = desc)
		if filmnum != '':
			self.labeltotal.configure(text = 'Canon has ' + filmnum + ' films total')		

def empty_list_box(menutofill):
	"""empty menu"""
	menutofill.delete(0, END)

def fill_list_box(listofentries,menutofill):
	"""empty menu, and then fill with the contents of list"""
	empty_list_box(menutofill)
	#menutofill.delete(0, END)
	for row in listofentries:
		menutofill.insert(END,row)

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

def process_film_canon_file(filename):
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

if __name__ == '__main__':

	# lozenge - make this less clunky
	class Usage(Exception):
		def __init__(self, msg):
			self.msg = msg

	import sys
	import getopt
	
	try:
		opts, args = getopt.getopt(sys.argv[1:], "ho:vt:z:w:r:", ["help", "output=", "threshold="])
	except getopt.error, msg:
		raise Usage(msg)


	# options:
        '''for option, value in opts:
            if option == "-v":
                verbose = True
            if option in ("-h", "--help"):
                raise Usage(help_message)
            if option in ("-o", "--output"):
                output = value
            if option in ("-t", "--threshoold"):
                threshold = int(value)
            if option == "-z":
                zipcode = int(value)
            if option == "-w":
                weeks = int(value)
            if option == "-r":
                radius = int(value)'''



	folder = './canons'
	listofcanons = []
	ultimatelist = []
	for f in os.listdir(folder):
		fullpath = './canons/' + f
		listofinformation = process_film_canon_file(fullpath)
		ultimatelist.append(listofinformation)
		listofcanons.append(f)
	filmdb = FilmDatabase(listofcanons, ultimatelist)
	
	maintk = Tk()
	maintk.title('Film Canon')
	maintk.geometry("1000x500")

	frametop = Frame(maintk)
	framebottom = Frame(maintk)#,width = 1000, height = 300)
	frametop.pack()#(anchor=N,expand=True,fill=X)
	framebottom.pack(side=LEFT,expand=YES,fill=BOTH)

	labelsforfilms = LabelSetFilm(frametop)
	
	framelistofcanons = Frame(frametop, labelsforfilms)

	framelistofcanons.pack(side=LEFT,expand=True,fill=BOTH)

	listboxofcanons = CanonListbox(framelistofcanons, listofcanons)
	listboxofcanons.pack()
	comparisonwidget = ComparisonWidget(framebottom)
	comparisonwidget.pack(fill=X)
	dashboard = Dashboard(frametop, listboxofcanons, filmdb, comparisonwidget, labelsforfilms)
	dashboard.pack(side=LEFT,expand=True,fill=BOTH)
	labelsforfilms.pack()
	maintk.mainloop()
	# ultimate process:
	# read in all files in folder
	# parse for headers, contents (correct for trailing "the"... or make separate file that does that)
	# fill "files" box with .txt-less filenames. When selected, update label with short header info.
	# 1) Select file. Shows Y on left, N on right
	# 2) Merge files - just merge all files in multiple, show in alphabetical order, descending by "most hit" at top.
