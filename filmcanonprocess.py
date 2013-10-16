#!/usr/bin/python

from Tkinter import *
import os
import itertools
import filmdata
import filmgui

if __name__ == '__main__':
    # build the data backend:
    folder = './canons'
    listofcanons = []
    ultimatelist = []
    for f in os.listdir(folder):
        fullpath = './canons/' + f
        listofinformation = filmdata.process_film_canon_file(fullpath)
        ultimatelist.append(listofinformation)
        listofcanons.append(f)
    filmdb = filmdata.FilmDatabase(listofcanons, ultimatelist)

    # import the frontend:
    gui = filmgui.Tkinterface(listofcanons, filmdb)
    # WIRE UP THE FRONT END AND BACK END
    gui.dashboard.update_sort_function(filmdata.sort_into_boxes)
    gui.comparisonwidget.update_backend_functions(fcnreadable = filmdata.yesnolistintoreadable, fcngrouping = filmdata.group_yes_and_no)

    # let it go:
    gui.run_continuously()

    # ultimate process:
    # read in all files in folder
    # parse for headers, contents (correct for trailing "the"... or make separate file that does that)
    # fill "files" box with .txt-less filenames. When selected, update label with short header info.
    # 1) Select file. Shows Y on left, N on right
    # 2) Merge files - just merge all files in multiple, show in alphabetical order, descending by "most hit" at top.
