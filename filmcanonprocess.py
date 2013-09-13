#!/usr/bin/python

from Tkinter import *
import os

class CanonListbox(Frame):
    def __init__(self, master,canonlist):
 		Frame.__init__(self, master)
		frame = Frame(self)
		frame.pack()
		lb = Listbox(frame,borderwidth=0, selectborderwidth=0,relief=FLAT, exportselection=FALSE)
		lb.pack(expand=YES, fill=BOTH)
		FillListBox(listofcanons,lb)

'''class Countdown(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
	frame = Frame(self)
	frame.pack()
        self.label = Label(self, text='', width=10)
        self.label.pack()
        self.remaining = 0
	self.remainingfull = 0
	self._job = None

    def countdown(self, firsttrigger=0):

    	if self.remaining <= 0:
#            self.label.configure(text='')
            self.label.configure(text="%d" % self.remainingfull)
	    self.remaining = self.remainingfull
        else:
	    if firsttrigger == 1:
		self.remaining = self.remainingfull
                self.label.configure(text="%d" % self.remaining)
                if self._job is not None:
		    self.after_cancel(self._job)
		    self._job = None
                self.remaining = self.remaining - 1
                self.after(1000, self.countdown)
	    else:
		self.label.configure(text="%d" % self.remaining)
                self.remaining = self.remaining - 1
                self._job = self.after(1000, self.countdown)


    def loadcountdown(self, remaining = None):
        if remaining is not None:
            self.remainingfull = remaining
            self.remaining = remaining
            self.label.configure(text="%d" % self.remaining)

class ButtonArray(Frame):

	def __init__(self, master):
		Frame.__init__(self, master)
		frame = Frame(self)
		frame.pack()
		itunes = app('iTunes')
	
		self.quitbutton = Button(frame, text="QUIT", fg="red", command=frame.quit)
		self.quitbutton.grid(row=0,column=0)
		self.stopbutton = Button(frame,text="STOP", command=lambda: self._stop(itunes))
		self.stopbutton.grid(row=0,column=1)
		playlisttextlist = [StringVar() for i in range(NUMBEROFPLAYLISTS)]
		for text in playlisttextlist:
			text.set("no file loaded")
		self.countdownarray = []
		for ii in range(NUMBEROFPLAYLISTS):
			self.loadbutton= Button(frame,text='LOAD'+str(ii+1), command=lambda ii=ii: self._loadplaylist(itunes,playlisttextlist,ii))
			self.loadbutton.grid(row=ii+1,column=0)
			self.playbutton = Button(frame,text='PLAY'+str(ii+1), command=lambda ii=ii: self._playplaylist(itunes,ii))
			self.playbutton.grid(row=ii+1,column=1)
			self.labelplaylist = Label(frame,textvariable=playlisttextlist[ii])
			self.labelplaylist.grid(row=ii+1,column=2)
			countdown = Countdown(frame)
			self.countdownarray.append(countdown)
			countdown.grid(row=ii+1,column=3)
		#keystroke capture:
		master.bind_all('<F1>', lambda event: self._playplaylist(itunes,0))
		master.bind_all('<F2>', lambda event: self._playplaylist(itunes,1))
		master.bind_all('<F3>', lambda event: self._playplaylist(itunes,2))
		master.bind_all('<F4>', lambda event: self._playplaylist(itunes,3))
		# etc prune to match actual number of playlists

	def _loadplaylist(self,itunes,playlisttextlist,playlistnumber):	
		if filenametoload == '':
			print "NOTHING TO LOAD"
		else:
			playlistTracks = itunes.playlists['SPOTBOX'+str(playlistnumber+1)].tracks()
			if len(playlistTracks) > 0:
				itunes.delete(itunes.playlists['SPOTBOX'+str(playlistnumber+1)].tracks)
			itunes.add(Alias(filenametoload),to=itunes.playlists['SPOTBOX'+str(playlistnumber+1)])
			filenamesplit = SplitFileName(filenametoload)
			playlisttextlist[playlistnumber].set(filenamesplit[3])
			[minutes,seconds] = filenamesplit[2].split('.')
			timetoload = 60*int(minutes) + int(seconds)
			self.countdownarray[playlistnumber].loadcountdown(timetoload)

	def _playplaylist(self,itunes,playlistnumber):
		itunes.play(itunes.playlists['SPOTBOX'+str(playlistnumber+1)])
		self.countdownarray[playlistnumber].countdown(1)

	def _stop(self,itunes):
		itunes.stop()

class RadioCategory(Frame):

	def __init__(self, master):
		Frame.__init__(self, master)
		frame = Frame(self)
		frame.pack()		
		types = [("PSA",1),("LID",2),("Promos",3),("Sound Effects",4),("Show Themes",5)]
		ii = 0
		for txt, modenum in types:
			Radiobutton(frame, text=txt, indicatoron = 0, variable = menumode, command=self._UpdateMenus,value=modenum).grid(row=0,column=ii)
			ii += 1		
	
	def _UpdateMenus(self):
		for menu in menulist:
			menu.grid_forget()
		menulist[menumode.get()-1].grid(row=1,columnspan=2)
		searchbox.clear()
		global currentmatrix
		currentmatrix = matrixlist[menumode.get()-1]
		for ii in range(len(menulist)):
		    if (ii != (menumode.get()-1)):
		        matrixtoshuffle = matrixlist[ii]
		        random.shuffle(matrixtoshuffle)
		        menulist[ii].delete(0, END)
		        FillListBox(matrixtoshuffle,menulist[ii])
		
class SearchBox(Frame):

	def __init__(self, master):
		Frame.__init__(self, master)
		frame = Frame(self)
		frame.pack()
		Button(frame,text="Search", command=lambda: self._search()).grid(row=0,column=1)
		self.searchstring = StringVar()
		self.searchentry = Entry(frame, textvariable=self.searchstring)
		self.searchentry.grid(row=0,column=0)
		self.searchstring.set('')
		self.searchentry.bind('<Return>', lambda e: self._search())
	
	def _search(self):
		searchby = self.searchstring.get()
		print searchby
		print 'SEARCH'
		searchmatrix = []
		for row in matrixlist[menumode.get()-1]:
			for part in row:
				if searchby.lower() in part.lower():
					searchmatrix.append(row)
					break 
		menulist[menumode.get()-1].delete(0, END)
		FillListBox(searchmatrix,menulist[menumode.get()-1])
		global currentmatrix
		currentmatrix = searchmatrix
	
	def clear(self):
		self.searchentry.delete(0,END)

class MultiListbox(Frame):

    def __init__(self, master, lists):
	Frame.__init__(self, master)
	self.lists = []
	ii = 0
	for l,w in lists:
	    frame = Frame(self); frame.pack(side=LEFT, expand=YES, fill=BOTH)
	    a_label = Label(frame, text=l, borderwidth=1, relief=RAISED)
	    a_label.pack(fill=X)
	    lb = Listbox(frame, width=w, borderwidth=0, selectborderwidth=0,
			 relief=FLAT, exportselection=FALSE)
	    lb.pack(expand=YES, fill=BOTH)
	    self.lists.append(lb)
	    lb.bind('<B1-Motion>', lambda e, s=self: s._select(e.y))
	    lb.bind('<Button-1>', lambda e, s=self: s._select(e.y))
	    lb.bind('<Leave>', lambda e: 'break')
	    lb.bind('<B2-Motion>', lambda e, s=self: s._b2motion(e.x, e.y))
	    lb.bind('<Button-2>', lambda e, s=self: s._button2(e.x, e.y))
	    lb.bind('<MouseWheel>', self._mousewheel)
	    a_label.bind('<Button-1>', lambda e, ii=ii: self._sort(ii))
	    ii += 1
	frame = Frame(self); frame.pack(side=LEFT, fill=Y)
	Label(frame, borderwidth=1, relief=RAISED).pack(fill=X)
	sb = Scrollbar(frame, orient=VERTICAL, command=self._scroll)
	sb.pack(expand=YES, fill=Y)
	self.lists[0]['yscrollcommand']=sb.set

    def _sort(self,columnnumber):
	global currentmatrix
	deco= [((a[indiceslist[menumode.get()-1][columnnumber]]),a) for a in matrixlist[menumode.get()-1]]
	deco.sort()
	currentmatrix = [v for k,v in deco]
	menulist[menumode.get()-1].delete(0, END)
	FillListBox(currentmatrix,menulist[menumode.get()-1])

    def _select(self, y):
	row = self.lists[0].nearest(y)
	self.selection_clear(0, END)
	self.selection_set(row)
	global filenametoload
	filenametoload = currentmatrix[row][0]	
	return 'break'

    def _button2(self, x, y):
	for l in self.lists: l.scan_mark(x, y)
	return 'break'

    def _b2motion(self, x, y):
	for l in self.lists: l.scan_dragto(x, y)
	return 'break'

    def _mousewheel(self,event):
	for l in self.lists: l.yview("scroll",event.delta,"units")
	return "break"

    def _scroll(self, *args):
	for l in self.lists:
	    apply(l.yview, args)

    def curselection(self):
	return self.lists[0].curselection()

    def delete(self, first, last=None):
	for l in self.lists:
	    l.delete(first, last)

    def get(self, first, last=None):
	result = []
	for l in self.lists:
	    result.append(l.get(first,last))
	if last: return apply(map, [None] + result)
	return result
	    
    def index(self, index):
	self.lists[0].index(index)

    def insert(self, index, *elements):
	for e in elements:
	    i = 0
	    for l in self.lists:
		l.insert(index, e[i])
		i = i + 1

    def size(self):
	return self.lists[0].size()

    def see(self, index):
	for l in self.lists:
	    l.see(index)

    def selection_anchor(self, index):
	for l in self.lists:
	    l.selection_anchor(index)

    def selection_clear(self, first, last=None):
	for l in self.lists:
	    l.selection_clear(first, last)

    def selection_includes(self, index):
	return self.lists[0].selection_includes(index)

    def selection_set(self, first, last=None):
	for l in self.lists:
	    l.selection_set(first, last)

def FileComponentsToTuple(filecomponents):
	tuplereturn = ()
	if filecomponents[1] == 'PSA':
		indices = psaindices
	elif filecomponents[1] == 'LID':
		indices = lidindices

	for index in indices:
		try:
			tuplereturn = tuplereturn + (filecomponents[index],)
		except:
			print "SOMETHING MALFORMED"
	return tuplereturn

def SplitFileName(filename):
	# Look at only the file, remove file extension, and split into array on commas:
	filenamecomponents = (((filename.rsplit('/',1))[1]).rsplit('.',1)[0]).split('_')
	filenamecomponents.insert(0, filename)
	return filenamecomponents

def FillListBox(filematrix,menutofill):
    for row in filematrix:
        menutuple =  FileComponentsToTuple(row)
        try:
            menutofill.insert(END,menutuple)
        except:
            menutofill.insert(END,("error"))
            print "FILENAME FOR " + row[0] + " NOT VALID"

def ExtractListFromDir(directorystring):
	directorylisting = os.listdir(directorystring)
	filenamelist = [SplitFileName(directorystring+x) for x in directorylisting if not x[0] == '.']
	return filenamelist'''
