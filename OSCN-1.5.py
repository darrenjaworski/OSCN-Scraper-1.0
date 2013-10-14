#!/usr/bin/env python

import scraperwiki
import lxml.html           

counter = 1 

casetype = 'cf'
county = 'Tulsa'
year = 2013

print 'Beginning with ' + str(county) + ' County ' + str(year)

while counter < 10: #set to 3400 
    
    html = scraperwiki.scrape("http://www.oscn.net/applications/oscn/GetCaseInformation.asp?number=" + str(casetype) + "-" + str(year) + "-" + str(counter) + "&db=" + str(county) + "&submitted=true")
    root = lxml.html.fromstring(html)
    
    for tr in root.cssselect("center table"):
    	tabledata = tr.cssselect("td")
        
        leftcenter = tabledata[0].text_content().strip().replace(u'\xa0','')
        rightcenter = tabledata[1].text_content().strip().replace('\r','').replace('\n','').replace('\t','').replace(u'\xa0','').replace(' ','')
        
    for table in root.cssselect("html"):
		tabledata = table.cssselect("table")[4]
	
		countstable = tabledata.text_content().strip().replace('\r','').replace('\n','').replace('\t','').replace(u'\xa0','').replace('  ','')
        
	#parsing the relevant text to clean it up
	#defendant
    defstart = leftcenter.rfind('v.')
    defend = leftcenter.rfind('Defendant.') - len(leftcenter)
    defendant = str(leftcenter[defstart + 2: defend - 1])
	
	#judge
    judgestart = rightcenter.rfind('Judge:')
    judge = str(rightcenter[judgestart + 6:])
	
	#plaintiff
    plaintiffstart = leftcenter.rfind(',Plaintiff')
    plaintiff = str(leftcenter[:plaintiffstart])
	
	#filed
    filedstart = rightcenter.rfind('Filed:')
    filed = str(rightcenter[filedstart+6:filedstart+16])
	
	#closed - will need to figure out a way to stop this if there is not a closed date
    closedstart = rightcenter.rfind('Closed:')
    closed = str(rightcenter[closedstart+7:closedstart+17])
	
	#counts are in reverse order because 
    countonestart = countstable.rfind('Count as Filed: ')
    countoneend = countstable.rfind('Date Of Offense:') - len(countstable)
    countone = str(countstable[countonestart + 16:countoneend])
    
    counttwostart = countstable.rfind('Count as Filed: ', 0, countonestart)
    counttwoend = countstable.rfind('Date Of Offense', 0, countonestart) - len(countstable)
    counttwo = str(countstable[counttwostart + 16:counttwoend])
    
    countthreestart = countstable.rfind('Count as Filed: ', 0, counttwostart)
    countthreeend = countstable.rfind('Date Of Offense', 0, counttwostart) - len(countstable)
    countthree = str(countstable[countthreestart + 16:countthreeend])
	
	#disposition
    dispositionindex = countstable.rfind('Disposed:')
    dispositionindextwo = countstable.rfind('Disposed',0,dispositionindex)
    dispositionindexthree = countstable.rfind('Disposed',0,dispositionindextwo)
    dispositionindexfour = countstable.rfind('disposed',0,dispositionindexthree)
    dispositionindexfive = countstable.rfind('Disposed',0,dispositionindexfour)
    
    dispositiononestart = countstable.rfind('Disposed:',0,dispositionindex)
    dispositiononeend = countstable.rfind('Count as Disposed') - len(countstable)
    dispositionone = str(countstable[dispositiononestart + 9:dispositiononeend])
    
    dispositiontwostart = countstable.rfind('Disposed:',0,dispositionindexthree)
    dispositiontwoend = countstable.rfind('Count as Disposed',0,dispositiononestart) - len(countstable)
    dispositiontwo = str(countstable[dispositiontwostart + 9:dispositiontwoend])
    
    dispositionthreestart = countstable.rfind('Disposed:',0,dispositionindexfive)
    dispositionthreeend = countstable.rfind('Count as Disposed',0,dispositiontwostart) - len(countstable)
    dispositionthree = str(countstable[dispositionthreestart + 9:dispositionthreeend])
	
	#date of offenses
	#there is a bug here somewhere
    offensestart1 = countstable.rfind('Date Of Offense: ') + 17
    dateofoffense1 = str(countstable[offensestart1:offensestart1+10])
    
    offensestart2 = countstable.rfind('Date Of Offense: ', 0, offensestart1) + 1
    dateofoffense2 = str(countstable[offensestart2:offensestart2+10])
    
    offensestart3 = countstable.rfind('Date Of Offense: ', 0, offensestart2) + 17
    dateofoffense3 = str(countstable[offensestart2:offensestart2+10])
	
    data = {     
		'OSCN hyperlink' : "http://www.oscn.net/applications/oscn/GetCaseInformation.asp?number=" + str(casetype) + "-" + str(year) + "-" + str(counter) + "&db=" + str(county) + "&submitted=true",
		'unique case number' : str(county) + " cf-" + str(year) + "-" + str(counter),
		'case number' : "cf-" + str(year) + "-" + str(counter),
		'county' : str(county),
		'year' : str(year),
		'plaintiff' : plaintiff,
		'defendant' : defendant,
	#        'defstart' : defstart,
	#        'defend' : defend,
	#        'judgestart' : judgestart,
		'judge' : judge,
		'filed' : filed,
		'closed' : closed,
	#        'counts' : countstable,
	#        'counts' : str(counts),
		'count 1' : countone,
		'count 1 - date of offense' : dateofoffense1,
		'count 2' : counttwo,
		'count 2 - date of offense' : dateofoffense2,
		'count 3' : countthree,
		'count 3 - date of offense' : dateofoffense3,
	#        'count3' : countsthree,
		'disposition count 1' : dispositionone,
		'disposition count 2': dispositiontwo,
		'disposition count 3': dispositionthree,
		}

    print data
    scraperwiki.sqlite.save(unique_keys=['unique case number'], data=data)
    counter +=1
