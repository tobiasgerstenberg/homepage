#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Receives a Bibtex file and produces the markdown files for academic-hugo theme

@author: Petros Aristidou
@contact: p.aristidou@ieee.org
@date: 19-10-2017
@version: alpha

@adapted by Tobias Gerstenberg
@date: 11-21-2017

It would be nice to adapt the parser in the future so that it creates the long publication in APA style. Maybe using: https://docs.pybtex.org/
"""

import bibtexparser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
import os, sys, getopt
from citation_generator import construct_citation
import datetime

def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def supetrim(string):
    return string.replace("\\" , "").replace("{" , "").replace("}" , "").replace("\n"," ")

def month_string_to_number(string):
    m = {
        'jan':1,
        'feb':2,
        'mar':3,
        'apr':4,
        'may':5,
        'jun':6,
        'jul':7,
        'aug':8,
        'sep':9,
        'oct':10,
        'nov':11,
        'dec':12
        }
    s = string.strip()[:3].lower()
    try:
        out = m[s]
        return out
    except:
        raise ValueError('Not a month')

# You can add the name of a co-author and their website and it will create a link on the publications website
def get_author_link(string):
    web = {
        # 'T. Gerstenberg':'https://tobiasgerstenberg.github.io/'
        }
    out = ''
    try:
        out = web[string]
    except:
        print("Author's "+string+" website is missing.")
    return out

def main(argv):
    inputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hi:", ["ifile="])
    except getopt.GetoptError:
        print('parse_bib.py -i <inputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('parse_bib.py -i <inputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
    return inputfile

if __name__ == "__main__":
    inputfile = main(sys.argv[1:])
    try:
        with open(inputfile, encoding="utf8") as bibtex_file:
            bibtex_str = bibtex_file.read()
    except EnvironmentError:  # parent of IOError, OSError *and* WindowsError where available
        print('File '+inputfile+' not found or some other error...')

    # It takes the type of the bibtex entry and maps to a corresponding category of the academic theme
    pubtype_dict = {
        'forthcoming': '"0"',
        'uncategorized': '"0"',
        'preprint': '"1"',
        'article': '"2"',
        'inproceedings': '"3"',
        'incollection': '"4"',
        'thesis': '"5"'
    }
    
    bib_database = bibtexparser.loads(bibtex_str)

    # loop over entries 
    for entry in bib_database.entries:
        filenm='content/publication/'+entry['ID']+'.md'
        
        # If the same publication exists, then skip the creation. I customize the .md files later, so I don't want them overwritten. Only new publications are created.
        if os.path.isfile(filenm):
            pass
        else:
            with open(filenm, 'w', encoding="utf8") as the_file:
                the_file.write('+++\n')
                the_file.write("# 0 -> 'Forthcoming',\n# 1 -> 'Preprint',\n# 2 -> 'Journal',\n# 3 -> 'Conference Proceedings',\n# 4 -> 'Book chapter',\n# 5 -> 'Thesis'\n\n")
                the_file.write('title = "'+supetrim(entry['title'])+'"\n')
                #print('Parsing ' + entry['ID'])
                
                if 'year' in entry:
                    yr = entry['year']
                    if RepresentsInt(yr):
                        date = yr
                        if 'month' in entry:
                            if RepresentsInt(entry['month']):
                               month = entry['month']
                            else:
                               month = str(month_string_to_number(entry['month']))
                            date = date+'-'+ month.zfill(2)
                        else:
                           date = date+'-01'
                        the_file.write('date = "'+date+'-01"\n')
                    else:
                        dt = datetime.datetime.now()
                        date = str(dt.year) + '-' + str(dt.month).zfill(2) + '-' + str(dt.day).zfill(2)
                        the_file.write('date = "'+date+'"\n')
                        the_file.write('year = "'+yr+'"\n')
                else:
                        dt = datetime.datetime.now()
                        date = str(dt.year) + '-' + str(dt.month).zfill(2) + '-' + str(dt.day).zfill(2)

                    
                # Treating the authors
                if 'author' in entry:
                    authors = entry['author'].split(' and ')
                    the_file.write('authors = [')
                    authors_str = ''
                    for author in authors:
                        author_strip = supetrim(author)
                        author_split = author_strip.split(',')
                        if len(author_split)==2:
                            author_strip = author_split[1].strip() + ' ' +author_split[0].strip()
                        author_split = author_strip.split(' ')
                        author_strip = author_split[0][0]+'. '+' '.join(map(str, author_split[1:]))
                        author_web = get_author_link(author_strip)
                        if author_web:
                            authors_str = authors_str + '"['+author_strip+'](' + author_web + ')",'
                        else:
                            authors_str = authors_str+ '"'+author_strip+'",'
                    the_file.write(authors_str[:-1]+']\n')
                
                # Treating the publication type
                if 'ENTRYTYPE' in entry:
                    # This type of treatment seems like overkill given what we want to achieve
                    # All we need to check is the ENTRYTYPE and then add whether it is forthcoming

                    # if 'booktitle' in entry and ('Seminar' in supetrim(entry['booktitle'])):
                    #     the_file.write('publication_types = ['+pubtype_dict['PW']+']\n')
                    # elif 'booktitle' in entry and ('Workshop' in supetrim(entry['booktitle'])):
                    #     the_file.write('publication_types = ['+pubtype_dict['conference']+']\n')
                    # elif 'note' in entry and ('review' in supetrim(entry['note'])):
                    #     the_file.write('publication_types = ['+pubtype_dict['submitted']+']\n')
                    # elif 'note' in entry and ('Conditional' in supetrim(entry['note'])):
                    #     the_file.write('publication_types = ['+pubtype_dict['submitted']+']\n')
                    # else:
                    #     the_file.write('publication_types = ['+pubtype_dict[entry['ENTRYTYPE']]+']\n')
                    pub_type_entry = 'publication_types = [' + pubtype_dict[entry['ENTRYTYPE']] + ']\n'
                    if 'year' in entry:
                        if not RepresentsInt(entry['year']):
                            pub_type_entry = pub_type_entry.replace('[', '[' + pubtype_dict['forthcoming'] + ', ')

                    the_file.write(pub_type_entry)

                else:
                    the_file.write('publication_types = [' + pubtype_dict[entry['uncategorized']] + ']\n')

                
                # Treating the publication journal, conference, etc.
                if 'booktitle' in entry:
                    the_file.write('publication_short = "_'+supetrim(entry['booktitle'])+'_"\n')
                elif 'journal' in entry:
                    the_file.write('publication_short = "_'+supetrim(entry['journal'])+'_"\n')
                elif 'school' in entry:
                    the_file.write('publication_short = "_'+supetrim(entry['school'])+'_"\n')
                elif 'institution' in entry:
                    the_file.write('publication_short = "_'+supetrim(entry['institution'])+'_"\n')
                
                # I never put the short version. In the future I will use a dictionary like the authors to set the acronyms of important conferences and journals
                # Not sure what the above comment is about. This adds the citation to the markdown file
                the_file.write('publication = ' + construct_citation(entry) + '\n')
                
                # Add the abstract if it's available in the bibtex
                if 'abstract' in entry:
                    the_file.write('abstract = "'+supetrim(entry['abstract'])+'"\n')
                
                # Some features are disabled. I activate them later
                the_file.write('image_preview = ""\n')
                the_file.write('selected = false\n')
                the_file.write('projects = []\n')

                # Links (optional).
                the_file.write('#url_pdf = "papers/' + entry['ID']+ '.pdf"\n')
                the_file.write('url_preprint = ""\n')
                the_file.write('url_code = ""\n')
                the_file.write('url_dataset = ""\n')
                the_file.write('url_slides = ""\n')
                the_file.write('url_video = ""\n')
                the_file.write('url_poster = ""\n')
                the_file.write('url_source = ""\n')
                the_file.write('#url_custom = [{name = "Github", url = ""}]\n')

                # I add urls to the online version and the DOI
                # if 'link' in entry:
                #     the_file.write('url_pdf = "'+supetrim(entry['link'])+'"\n')
                # if 'doi' in entry:
                #     the_file.write('url_custom = [{name = "DOI", url = "'+'http://dx.doi.org/'+supetrim(entry['doi'])+'"}]\n')
                
                # Default parameters that can be later castomized
                the_file.write('math = true\n')
                the_file.write('highlight = true\n')
                the_file.write('[header]\n')
                the_file.write('# image = "publications/' + entry['ID']+ '.png"\n')
                the_file.write('caption = ""\n')
                
                # I keep in my bibtex file a parameter called award for publications that received an award (e.g., best paper, etc.)
                # if 'award' in entry:
                #     the_file.write('award = "true"\n')
                
                # I put the individual .bib entry to a file with the same name as the .md to create the CITE option
                # db = BibDatabase()
                # db.entries =[entry]
                # writer = BibTexWriter()
                # with open('static/files/citations/'+supetrim(entry['ID']+'.bib'), 'w', encoding="utf8") as bibfile:
                #     bibfile.write(writer.write(db))

                # the_file.write('+++\n\n')
                
                # Any notes are copied to the main document
                if 'note' in entry:
                    strTemp = supetrim(entry['note'])
                    the_file.write(strTemp + "\n")
                the_file.write('+++')
