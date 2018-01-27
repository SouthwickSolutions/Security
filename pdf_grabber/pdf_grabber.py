'''in order to get the links from index-of.es, you have to create a session (cookie)
for the server to be happy, otherwise you will get an infinite 302 redirect loop.
that is the Session() method. It's important to note you have to install requests
and lxml via pip for this program to work. The program sleeps between 1 and 9 seconds
to prevent an unintentional DOS attack'''

'''this is not the original. I had to iterate through the list from the middle. take
care to delete [:1317] from line 92'''
import requests
from lxml import html
from collections import OrderedDict
import time
import os
import itertools
import random

level1_link_list           = [] #level1 hyperlink list
level2_link_list           = [] #unsorted level2 list
level3_link_list           = [] #unsorted level3 list
level4_link_list           = [] #unsorted level4 list
level5_link_list           = [] #unsorted level5 list
level6_link_list           = [] #unsorted level6 list
level7_link_list           = [] #unsorted level7 list
level8_link_list           = [] #unsorted level8 list
level9_link_list           = [] #unsorted level9 list
level10_link_list          = [] #unsorted level10 list
level1_relative_link_list  = []
level2_relative_link_list  = []
level3_relative_link_list  = []
level4_relative_link_list  = []
level5_relative_link_list  = []
level6_relative_link_list  = []
level7_relative_link_list  = []
level8_relative_link_list  = []
level9_relative_link_list  = []
level10_relative_link_list = []

master_pdf_list           = []
master_program_list       = []

master_list               = [] #unsorted master list
hyperlink_list            = []



def filter_links(list_to_filter):
    #the following uses list comprehension to filter out unwanted links. The fourth
    #line cuts out duplicates
    
    list_to_filter = [ x for x in list_to_filter if "?" not in x ]
    list_to_filter = [ x for x in list_to_filter if "http://" not in x ]
    list_to_filter = [ x for x in list_to_filter if ".php" not in x ]
    list_to_filter = list(OrderedDict.fromkeys(list_to_filter))

    return list_to_filter



def sorter():
    #this function sorts the master list into separate lists of pdfs and programs

    global master_list, master_pdf_list, master_program_list

    for i in master_list:
        if i[-3:] == 'pdf': master_pdf_list.append(i)
        else: master_program_list.append(i)


        
def director(pdf_link):
    #this function determines where the downloaded files go

    global level1_relative_link_list

    for i in level1_relative_link_list:
        if i in pdf_link:
            i = i[:-1]
            return i



def grabber():
    #this function downloads the pdfs and programs into the appropriate folder

    global level1_relative_link_list, master_pdf_list, master_program_list

    pdf_list_length = range(len(master_pdf_list))
    program_list_length = range(len(master_program_list))
    times = []

    #downloads the pdfs
    for pdf, length in itertools.izip(master_pdf_list[4581:], pdf_list_length[4581:]):
        rand_int = random.randint(1,9)
        start = time.time()

        open_session = requests.Session()
        open_session.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
        page = open_session.get(pdf, stream=True)

        #creates the name for the pdf
        last_slash = pdf.rfind('/')
        name = pdf[last_slash+1:]
        name = name.replace('%20', ' ')

        #finds which level1 category to put file in
        location = director(pdf)

        #downloads file
        with open('./index-of/' + location + '/pdfs/' + name, 'wb') as f:
            for chunk in page.iter_content(32000):
                f.write(chunk)

        finish = time.time()

        times.append(finish-start)
        
        time.sleep(rand_int)
        times.append(rand_int)
        average = sum(times)/len(times)
        print str(length+1) + " out of " + str(len(pdf_list_length)) + " pdfs are done downloading."
        print "Time: " + str(finish-start) + " seconds."
        print "Total time so far: " + str(sum(times)/60) + " minutes."
        print "slept for " + str(rand_int) + " seconds"
        print "Average: " + str(average) + " seconds."
        print "\n"

    times = []
    
    #downloads the programs
    for program, length in itertools.izip(master_program_list[:], program_list_length[:]):
        rand_int = random.randint(1,9)
        start = time.time()

        open_session = requests.Session()
        open_session.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
        page = open_session.get(program, stream=True)

        #creates the name for the pdf
        last_slash = program.rfind('/')
        name = program[last_slash+1:]
        name = name.replace('%20', ' ')

        #finds which level1 category to put file in
        location = director(program)

        #downloads file
        with open('./index-of/' + location + '/programs/' + name, 'wb') as f:
            for chunk in page.iter_content(32000):
                f.write(chunk)

        finish = time.time()

        times.append(finish-start)
        
        time.sleep(rand_int)
        times.append(rand_int)
        average = sum(times)/len(times)
        print str(length+1) + " out of " + str(len(program_list_length)) + " programs are done downloading."
        print "Time: " + str(finish-start) + " seconds."
        print "Total time so far: " + str(sum(times)/60) + " minutes."
        print "slept for " + str(rand_int) + " seconds"
        print "Average: " + str(average) + " seconds."
        print "\n"

        
