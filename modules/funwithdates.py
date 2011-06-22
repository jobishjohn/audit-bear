#!/usr/bin/python
"""
-----Fun With Dates!-----
-Scope: This module is a collection of related functions that are hopfully useful in dealing with date anomalies and splitting up the main data structure based on Election-Day Voting, Pre-Voting Days, and Other days

-Usage: The "main" function serves as a usage example  You can import this module in any file you might want access to the functions.  It requies auditLog.py to have been imported.

    -Class DateMod:  Init this class with an AuditLog object and a path to the 68a file.
    This will duplicate the memory to store the AuditLog, but give you access to the variables below
    

    -Variable Names: These can all be accessed once an DateMod object is created.
        pdata: main data structure split into pre-election voting
        edata: events only from election day
        odata: events neither in the pre-voting or election voting

    -Functions: Commented out for the time being

-TO-DO: I'll update this as we figure out the easiest and most useful ways to share functions

-Note:
    -Currently Creating a DateMod instance will duplicate the data set and this might have to change in the future

------------------------
"""


class DateMod:

    #These Variables are dependant on a valid path and date parse from the 68a text file
    pdata = [] #AuditLog Object for all Pre-Voting
    edata = [] #AuditLog Object for all Election-Day Voting
    odata = [] #AuditLog Object for all days after election days and > 15 days before
    eday = ''  #Parsed Election Date from 68.lst file 
    pday = ''  #Election Day Minus 15
    
    def __init__(self, data, path):

        if not isinstance(data, auditLog.AuditLog):
            raise Exception('Must pass valid AuditLog object')

        if self.daygrab(path):
             self.splitDays(data, self.eday, self.pday)
        else:
            raise Exception('Must pass valid path with l68a file')
 
    """
    Gets date from l68a file or returns blank string. Its a little ugly, but it works for now
    TO-DO: Would be more robust with regex but still avoid reading entire file (Sammy!?)
    """
    def daygrab(self,path):
        try: f = open(path, 'r') 
        except: return False
        else:
            line = [f.next() for x in xrange(4)]
            try:
                self.eday = dateutil.parser.parse(' '.join(line[3].split()[0:3])).date()
            except ValueError:
                print 'Could not parse date from 168.lst'
                return False
            else:
                self.pday = self.eday - datetime.timedelta(15)
                return True 

    """
    Creates 3 AuditLog objects based on pdate and edate.
    """
    def splitDays(self, data, eday, pday):
        edata = []
        pdata = []
        odata = []
        daystring = str(eday.month).zfill(2) + '/' + str(eday.day).zfill(2) + '/' + str(eday.year)
    
        for line in data:
            if line.dateTime[0:10] == daystring:
                self.edata.append(line)
            else:
                try: 
                    temp = dateutil.parser.parse(line.dateTime[0:10]).date()
                except ValueError:
                    self.odata.append(line)
                else:
                    if temp < eday and temp >= pday: self.pdata.append(line)
                    else: self.odata.append(line)
                    
        return True

"""
---Main---
This only executes if you run this as a script.  This serves more as an example then anything else. All imports here are required for this module. Make sure you import this module into a file that already has these imports listed.
----------
"""
        
if __name__== "__main__":

    import auditLog
    import datetime
    import dateutil.parser

    path1 = "/home/patrick/documents/data/anderson_co_01_14_11_el152.txt"
    path2 = "/home/patrick/documents/data/anderson_co_03_07_11_el68a.txt"

    f = open(path1, 'r')
    data = auditLog.AuditLog(f)
    f.close()

    print data[0]

    dateclass = DateMod(data, path2)
    print dateclass.eday
    print dateclass.pday

    print 'Election Day:', dateclass.eday
    for x in xrange(10): print dateclass.edata[x] 
    print 'PreVoting Days:',dateclass.pday, '+'
    for x in xrange(10): print dateclass.pdata[x]
    print 'Other Dates:' 
    for x in xrange(10): print dateclass.odata[x]



"""
#Checks dates that are past the election date and clearly wrong
def daycheck(pdata, day):
    day = dateutil.parser.parse(day)
    flag = True
    # This dict uses the machine and date as a key in a tuple and the value is the # of lines
    d = {}

    for line in pdata:
        try:
            cday = dateutil.parser.parse(line[3])
        except ValueError:
            pass #pass here because we'll look at unparsible dates in another function
        else:
            if (dateutil.parser.parse(line[3]) - day) > datetime.timedelta(0):
                if (line[0], line[3]) in d:
                    d[(line[0],line[3])] += 1
                else:
                    d.update({(line[0],line[3]): 1})
                flag = False
    return (flag, d)

#Checks data for any events not in increaseing order by time stamp
def eventsinorder(data):
    events = []
    lastmachine = '0'
    for line in data:
        currenttime = ' '.join(line[3:5])
        if line[0] != lastmachine:
            lastmachine = line[0]
            lasttime = datetime.datetime.min
        try:
            eventtime = dateutil.parser.parse(currenttime)
        except ValueError:
            flag = False
            events.append(line)
        else:
            if (eventtime - lasttime) < datetime.timedelta(0):
                events.append(line)
            lasttime = dateutil.parser.parse(currenttime)

    return events

#Checks that each machine was opened and closed returns true for success
#Added a list that returns hours each machine was open for histogram purposes
def isclosed(data):
    temp = data[0][0]
    times = []
    ostate = 0 
    success = True
    for line in data:
        if line[0] != temp:
            if ostate == 0: 
                print temp, (end-start)
                times.append(end-start)
            else: 
                print 'Machine', temp, 'Not Closed' 
                success = False
            temp = line[0]
        if line[5] == '0001672': 
            ostate = 1
            start = dateutil.parser.parse(' '.join(line[3:5]))
        elif line[5] == '0001673':
            if ostate == 1:
                ostate  = 0
                end = dateutil.parser.parse(' '.join(line[3:5]))
            elif ostate == 0:
                #This applys when edata is passed and so far only occurs then
                print 'Machine', temp, 'Opened before Election Day without closing'

    return times

#Returns list of times of day in minutes for each opening
def datesopened(data): #histogram2
    minutes = [] 
    for line in data:
        if line[5] == '0001672':
            minutes.append(int(line[4][0:2])*60 + int(line[4][3:5]))
    return minutes
"""
