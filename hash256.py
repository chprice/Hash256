#Channon Price
#IDS Assignment 3
#2/15/10
#Program to compute sha256 hashes of files in a specified directory.

#NOTE: Currently only set up to handle windows OS. Minor changes and testing needed to change file handling to work with unix.

#Has four main functions.
#makeHash computes the sha256 hash of a file
#getFileNames generates a list of all file names within a given directory and their hashes
#openFile opens a precomputed list of filenames and hashes
#writeFile writes a list of filenames and hashes

#Call writeFile(getFileNames()) to write a file with the hashes for a directory.

#The program currently compares an inputted hashfile to an inputted directory tree and returns any discrepancies.

import hashlib
import os

#os.environ["OS"] #to set the linux vs windows flags

#BEGIN FUNCTIONS ----------------------------------------------------

def makeHash(fileName): #given a filename and path, computes hash of file
    tHash = hashlib.sha256()
    somefile = open(fileName, 'rb')
    tempString = somefile.readline()
    while(len(tempString)!=0):
        tHash.update(tempString)
        tempString = somefile.readline()

    return tHash.hexdigest()

def getFileNames(directory): #returns a list containing all of the files within the directory and subdirectories and their hashes
    masterReturn = []
    folderNames = []
    listFiles = os.listdir(directory)
    for i in listFiles:
        if("." not in i):
            folderNames.append(i) #get the names of all folders
        else:
            masterReturn.append([i.replace(" ",""), makeHash(directory + "\\" + i) ]) #appends a two element list containing the folder and it's hash
                                                                                        #this can be a bit slow =/

    if(len(folderNames) == 0): #if I have no more subfolders
        return masterReturn
    for folder in folderNames:
        hold = getFileNames(directory + "\\" + folder) #the \\ again is only for windows. Unix needs / instead.
        for file in hold:
            masterReturn.append(file)

    return masterReturn


def openFile(nameFile): #returns a list containing the filenames and hashes pulled from the file
	somefile = open(nameFile, 'r')
	temp = somefile.readline()
	fileArray=[]
	while(len(temp)!=0):
		fileArray.append( (temp.rstrip('\n')).split(" ")  )
		temp = somefile.readline()
	somefile.close()
	return fileArray

def writeFile(nameFile, hashList): #takes a path and filename, and hashList to write
    somefile = open(nameFile, 'w')
    for line in hashList:
        somefile.write(line[0]+" "+line[1]+"\n")
    somefile.close()
    




    
# BEGIN ACTUAL MAIN ------------------------------------------------------



nameDirectory = input("Directory name and path? \n")
nameFile = input("And now give me the path and filename containing the SHA-256 hash values. \n")

#nameDirectory needs to have all \ turned into \\ on windows systems, but fine on unix
CurrentFiles = getFileNames(nameDirectory)
PastFiles = openFile(nameFile)

#at this point in the code, I have two arrays:
    #CurrentFiles is an array containing the names of all of the files within the specified directory and their hashes
    #PastFiles is an array containing the names and the hashes of the files that were computed before.

CurrentFiles.sort()
PastFiles.sort()

CurrentFilesCopy = []
CurrentFilesCopy.extend(CurrentFiles)
PastFilesCopy = []
PastFilesCopy.extend(PastFiles)
#They are both now in alphabetical order

for curFile in CurrentFiles:
    for oldFile in PastFiles:
        if(curFile[0] == oldFile[0]):#file name match
            if(curFile[1] == oldFile[1]):#hash name match
                PastFilesCopy.remove(oldFile)
                CurrentFilesCopy.remove(curFile)
            else:
                print("The file "+ curFile[1]+" has had it's hash changed from "+oldFile[1]+" to "+curFile[1])                
                
if((len(CurrentFilesCopy)==0) and (len(PastFilesCopy)==0)):
    print("There are no new files, and no files removed. All hashes are as before.")

#Any files left in CurrentFilesCopy have been added since the hashfile was last computed
#Any files left in PastFilesCopy are files that are no longer present

for file in CurrentFilesCopy:
    print("The file "+file[0]+" was added since the hash file was last computed.")
for file in PastFilesCopy:
    print("The file "+file[0]+" is no longer in the directory.")