def level1():
    #this function grabs the links off of the home page

    global level1_relative_link_list, level1_link_list
    
    #gets index-of.es ready for parsing
    open_session = requests.Session()
    open_session.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
    page = open_session.get('http://index-of.co.uk/')
    tree = html.fromstring(page.content)

    #grabs all of the links from index-of.es
    for link in tree.xpath('//a/@href'):
        level1_relative_link_list.append(link)

    #filters the links
    level1_relative_link_list = filter_links(level1_relative_link_list)

    #creates the level1 list
    for relative_link in level1_relative_link_list:
        level1_link_list.append('http://index-of.co.uk/' + relative_link)

    #creates level1 directories
    for i in level1_relative_link_list:
        i = i[:-1]
        os.makedirs('./index-of/' + i)
        os.makedirs('./index-of/' + i + '/pdfs')
        os.makedirs('./index-of/' + i + '/programs')

    time.sleep(1)



def level2():
#this function grabs the links from level 1 and sorts them

    global level1_link_list, level2_link_list, level2_relative_link_list, master_list, hyperlink_list
    
    for i in level1_link_list:
        #gets i ready for parsing
        open_session = requests.Session()
        open_session.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
        page = open_session.get(i)
        tree = html.fromstring(page.content)

        #grabs all of the links from i
        for link in tree.xpath('//a/@href'):
            level2_relative_link_list.append(link)

        #filters the links
        level2_relative_link_list = filter_links(level2_relative_link_list)

        #creates the level2 list
        for relative_link in level2_relative_link_list:
            level2_link_list.append(i + relative_link)
        
        level2_relative_link_list = []

    #does some basic sorting
    for i in level2_link_list:
        if i[-2:] == '//': continue
        elif i[-1] == '/': hyperlink_list.append(i)
        else: master_list.append(i)

    time.sleep(2)


    
def level3():
#this function grabs the links from level 2 and sorts them

    global level3_link_list, level3_relative_link_list, master_list, hyperlink_list
    
    for i in hyperlink_list:
        #gets i ready for parsing
        open_session = requests.Session()
        open_session.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
        page = open_session.get(i)
        tree = html.fromstring(page.content)

        #grabs all of the links from i
        for link in tree.xpath('//a/@href'):
            level3_relative_link_list.append(link)

        #filters the links
        level3_relative_link_list = filter_links(level3_relative_link_list)

        #cuts out leading /
        for j in range(len(level3_relative_link_list)):
            if level3_relative_link_list[j][0] == '/': level3_relative_link_list[j] = level3_relative_link_list[j][1:]
        
        #creates the level3 list
        for relative_link in level3_relative_link_list:
            if relative_link not in i: level3_link_list.append(i + relative_link)

        level3_relative_link_list = []
    
    hyperlink_list = []
    
    #does some basic sorting
    for i in level3_link_list:
        if i[-2:] == '//': continue
        elif i[-1] == '/': hyperlink_list.append(i)
        else: master_list.append(i)

    time.sleep(3)



def level4():
#this function grabs the links from level 3 and sorts them

    global level4_link_list, level4_relative_link_list, master_list, hyperlink_list
    
    for i in hyperlink_list:
        #gets i ready for parsing
        open_session = requests.Session()
        open_session.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
        page = open_session.get(i)
        tree = html.fromstring(page.content)

        #grabs all of the links from i
        for link in tree.xpath('//a/@href'):
            level4_relative_link_list.append(link)

        #filters the links
        level4_relative_link_list = filter_links(level4_relative_link_list)

        #cuts out leading /
        for j in range(len(level4_relative_link_list)):
            if level4_relative_link_list[j][0] == '/': level4_relative_link_list[j] = level4_relative_link_list[j][1:]
        
        #creates the level4 list
        for relative_link in level4_relative_link_list:
            if relative_link not in i: level4_link_list.append(i + relative_link)

        level4_relative_link_list = []
    
    hyperlink_list = []
    
    #does some basic sorting
    for i in level4_link_list:
        if i[-2:] == '//': continue
        elif i[-1] == '/': hyperlink_list.append(i)
        else: master_list.append(i)

    time.sleep(4)



