__author__ = 'cromox'
'''
to show the PageSource view of specific page or site.
Example how to run :
$ python3 PAGESOURCE_IndentView_InputDataFile.py

Python Version = 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]

Data file = test1_html_mengkome.html
DECL     : DOCTYPE html
............(output)...........
(will give the output - in Indent tab View style)

(This is using OOP (Object-Oriented Programming) with simple Polymorphism style of the Requests's GET output)
'''

from sys import version as pythonversion
from html.parser import HTMLParser
from html.entities import name2codepoint

### GET python version
print('Python Version = ' + pythonversion)
print()

class ReadableHTML(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.numtabbar = 0
        self.maxword = 150

    def handle_starttag(self, tag, attrs):
        print("  "*self.numtabbar + '/' + str(tag))
        self.numtabbar += 1
        if len(attrs) >= 1:
            for attr in attrs:
                print("  "*self.numtabbar + str(attr))

    def handle_endtag(self, tag):
        self.numtabbar -= 1
        print("  "*self.numtabbar + str(tag) + '/')

    def handle_data(self, data):
        if len(data) > self.maxword:
            endone = ' ...(cont)...'
        else:
            endone = ''
        print("  "*self.numtabbar + str(data.replace('\n', ' ').replace('  ', ' ').replace('   ', ' ')[:self.maxword]) + endone)

    def handle_comment(self, data):
        if len(data) > self.maxword:
            endone = ' ...(cont)...'
        else:
            endone = ''
        print("  "*self.numtabbar + str(data.replace('\n', ' ').replace('  ', ' ').replace('   ', ' ')[:self.maxword]) + endone)

    def handle_entityref(self, name):
        c = chr(name2codepoint[name])
        print("  "*self.numtabbar + str(c))

    def handle_charref(self, name):
        if name.startswith('x'):
            c = chr(int(name[1:], 16))
        else:
            c = chr(int(name))
        print("  "*self.numtabbar + str(c))

    def handle_decl(self, data):
        if len(data) > self.maxword:
            endone = ' ...(cont)...'
        else:
            endone = ''
        print("DECL     : " + str(data.replace('\n', ' ').replace('  ', ' ').replace('   ', ' ')[:self.maxword]) + endone)
        # print()

print()
file1 = input('Data file = ')
data1 = open(str(file1), 'r')
data2 = data1.read()
ReadableHTML().feed(data2)