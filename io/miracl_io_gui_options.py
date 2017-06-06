#! /usr/bin/env python
# Maged Goubran @ 2016, mgoubran@stanford.edu 

# coding: utf-8 

import argparse
import sys

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *


# Inputs #########

def helpmsg(name=None):
    return '''miracl_io_gui_options.py -t title -f fields [separated by space] -v [volumes to open] -hf helpfun

Takes list of strings as options for entries for a gui options, and a gui title

example: miracl_io_gui_options.py -t "Reg options" -v clar labels -f orient label resolution

Input options will be printed as output

'''

def parseargs():

    parser = argparse.ArgumentParser(description='Sample argparse py', usage=helpmsg())
    parser.add_argument('-t', '--title', type=str, help="gui title", required=True)
    parser.add_argument('-f', '--fields', type=str, nargs='+', help="fields for options")
    parser.add_argument('-v', '--vols', type=str, nargs='+', help="volumes for reading")
    parser.add_argument('-hf', '--helpfun', type=str, help="help fun")

    args = parser.parse_args()

    title = args.title
    fields = args.fields
    vols = args.vols
    helpfun = args.helpfun

    return title, vols, fields, helpfun


def OptsMenu(title, vols, fields, helpfun):
        
    # create GUI
    main = QtGui.QMainWindow()

    widget = QtGui.QWidget()
    widget.setWindowTitle('%s' % title)    

    layout = QFormLayout()
    layout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)

    linedits = {}
    buttons = {}
    labels = {}

    for v, vol in enumerate(vols):
        # Create buttons for vols
        labels["%s" % vol] = QtGui.QLabel('No file selected')
        buttons["%s" % vol] = QtGui.QPushButton('Select %s' % vol)

        # Layout for widgets        
        layout.addRow(labels["%s" % vol], buttons["%s" % vol])

        widget.connect(buttons["%s" % vol], QtCore.SIGNAL('clicked()'), lambda: get_fname(main, labels, vol))

    for f, field in enumerate(fields):

        # Create inputs (line edts)
        linedits["%s" % field] = QLineEdit()
        linedits["%s" % field].setAlignment(QtCore.Qt.AlignRight)

        # Layout for widgets        
        layout.addRow("%s" % field, linedits["%s" % field])

    # Create push button
    helpbutton = QtGui.QPushButton('Help')
    submit = QtGui.QPushButton('Submit')

    layout.addRow(helpbutton, submit)
    widget.setLayout(layout)

    widget.connect(submit, QtCore.SIGNAL('clicked()'), lambda: print_input(linedits, fields))
    widget.connect(helpbutton, QtCore.SIGNAL('clicked()'), lambda: print_help(main, helpfun))

    return widget


def get_fname(main, labels, vol):
    file = QtGui.QFileDialog.getOpenFileName(main, 'Select %s' % vol)
    if file:
        filestr = "%s:" % vol + file
        labels["%s" % vol].setText(filestr)
        print '%s path:' % vol, file
    else:
        labels["%s" % vol].setText('No file selected')


def print_input(linedits, fields):
    for f, field in enumerate(fields):
        print "%s :" % field, linedits["%s" % field].text()

def print_help(main, helpfun):
    helpwidget = QtGui.QDialog()
    main.setCentralWidget(helpwidget)
    helpwidget.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    main.setWindowTitle('Help function')    

    helplayout = QVBoxLayout()
    helplbl = QtGui.QLabel(helpfun)
    helplayout.addWidget(helplbl)

    helpwidget.setLayout(helplayout)

    main.show()

    QApplication.processEvents()

def main():
    [title, vols, fields, helpfun] = parseargs()

    # Create an PyQT4 application object.
    app = QApplication(sys.argv)
    menu = OptsMenu(title, vols, fields, helpfun)
    menu.show()
    app.exec_()
    app.processEvents()

if __name__ == "__main__":
    sys.exit(main())