def level5():
#this function grabs the links from level 4 and sorts them

    global level5_link_list, level5_relative_link_list, master_list, hyperlink_list
    
    for i in hyperlink_list:
        #gets i ready for parsing
        open_session = requests.Session()
        open_session.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
        page = open_session.get(i)
        tree = html.fromstring(page.content)

        #grabs all of the links from i
        for link in tree.xpath('//a/@href'):
            level5_relative_link_list.append(link)

        #filters the links
        level5_relative_link_list = filter_links(level5_relative_link_list)

        #cuts out leading /
        for j in range(len(level5_relative_link_list)):
            if level5_relative_link_list[j][0] == '/': level5_relative_link_list[j] = level5_relative_link_list[j][1:]
        
        #creates the level5 list
        for relative_link in level5_relative_link_list:
            if relative_link not in i: level5_link_list.append(i + relative_link)

        level5_relative_link_list = []
    
    hyperlink_list = []
    
    #does some basic sorting
    for i in level5_link_list:
        if i[-2:] == '//': continue
        elif i[-1] == '/': hyperlink_list.append(i)
        else: master_list.append(i)

    time.sleep(5)



def level6():
#this function grabs the links from level 5 and sorts them

    global level6_link_list, level6_relative_link_list, master_list, hyperlink_list
    
    for i in hyperlink_list:
        #gets i ready for parsing
        open_session = requests.Session()
        open_session.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
        page = open_session.get(i)
        tree = html.fromstring(page.content)

        #grabs all of the links from i
        for link in tree.xpath('//a/@href'):
            level6_relative_link_list.append(link)

        #filters the links
        level6_relative_link_list = filter_links(level6_relative_link_list)

        #cuts out leading /
        for j in range(len(level6_relative_link_list)):
            if level6_relative_link_list[j][0] == '/': level6_relative_link_list[j] = level6_relative_link_list[j][1:]
        
        #creates the level6 list
        for relative_link in level6_relative_link_list:
            if relative_link not in i: level6_link_list.append(i + relative_link)

        level6_relative_link_list = []
    
    hyperlink_list = []
    
    #does some basic sorting
    for i in level6_link_list:
        if i[-2:] == '//': continue
        elif i[-1] == '/': hyperlink_list.append(i)
        else: master_list.append(i)

    time.sleep(6)



def level7():
#this function grabs the links from level 6 and sorts them

    global level7_link_list, level7_relative_link_list, master_list, hyperlink_list
    
    for i in hyperlink_list:
        #gets i ready for parsing
        open_session = requests.Session()
        open_session.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
        page = open_session.get(i)
        tree = html.fromstring(page.content)

        #grabs all of the links from i
        for link in tree.xpath('//a/@href'):
            level7_relative_link_list.append(link)

        #filters the links
        level7_relative_link_list = filter_links(level7_relative_link_list)

        #cuts out leading /
        for j in range(len(level7_relative_link_list)):
            if level7_relative_link_list[j][0] == '/': level7_relative_link_list[j] = level7_relative_link_list[j][1:]
        
        #creates the level7 list
        for relative_link in level7_relative_link_list:
            if relative_link not in i: level7_link_list.append(i + relative_link)

        level7_relative_link_list = []
    
    hyperlink_list = []
    
    #does some basic sorting
    for i in level7_link_list:
        if i[-2:] == '//': continue
        elif i[-1] == '/': hyperlink_list.append(i)
        else: master_list.append(i)

    time.sleep(7)



