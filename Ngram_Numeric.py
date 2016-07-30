import collections

stringTonumericDict = {}
numericToStringDict = {}
class NumConver:


    def __init__(self,SortedSentece):

         for s,i in zip(SortedSentece,range(1,len(SortedSentece)+1)):
            numericToStringDict[i] = s
            stringTonumericDict[s] = i

    def getNumericFromString(self,val):
        return stringTonumericDict[val]

    def getStringFromNumeric(self,val):
        return numericToStringDict[val]
