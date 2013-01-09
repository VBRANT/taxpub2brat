#!usr/bin/python3.2
'''
To create BRAT stand off files from TaxPub files
Requires select-taxon-name.xsl

Text and taxon names from XML source are saved for later review/re-use outside this script

David King <d.j.king@open.ac.uk>
The Open University, July 2012
For the ViBRANT project, <http://vbrant.eu>
'''

import csv
from lxml import etree
import html.parser
import re
import sys

print('taxpub2brat started')

# used later for converting XML entities
decoder = html.parser.HTMLParser()
# used later for removing XML tags
strip_tags = re.compile('<[^>]*>')

# minimal error handling ;-)
if len(sys.argv) == 2:
    input_file_name = sys.argv[1]
    stem_file_name = input_file_name.rsplit('.', 1)[0]
else:
    print('no file name supplied\nscript closing')
    exit()

# encoding and newline specified to ensure consistency when run under Windows
with open(input_file_name, 'r', encoding='utf-8', newline='\n') as xml_file, \
    open(stem_file_name + '.txt', 'w+', encoding='utf-8', newline='\n') as text_file, \
    open(stem_file_name + '.ann', 'w', encoding='utf-8', newline='\n') as brat_file, \
    open(stem_file_name + '-tax2brat.tsv', 'w+', encoding='utf-8', newline='\n') as taxon_name_file, \
    open(stem_file_name + '-tax2brat.log', 'w', encoding='utf-8', newline='\n') as log_file:

    # process each line individually
    # using a crude regex to remove XML tags
    # then if any text present in the line, convert XML entities and write out result
    # be aware if TaxPub ever changes to support < or > in attributes the existing regex will remove them too
    print('extracting text')
    for line in xml_file:
        line_edited = strip_tags.sub('', line).strip()
        if len(line_edited) > 0:
            line_edited = decoder.unescape(line_edited)
            print(line_edited, file=text_file)
    print('extracted text')

    # parse XML source and XSLT
    # then apply XSLT to extract taxon names
    # taxon_name_file has end set to '' to prevent addition of an extra new line
    # because the XSL already inserts new lines
    print('extracting annotations')
    xml_tree = etree.parse(input_file_name)
    xsl_tree = etree.parse('select-taxon-name.xsl')
    transform = etree.XSLT(xsl_tree)
    print(str(transform(xml_tree)), file=taxon_name_file, end='')
    print('extracted annotations')

    # now we have source text and taxon names we can create stand off mark up
    print('starting mark up')
    # reset files to the beginning
    text_file.seek(0)
    taxon_name_file.seek(0)
    # read text as a long string
    text_source = text_file.read()
    # read taxon names into a dictionary, which makes later processing much easier
    taxon_elements = csv.DictReader(taxon_name_file, fieldnames= ['attribute', 'name'],  dialect='excel-tab')
    # start position for find, incremented with result so always start after a successful find
    start_pos = 0
    # provides a unique number to identify text-bound annotations
    t_counter = 0
    for element in taxon_elements:
        pos = text_source.find(element['name'], start_pos)
        print(element['attribute'] + '  ' + element['name'] + ' found at ' + str(pos), file=log_file) 
        if pos != -1:
            end_pos = pos + len(element['name'])
            start_pos = pos + 1
            t_counter += 1
            print('T{:d}\t{:s} {:d} {:d}\t{:s}'.format(t_counter, element['attribute'], pos, end_pos, element['name']), file=brat_file)
        else:
            print(element['attribute'] + '  ' + element['name'] + ' not found', file=log_file)
            start_pos += 1
    print('finished mark up')

print('taxpub2brat finished')