def level8():
#this function grabs the links from level 7 and sorts them

    global level8_link_list, level8_relative_link_list, master_list, hyperlink_list
    
    for i in hyperlink_list:
        #gets i ready for parsing
        open_session = requests.Session()
        open_session.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
        page = open_session.get(i)
        tree = html.fromstring(page.content)

        #grabs all of the links from i
        for link in tree.xpath('//a/@href'):
            level8_relative_link_list.append(link)

        #filters the links
        level8_relative_link_list = filter_links(level8_relative_link_list)

        #cuts out leading /
        for j in range(len(level8_relative_link_list)):
            if level8_relative_link_list[j][0] == '/': level8_relative_link_list[j] = level8_relative_link_list[j][1:]
        
        #creates the level8 list
        for relative_link in level8_relative_link_list:
            if relative_link not in i: level8_link_list.append(i + relative_link)

        level8_relative_link_list = []
    
    hyperlink_list = []
    
    #does some basic sorting
    for i in level8_link_list:
        if i[-2:] == '//': continue
        elif i[-1] == '/': hyperlink_list.append(i)
        else: master_list.append(i)

    time.sleep(8)



def level9():
#this function grabs the links from level 8 and sorts them

    global level9_link_list, level9_relative_link_list, master_list, hyperlink_list
    
    for i in hyperlink_list:
        #gets i ready for parsing
        open_session = requests.Session()
        open_session.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
        page = open_session.get(i)
        tree = html.fromstring(page.content)

        #grabs all of the links from i
        for link in tree.xpath('//a/@href'):
            level9_relative_link_list.append(link)

        #filters the links
        level9_relative_link_list = filter_links(level9_relative_link_list)

        #cuts out leading /
        for j in range(len(level9_relative_link_list)):
            if level9_relative_link_list[j][0] == '/': level9_relative_link_list[j] = level9_relative_link_list[j][1:]
        
        #creates the level9 list
        for relative_link in level9_relative_link_list:
            if relative_link not in i: level9_link_list.append(i + relative_link)

        level9_relative_link_list = []
    
    hyperlink_list = []
    
    #does some basic sorting
    for i in level9_link_list:
        if i[-2:] == '//': continue
        elif i[-1] == '/': hyperlink_list.append(i)
        else: master_list.append(i)

    time.sleep(9)



def level10():
#this function grabs the links from level 9 and sorts them

    global level10_link_list, level10_relative_link_list, master_list, hyperlink_list
    
    for i in hyperlink_list:
        #gets i ready for parsing
        open_session = requests.Session()
        open_session.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
        page = open_session.get(i)
        tree = html.fromstring(page.content)

        #grabs all of the links from i
        for link in tree.xpath('//a/@href'):
            level10_relative_link_list.append(link)

        #filters the links
        level10_relative_link_list = filter_links(level10_relative_link_list)

        #cuts out leading /
        for j in range(len(level10_relative_link_list)):
            if level10_relative_link_list[j][0] == '/': level10_relative_link_list[j] = level10_relative_link_list[j][1:]
        
        #creates the level10 list
        for relative_link in level10_relative_link_list:
            if relative_link not in i: level10_link_list.append(i + relative_link)

        level10_relative_link_list = []
    
    hyperlink_list = []
    
    #does some basic sorting
    for i in level10_link_list:
        if i[-2:] == '//': continue
        elif i[-1] == '/': hyperlink_list.append(i)
        else: master_list.append(i)

    time.sleep(10)



#runs levels 1 thorugh 10 to get all pdfs and programs in a list
start = time.time()
level1()
end = time.time()
print "Level1 took " + str((end-start)/60) + " minutes."
start = time.time()
level2()
end = time.time()
print "Level2 took " + str((end-start)/60) + " minutes."
start = time.time()
level3()
end = time.time()
print "Level3 took " + str((end-start)/60) + " minutes."
start = time.time()
level4()
end = time.time()
print "Level4 took " + str((end-start)/60) + " minutes."
start = time.time()
level5()
end = time.time()
print "Level5 took " + str((end-start)/60) + " minutes."
start = time.time()
level6()
end = time.time()
print "Level6 took " + str((end-start)/60) + " minutes."
start = time.time()
level7()
end = time.time()
print "Level7 took " + str((end-start)/60) + " minutes."
start = time.time()
level8()
end = time.time()
print "Level8 took " + str((end-start)/60) + " minutes."
start = time.time()
level9()
end = time.time()
print "Level9 took " + str((end-start)/60) + " minutes."
start = time.time()
level10()
end = time.time()
print "Level10 took " + str((end-start)/60) + " minutes."

#now sort the master_list and download the files
sorter()
grabber()
