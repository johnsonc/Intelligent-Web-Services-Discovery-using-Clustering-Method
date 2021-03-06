import os
import nltk
import re
import time
import math
import pylab
import networkx
import string
from nltk.corpus import words as w
english_dictionary = w.words(fileids = 'en') # english dictionary from nltk




def findMessageTypes(filename): #finds the type of Messages exchanged by the service
 fl = open(filename,"r")
 i=0
 j=0
 typeName = ''
 typeNames = []
 x=''
 for line in fl:
  if re.search("[<]wsdl[\:]part[ ]*name[ ]*=[ ]*\"[_A-Z]*\"[ ]*type[ ]*=",line):
     #print line
     if re.search("name=",line):
        i=line.index("type=")
        i=i+6
        j=line.index(">")
        j=j-1
        typeName = line[i:j].strip("_")     
        typeNames = typeNames + [typeName]
        #name = line[i+1:len(line)-2]
        #x=name[0].strip("\"")
 return typeNames       





def findMessageNames(filename): #finds the name of Messages exchanged by the service
 fl = open(filename,"r")
 i=0
 j=0
 partName = ''
 partNames = []
 x=''
 for line in fl:
  if re.search("[<]wsdl[\:]part[ ]*name[ ]*=[ ]*\"[_A-Z]*\"[ ]*type[ ]*=",line):
     #print line
     if re.search("name=",line):
        i=line.index("name=")
        i=i+6
        j=line.index("type=")
        j=j-2
        partName = line[i:j].strip("_")     
        partNames = partNames + [ partName]
        #name = line[i+1:len(line)-2]
        #x=name[0].strip("\"")
 return partNames       



def replaceNumbers(name): #replaces numbers with their corresponding letter counterparts
 for i in range(0,9):
    if str(i) in name :
        if i == 0 :
           name = name.replace("0","zero")
        if i == 1 :
           name = name.replace("1","one")
        if i == 2 :
           name = name.replace("2","two")
        if i == 3 :
           name = name.replace("3","three")
        if i == 4 :
           name = name.replace("4","four")
        if i == 5 :
           name = name.replace("5","five")
        if i == 6 :
           name = name.replace("6","six")
        if i == 7 :
           name = name.replace("7","seven")
        if i == 8 :
           name = name.replace("8","eight")
        if i == 9 :
           name = name.replace("9","nine")
 return name   
 

def breakName(name): # breaks a name into induvidual components based on the english dictionary and camel case
 wordlist = []
 name= name.replace("-","")
 name = name.replace("_","")
 name = name.lower()
 name = replaceNumbers(name)
 start =  0
 wlen = 0
 end = 0
 k = len(name)
 temp = ''
 while k > 0:
  for i in range(start,len(name)+1):
   temp = name[start:i]
   #print temp
   if temp in english_dictionary:
    end = i
  temp = name[start:end]
  #print '\n\n'
  #print 'Word acquired : ', temp
  wlen = len(temp)
  k = k - wlen
  wordlist = wordlist + [temp]
  start = end
 k=0
 for i in range(len(wordlist)):
   if 'ing' in wordlist:
     k=wordlist.index('ing') 
     wordlist[k-1] = wordlist[k-1] + 'ing'
     wordlist.remove('ing')  
 return wordlist

def findName(filename): #finds the name of the web service by doing regular expression matching 
 fl = open(filename,"r")
 i=0
 name = ''
 x=''
 for line in fl:
  if re.search("name[ ]*=[ ]*\"[A-Za-z0-9]*\"[ \\n\\t]*targetNamespace",line):
     #print line
     if re.search("name=",line):
        name =  re.split("name=",line)[1]
        name = name.split(" ")
        #print name[0]     
        i=line.index("=")
        i=i+2 
        #name = line[i+1:len(line)-2]
        x=name[0].strip("\"")
        return x



def getTypes(filename): #gets a set of types used in the wsdl document
 fl = open(filename,"r")
 x=''
 start = 0
 end = 0
 type_sequence = []
 for line in fl:
   if re.search("type[ ]*=[ ]*\"xsd[\:]",line):
     #print line
     start = line.index("type=\"xsd:")+len("type=\"xsd:")
     end = line.index(">") - 1
     type_sequence = type_sequence +  [line[start:end].strip("\"")] 
     
   if re.search("base[ ]*=[ ]*\"xsd[\:]",line):
     #print line
     start = line.index("base=\"xsd:")+len("base=\"xsd:")
     end = line.index(">") - 2
     type_sequence = type_sequence +  [line[start:end].strip("\"")]  
 type_sequence=list(set(type_sequence))
 return type_sequence  


def iterate(): # iteraates through all the files present in the wsdl dataset and prints their details
 f=object()
 filename = ''
 counter = 0
 score = 0
 match = 0
 base_comparison = [] 
 types = [] 
 path = '/home/kaushik/Desktop/web services project/wsdl dataset'
 for fl in  os.listdir('/home/kaushik/Desktop/web services project/wsdl dataset'):
   filename = path+ "/" + fl
   counter = counter + 1 
   if re.search('str',str(type(findName(filename)))):
    print counter
    print breakName(findName(filename))
    print findMessageNames(filename)
    print findMessageTypes(filename)
    print getTypes(filename)
   



