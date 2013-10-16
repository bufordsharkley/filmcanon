#!/usr/bin/python

from Tkinter import *
import random

class ListboxWithScrollbar(Frame):
    """Subclass for Listbox, featuring scrollbar and select-all behavior"""
    def __init__(self, master, **options):#width=None, height=None):
        Frame.__init__(self, master, **options)#, **options)
        self.lb = Listbox(self,borderwidth=0, selectborderwidth=0,relief=FLAT, 
                  selectmode=EXTENDED, exportselection=TRUE)
        self.lb.bind('<Control-a>', lambda e, s=self: s._selectall())
        self.lb.bind('<Control-A>', lambda e, s=self: s._selectall())
        self.lb.pack(side=LEFT, fill=BOTH, expand=YES)
        s = Scrollbar(self, orient=VERTICAL, command=self.lb.yview)
        s.pack(side=LEFT, fill=Y)
        self.lb['yscrollcommand'] = s.set

    def fill(self,listofentries):
        """empty menu, and then fill with the contents of list"""
        self.empty()
        for row in listofentries:
            self.lb.insert(END,row)

    def empty(self):
        """empty menu"""
        self.lb.delete(0, END)

    def _selectall(self):
        return [self.lb.select_set(ii) for ii in range(self.lb.size())]

class CanonListbox(ListboxWithScrollbar):
    def __init__(self, master, canonlist):
        ListboxWithScrollbar.__init__(self, master)
        random.shuffle(canonlist) # randomize the order of appearance...
        self.fill(canonlist)

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

class Dashboard(Frame):
    """Contains button for sorting and also text information on canon."""
    def __init__(self, master,listboxofcanons, filmdb, comparisonwidget,labelswidget):
        Frame.__init__(self, master)
        self._sortfunction = None
        sortbutton = Button(self, text="SHOW", command = lambda: self._sort(listboxofcanons, filmdb, comparisonwidget, labelswidget))
        sortbutton.pack()#.grid(row=0,column=0)
        #self.label.configure(text= format_time_integer(self.remainingfull))

    def _sort(self, listboxofcanons, filmdb, comparisonwidget, labelswidget):
        if self._sortfunction:
            self._sortfunction(listboxofcanons, filmdb, comparisonwidget, labelswidget)
        else:
            print 'NO SORT' 

    def update_sort_function(self, newsortfunction):
        self._sortfunction = newsortfunction

class LabelSetFilm(Frame):
    """List of labels for film canon information"""
    def __init__(self, master):
        Frame.__init__(self, master)
        self.labeltitle = Label(self, text='Film canon selected:')
        self.labeldescription = Label(self, text='')
        self.labeltotal = Label(self, text='')
        self.labeltitle.grid(row=1,column=0)
        self.labeldescription.grid(row=2,column=0)
        self.labeltotal.grid(row=3,column=0)

    def clear(self):
        self.labeltitle.configure(text = '')        
        self.labeldescription.configure(text = '')
        self.labeltotal.configure(text = '')

    def update_labels(self, fname = '', desc = '', filmnum = ''):
        self.labeltitle.configure(text = 'Film canon selected: ' + fname)        
        self.labeldescription.configure(text = desc)
        if filmnum != '':
            self.labeltotal.configure(text = 'Canon has ' + filmnum + ' films total')        

class ComparisonWidget(Frame):
    """two listboxes (yes and no) and label with count"""

    def __init__(self, master):
        Frame.__init__(self, master)
        frameleft = Frame(master)
        frameright = Frame(master)
        self.frameyes = ListboxWithScrollbar(frameleft)
        self.frameno = ListboxWithScrollbar(frameright)
        self.seenstring = StringVar()
        self.notseenstring = StringVar()
        self.seenstring.set('SEEN: ')
        self.notseenstring.set('NOT SEEN: ')
        yes_label = Label(frameleft, textvariable=self.seenstring, borderwidth=1)
        no_label = Label(frameright, textvariable=self.notseenstring, borderwidth=1)
        yes_label.pack()
        no_label.pack()
        self.frameyes.pack(side=LEFT, expand=YES, fill=BOTH)
        self.frameno.pack(side=LEFT, expand=YES, fill=BOTH)
        frameleft.pack(side=LEFT, expand=YES, fill=BOTH)
        frameright.pack(side=LEFT, expand=YES, fill=BOTH)
        # functions for creating data for sheets:
        self.fcnforreadability = None        
        self.fcnforgrouping = None

    def fill_yes_and_no(self, yeslist, nolist):
        if self.fcnforreadability:
            self.frameyes.fill(self.fcnforreadability(yeslist))
            self.frameno.fill(self.fcnforreadability(nolist))
            self.seenstring.set('SEEN: ' + str(len(yeslist)))
            self.notseenstring.set('NOT SEEN: ' + str(len(nolist)))

    def clear(self):
        self.frameyes.empty()
        self.frameno.empty()
        #empty_list_box(self.frameno.lb)
        self.seenstring.set('')
        self.notseenstring.set('')

    def fill_merged_lists(self, mergedyestitles, mergednotitles):
        if self.fcnforgrouping:
            fillyes, fillno = self.fcnforgrouping(mergedyestitles, mergednotitles)
            self.frameyes.fill(fillyes)
            self.frameno.fill(fillno)

    def update_backend_functions(self, fcnreadable, fcngrouping):
        self.fcnforreadability = fcnreadable
        self.fcnforgrouping = fcngrouping

        
class Tkinterface(Tk):
    def __init__(self, listofcanons, filmdb):
        Tk.__init__(self)
        self.title('Film Canon')
        self.geometry("1000x500")
        frame = Frame(self)
        frame.pack(expand=True, fill=BOTH)

        frametop = Frame(frame)
        framebottom = Frame(frame)
        frametop.pack()
        framebottom.pack(side=LEFT,expand=YES,fill=BOTH)

        labelsforfilms = LabelSetFilm(frametop)
        
        framelistofcanons = Frame(frametop, labelsforfilms)

        framelistofcanons.pack(side=LEFT,expand=True,fill=BOTH)

        listboxofcanons = CanonListbox(framelistofcanons, listofcanons)
        listboxofcanons.pack()
        self.comparisonwidget = ComparisonWidget(framebottom)
        self.comparisonwidget.pack(fill=X)
        self.dashboard = Dashboard(frametop, listboxofcanons, filmdb, self.comparisonwidget, labelsforfilms)
        self.dashboard.pack(side=LEFT,expand=True,fill=BOTH)
        labelsforfilms.pack()

    def run_continuously(self):
        self.mainloop()

if __name__ == '__main__':
    pass