def FillListBox(filematrix,menutofill):
    for row in filematrix:
        menutofill.insert(END,row)
        '''try:
            menutofill.insert(END,menutuple)
        except:
            menutofill.insert(END,("error"))
            print "FILENAME FOR " + row[0] + " NOT VALID"'''

if __name__ == '__main__':
    maintk = Tk()
    folder = 'C:/pythontest/film/canons'
    listofcanons = []
    for f in os.listdir(folder):
        print f
        listofcanons.append(f)
    listboxofcanons = CanonListbox(maintk,listofcanons)
    #listboxofcanons.grid(row=0,column=1)
    listboxofcanons.pack(expand='Yes',fill='both')
	
    maintk.mainloop()
'''	# global file -- the "clipboard" value of the filename that is waiting to be loaded.
	filenametoload = ''
	# Global variable: menumode = PSA=1/LID=2/etc. Defaults to PSA.
	menumode = IntVar()
	menumode.set(1)

    	psamenu = MultiListbox(tk, (('Subject ', 40), ('Time', 10), ('Soundbed', 20), ('Voice/Author', 20)))
	psaindices = [3,2,4,5]
	lidmenu = MultiListbox(tk, (('Speaker/Subject', 60), ('Time', 10), ('LID Type', 20)))
	lidindices = [3,2,4]
	promomenu = MultiListbox(tk, (('Show', 40), ('Time', 10), ('Day/Time', 20), ('Voice/Author', 20)))
	promoindices = []
	sfxmenu = MultiListbox(tk, (('Sound Effect', 60), ('Time', 10), ('Type', 20)))
	sfxindices = []
	thememenu = MultiListbox(tk, (('Song', 30), ('Time', 10),('Artist', 20),('KZSU DJ/show', 30)))
	themeindices = []
	
	menulist = []
	indiceslist = []

	menulist.append(psamenu)	
	menulist.append(lidmenu)
	menulist.append(promomenu)
	menulist.append(sfxmenu)
	menulist.append(thememenu)
	indiceslist.append(psaindices)
	indiceslist.append(lidindices)
	indiceslist.append(promoindices)
	indiceslist.append(sfxindices)
	indiceslist.append(themeindices)
	
	buttonarray = ButtonArray(tk)
	radiocat = RadioCategory(tk)
	searchbox = SearchBox(tk)
	
	parentdirectory = '/Users/automation/Desktop/SPOTBOX_test/'
	directorylist = [parentdirectory + 'PSA/',parentdirectory + 'LID/',parentdirectory + 'PROMO/',parentdirectory + 'SFX/',parentdirectory + 'THEME/']

	matrixlist = []
	for ii in range(len(menulist)):
		matrixlist.append(ExtractListFromDir(directorylist[ii]))

	currentmatrix = []
	currentmatrix = matrixlist[menumode.get()-1]


	for ii in range(len(menulist)):
		FillListBox(matrixlist[ii],menulist[ii])

	#graphicfile = '/Users/automation/Desktop/SPOTBOX_test/spotboxgraphic1.gif'
	#graphic = PhotoImage(file = graphicfile)
	#graphicw = Label(tk, image=graphicfile)
	#graphicw.image = graphicfile
	#graphicw.grid(row=0,column=0)
	
	buttonarray.grid(row=0,column=1)
	psamenu.grid(row=1,columnspan=2)
	searchbox.grid(row=2,column=0)	
	radiocat.grid(row=2,column=1)	
    	'''