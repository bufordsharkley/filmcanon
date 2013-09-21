#!/usr/bin/python

from Tkinter import *
import os
import itertools
import operator

class CanonListbox(Frame):
	def __init__(self, master, canonlist, filmlabels):
 		Frame.__init__(self, master)
		frame = Frame(self)
		frame.pack()
		self.lb = Listbox(frame,borderwidth=0, selectborderwidth=0,relief=FLAT, 
				  selectmode=SINGLE, exportselection=FALSE)
		self.lb.bind('<B1-Motion>', lambda e, s=self: s._select(e.y))
		self.lb.bind('<Button-1>', lambda e, s=self: s._select(e.y))
		self.lb.pack(side=LEFT, fill=BOTH, expand=YES)
		s = Scrollbar(frame, orient=VERTICAL, command=self.lb.yview)
		s.pack(side=RIGHT, fill=Y)
		self.lb['yscrollcommand'] = s.set
		fill_list_box(listofcanons,self.lb)
		self.labels = filmlabels
	
	def get_selection(self):
		try:
			return self.lb.get(self.lb.curselection())
		except:
			# lozenge - restrict to the right exception... that nothing
			# has been selected
			return None

	def _select(self, y):
		filename = self.lb.get(self.lb.nearest(y))
		self.labels.update_labels(filename)
		# call labels, and update
		return


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
				  selectmode=SINGLE, exportselection=FALSE)
		syes = Scrollbar(frameyes, orient=VERTICAL, command=self.lbyes.yview)
		self.lbyes['yscrollcommand'] = syes.set
		self.lbno = Listbox(frameno,borderwidth=0, selectborderwidth=0,relief=FLAT, 
				  selectmode=SINGLE, exportselection=FALSE)
		sno = Scrollbar(frameno, orient=VERTICAL, command=self.lbno.yview)
		self.lbyes.pack(side=LEFT, fill=BOTH, expand=YES)
		syes.pack(side=LEFT, fill=Y)
		self.lbno.pack(side=LEFT, fill=BOTH, expand=YES)
		sno.pack(side=LEFT, fill=Y)
		self.lbno['yscrollcommand'] = sno.set


	def fill_yes_and_no(self,yeslist,nolist):
		fill_list_box(self._yesnolistintoreadable(yeslist),self.lbyes)
		fill_list_box(self._yesnolistintoreadable(nolist),self.lbno)
		self.seenstring.set('SEEN: ' + str(len(yeslist)))
		self.notseenstring.set('NOT SEEN: ' + str(len(nolist)))

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
		[titleforfilm,extrainfo] = filminfolist
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
	def __init__(self, master):
 		Frame.__init__(self, master)
		frame = Frame(self)
		sortbutton = Button(frame, text="SHOW", command=lambda: self._sort_into_boxes(listboxofcanons, filmdb, comparisonwidget)) # LOZENGE - out of scope
		sortbutton.pack()#.grid(row=0,column=0)
		frame.pack(side=LEFT, expand=YES)

                #self.label.configure(text= format_time_integer(self.remainingfull))


	def _sort_into_boxes(self, listboxofcanons, filmdb, comparisonwidget):
		filename = listboxofcanons.get_selection()
		yeslist,nolist = filmdb.break_into_yes_and_no(filename)
		comparisonwidget.fill_yes_and_no(yeslist,nolist)

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

class LabelSetFilm(Frame):
	"""List of labels for film canon information"""
	def __init__(self, master):
 		Frame.__init__(self, master)
		frame = Frame(self)
		self.labeltitle = Label(frame, text='Film canon selected:')
		self.labeldescription = Label(frame, text='')
		self.labeltotal = Label(frame, text='')
		self.labelseen = Label(frame, text='')
		self.labelnot = Label(frame, text='')
		self.labeltitle.grid(row=1,column=0)
		self.labeldescription.grid(row=2,column=0)
		self.labeltotal.grid(row=3,column=0)
		self.labelseen.grid(row=4,column=0)
		self.labelnot.grid(row=5,column=0)
		frame.pack()

	def update_labels(self, updateinfo):
		self.labeltitle.configure(text = 'Film canon selected: ' + updateinfo)
		

def fill_list_box(listofentries,menutofill):
	"""empty menu, and then fill with the contents of list"""
	menutofill.delete(0, END)
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
		filmandinfo = ''
		'Fix line: ' + filmline
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
	return (ranking,yesno,put_the_at_end(filmtitle),extrametainfo)

def put_the_at_end(stringtocheck):
	# if first word is the or a (what about le la ???)
	# put at end
	# LOZENGE
	return stringtocheck

def put_the_at_start(stringtocheck):
	# if there is a ", the" clause at end,
	# put at start, for readability
	correctedstring = stringtocheck
	if stringtocheck.endswith(', The'):
		correctedstring = 'The ' + correctedstring.rstrip(', The')
	elif stringtocheck.endswith(', A'):
		correctedstring = 'A ' + correctedstring.rstrip(', A')
	elif stringtocheck.endswith(', L\''): # lozenge- doesn't work.
		correctedstring = 'L\'' + correctedstring.rstrip(', L\'')
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
	dashboard = Dashboard(frametop)

	labelsforfilms = LabelSetFilm(dashboard)
	labelsforfilms.pack()
	
	framelistofcanons = Frame(frametop, labelsforfilms)

	framelistofcanons.pack(side=LEFT,expand=True,fill=BOTH)

	listboxofcanons = CanonListbox(framelistofcanons, listofcanons, labelsforfilms)
	listboxofcanons.pack()
	dashboard.pack(side=LEFT,expand=True,fill=BOTH)
	comparisonwidget = ComparisonWidget(framebottom)
	comparisonwidget.pack(fill=X)
	maintk.mainloop()
	# ultimate process:
	# read in all files in folder
	# parse for headers, contents (correct for trailing "the"... or make separate file that does that)
	# fill "files" box with .txt-less filenames. When selected, update label with short header info.
	# 1) Select file. Shows Y on left, N on right
	# 2) Merge files - just merge all files in multiple, show in alphabetical order, descending by "most hit" at top.
