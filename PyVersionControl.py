#Used to create the GUI
import tkinter as tk
from tkinter import messagebox
from tkinter import *
import sys

#Used to handle files
import glob 
import os
from pathlib import Path
import shutil
from shutil import *
import webbrowser as wb

#Used for the log to insert date/time
import time

nameArray = []
dirPath = ''

#Generates folders + standard documents

class sourceControl():

    def __init__(self, root):
        #Labels
        sourceLabel = Label(root, text='Source Folder')
        sourceLabel.grid(row=1, column=0, sticky=W)

        workingLabel = Label(root, text='Working Folder')
        workingLabel.grid(row=1, column=1, sticky=W, padx=(50,0))

        logLabel = Label(root, text='Activity Log')
        logLabel.grid(row=4, column=0, sticky=W, pady=(10,0))

        nameLabel = Label(root, text='Please enter folder name:')
        nameLabel.grid(row=0,column=0, sticky=W)

        logLabel2 = Label(root, text='Change Log')
        logLabel2.grid(row=4, column=5, sticky=W, pady=(10,0), padx=(8,0))

        #Entry boxes
        nameEntry = Entry(root)
        nameEntry.grid(row=0, column=0, sticky=E)

        #List boxes
        workingList = Listbox(root, height=10, width=50, exportselection=FALSE)
        workingList.grid(row=2, column=1, padx=(50,0))

        sourceList = Listbox(root, height=10, width=50, exportselection=FALSE)
        sourceList.grid(row=2, column=0)

        #Log text box
        textLog = Text(root, height= 10, width= 80, wrap="word")
        textLog.grid(row=5, column=0, columnspan=2)

        logScroll = Scrollbar(root, command=textLog.yview)
        textLog.config(yscrollcommand=logScroll.set)
        logScroll.grid(row=5, column=1, sticky='nse', padx=(0))

        #Changes text box
        changeLog = Text(root, height=10, width=65, wrap="word")
        changeLog.grid(row=5, column=5, columnspan=4)

        changeScroll = Scrollbar(root, command=changeLog.yview)
        changeLog.config(yscrollcommand=changeScroll.set)
        changeScroll.grid(row=5, column=8, sticky='nse')

        #Options for buttons
        button_opt = {'fill': constants.BOTH, 'padx': 5, 'pady': 5}

        #Define buttons
        genFileBut = Button(root, text= 'Generate \nfile structure', width=15, height=2, fg = 'black', command= lambda: genFolders())
        genFileBut.grid(row=2, column=5, padx=20, sticky=N)

        copyFileBut = Button(root, text= 'Copy \n Files working folder', width=15, height=2, fg= 'black', command= lambda: copySelectedFolder())
        copyFileBut.grid(row=2, column=6, padx=10, sticky=N)

        revertBut = Button(root, text= 'Move folders\n to Source folder', width= 15, height= 2, fg= 'black', command= lambda: revertChanges())
        revertBut.grid(row= 2, column= 5, padx= 10, sticky=S)

        showLogBut = Button(root, text= 'Show \n changelog', width = 15, height = 2, fg= 'black', command=lambda: showLog())
        showLogBut.grid(row= 2, column= 6, padx= 10, sticky=S)

        createReleaseBut = Button(root, text= 'Create\n release pack', width = 15, height = 2, fg= 'black', command=lambda: compressFile())
        createReleaseBut.grid(row= 2, column= 7, padx= 10, sticky=S)

        helpBut = Button(root, text='Help', width= 15, height= 2, fg= 'black', command= lambda: showHelp())
        helpBut.grid(row= 2, column= 7, padx= 10, sticky=N)

        checkDateBut = Button(root, text='Check changes', width=15, height=2, fg='black', command= lambda: checkChanges())
        checkDateBut.grid(row=2, column=8, padx=10, sticky=N)

        nameBut = Button(root, text='Enter folder name', width=15, fg='black', command= lambda: nameFolderStructure())
        nameBut.grid(row=0, column=1, sticky=W, padx=(40,0))
        #End of button creation

        #Functions
        def nameFolderStructure():
            workingName = nameEntry.get() #Get user input for folder name
            global nameArray 
            nameArray.append(dirPath+'\\source') #Adds source folder location to storage variable
            nameArray.append(dirPath+'\\'+workingName) #Adds working folder location to storage variable
            folderLocs = ",".join(nameArray) #Joins items inside array into one string to be written to text file for storage
            fileLoc = open(dirPath+'\\FolderLocations.txt','r+')
            fileLoc.seek(0)
            fileLoc.write(folderLocs)
            fileLoc.truncate()
            fileLoc.close()
            genFolders()

        def showLog():
            wb.open(dirPath+'\\log.txt') #Opens Log file in notepad

        def showHelp():
            wb.open(dirPath+'\\help.txt') #Opens Help file in notepad


        def genFolders():
            #Generates pre-determined folder structure
            path=nameArray[1] #Dislike hard-coded value, needs changed. 
            foldersGenerated = False #Bool used to check if creation was successful
            if (os.path.isdir(path)): #Checks if toplevel folder exists, creates it if not
                tk.messagebox.showwarning('Error','File: %s' % path + ' already exists')
            else:
                os.mkdir(path)
                foldersGenerated = True
            #checks if required subfolders exist, creates them if not
            if (os.path.isdir(path+'/test')):
                tk.messagebox.showwarning('Error','File: %s' % path + '\\test already exists')
            else:
                os.mkdir(path+'/test')
                foldersGenerated = True

            if (os.path.isdir(path+'/code')):
                tk.messagebox.showwarning('Error','File: %s' % path + '\code already exists')
            else:
                os.mkdir(path+'/code')
                foldersGenerated = True
                
            if (os.path.isdir(path+'/docs')):
                tk.messagebox.showwarning('Error','File: %s' % path + '\docs already exists')
            else:
                os.mkdir(path+'/docs')
                foldersGenerated = True

            #Output to log text box and log file
            log = open(dirPath+'\\log.txt','w+')
            if foldersGenerated == True:
                textLog.insert(END, 'Folder structure generated at: ' + time.strftime("%H:%M") + ' - ' + time.strftime("%d/%m/%Y") + '\n')
                log.write('Folder structure generated at: ' + time.strftime("%H:%M") + ' - ' + time.strftime("%d/%m/%Y") + '\n')
            else:
                textLog.insert(END, 'Attempt at generating folder structure at: ' + time.strftime("%H:%M") + ' - ' + time.strftime("%d/%m/%Y") + '. Failed as structure already exists.\n')
                log.write('Attempt at generating folder structure at: ' + time.strftime("%H:%M") + ' - ' + time.strftime("%d/%m/%Y") + '. Failed as structure already exists.\n')
            log.close()
            for i in nameArray:
                writeFolderLists(i)
                
        #Writes folders to lsitboxes
        def writeFolderLists(parentFolder):
            fileList = []
            for dirname, dirnames, filenames in os.walk(parentFolder):
                #Stores files in array
                    for i in glob.glob(dirname):
                        identLevel = i.count('\\')-1
                        ident = '   ' * identLevel
                        fileList.append(ident+i)
                    for i in filenames:
                        p = os.path.join(dirname, i)
                        ident = '   ' * (identLevel+1)
                        fileList.append(ident+p)

            #Writes array of files to list.
            if 'source' in parentFolder:
                sourceList.delete(0, END)
                for item in fileList:
                    sourceList.insert(END, item)
                    fileList = []

            else: 
                workingList.delete(0, END)
                for item in fileList:
                    workingList.insert(END, item)
                    fileList = []

        #Gets selected items from folder display lists
        def getSelections():
            try:
                selectedSource = str(sourceList.get(sourceList.curselection()[0])).lstrip() #checks file is selected
                selectedWork = str(workingList.get(workingList.curselection()[0])).lstrip() #before trying to copy it
            except IndexError:
                tk.messagebox.showwarning('Oops', 'Please select a folder or file')
                    #TODO: add in logic to tell user if working or source file needs selected(IF statement?)
            else:
                return selectedSource, selectedWork
            

        #Copy selected item from Source to selected Working location
        def copySelectedFolder():
            selectedSource, selectedWork = getSelections()
            if os.path.isdir(selectedSource) is True: #checks if selected source location is a folder
                tk.messagebox.showinfo('Source folder selected!','You have selected a folder to be copied over to the working directory. Please select a file instead.')
                return
            if os.path.isdir(selectedWork) is False: #checks if selected working location is a file
                answer = tk.messagebox.askyesno('Working file selected!','You have selected a file to be copied to in the working directory. Do you wish to overwrite the file?')
                if answer is False:
                    return
                else:
                    shutil.copy2(selectedSource, selectedWork)
                    log = open(dirPath+'\\log.txt','w')
                    textLog.insert(END, selectedSource + ' copied to ' + selectedWork + ' at: '+ time.strftime("%H:%M") + ' - ' + time.strftime("%d/%m/%Y") + '\n')
                    log.write(selectedSource + " copied to " + selectedWork + " at: " + time.strftime("%H:%M") + " - " + time.strftime("%d/%m/%Y") + "\n")
                    log.close()
                    for i in nameArray:
                        writeFolderLists(i)
                        #rewrites updated file list display
            else:
                shutil.copy2(selectedSource, selectedWork)
                log = open(dirPath+'\\log.txt','w')
                textLog.insert(END, selectedSource + ' copied to ' + selectedWork + ' at: '+ time.strftime("%H:%M") + ' - ' + time.strftime("%d/%m/%Y") + '\n')
                log.write(selectedSource + " copied to " + selectedWork + " at: " + time.strftime("%H:%M") + " - " + time.strftime("%d/%m/%Y") + "\n")
                log.close()
                for i in nameArray:
                    writeFolderLists(i)
                    #rewrites updated file list display

        def checkChanges():
            selectedSource, selectedWork = getSelections()
            if os.path.isdir(selectedSource) is True:
                tk.messagebox.showinfo('Folder selected!','You have selected a folder to be checked for changes. Please select a file instead.')
                return
            else:
                sourceDate = time.ctime(os.path.getmtime(selectedSource))
                workingDate = time.ctime(os.path.getmtime(selectedWork))
                changeLog.insert(END, selectedSource+" was last modified at: "+sourceDate+". "+selectedWork+" was last modified at "+workingDate+".\n")
                if sourceDate < workingDate:
                    changeLog.insert(END, selectedWork+" has been altered since it was copied.")
                else:
                    changeLog.insert(END, selectedWork+" has not been altered since it was copied.")

        def revertChanges():
            selectedSource, selectedWork = getSelections()
            if os.path.isdir(selectedSource) is True or os.path.isdir(selectedWork) is True:
                tk.messagebox.showinfo('Folder selected!','You have selected a folder to be copied over from the working directory. Please select a file instead.')
                return
            else:
                sourceDate = time.ctime(os.path.getmtime(selectedSource))
                workingDate = time.ctime(os.path.getmtime(selectedWork))
                if os.path.basename(selectedSource) != os.path.basename(selectedWork):
                    answer = tk.messagebox.askyesno('File Transfer','The source file you are replacing does not have the same name as the working file. Do you still wish to replace it?')
                    if answer is True:
                        shutil.copy2(selectedWork, selectedSource)
                    else:
                        tk.messagebox.showinfo('Transfer aborted.')
                        return
                if sourceDate < workingDate:
                    answer = tk.messagebox.askyesno('File Transfer','The source file you are replacing will be overwritten. Do you still wish to replace it?')
                    if answer is True:
                        shutil.copy2(selectedWork, selectedSource)
                    else:
                        tk.messagebox.showinfo('Transfer aborted.')
                        return
                elif sourceDate > workingDate:
                    answer = tk.messagebox.askyesno('File Transfer','The source file you are replacing is newer than the working file. Do you still wish to replace it?')
                    if answer is True:
                        shutil.copy2(selectedWork, selectedSource)
                    else:
                        tk.messagebox.showinfo('Transfer aborted.')
                        return
                else:
                    answer = tk.messagebox.askyesno('File Transfer','The source file you are replacing is the same age as the working file. Do you still wish to replace it?')
                    if answer is True:
                        shutil.copy2(selectedWork, selectedSource)
                    else:
                        tk.messagebox.showinfo('Transfer aborted.')
                        return
                
                    return
        
        def compressFile():
            zippedFileName = nameArray[1] + ' - ' + time.strftime("%d - %m - %Y")
            shutil.make_archive(zippedFileName, 'zip', nameArray[1])
            
                    
        global dirPath
        dirPath = os.getcwd()
        
root = Tk()
root.title('Source Control!')
root.geometry('{}x{}'.format(1230,410))
sourceControl(root)
root.mainloop()
