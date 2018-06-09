# import bibtexparser
# from bibtexparser.bwriter import BibTexWriter
# from bibtexparser.bibdatabase import BibDatabase


# inputfile = '~/Documents/CICL/homepage/static/bibtext/cic_papers.bib'
# inputfile = 'static/bibtex/cic_papers.bib'

# with open(inputfile, encoding='utf8') as bibtex_file:
# 	bib_database = bibtexparser.load(bibtex_file)

# print(bib_database.entries[0])

# string -> string
def format_authors(authors):
	# authors_str = ''

	# '" and " seems to be the consistent split term'
	auts = authors.split(' and ')

	for a in range(len(auts)):
		words = auts[a].split()
		# print(words)

		# if the name does not contain a comma, it is not last name first
		# take the last name and put it on the front
		if ',' not in words[0]:
			words = [words[-1]] + words[:len(words) - 1]

		# Don't alter the last name. For all other names replace with first inital period
		for i in range(1, len(words)):
			words[i] = words[i][0] + '.'

		auts[a] = ' '.join(words)
		# authors_str = authors_str + ' '.join(words)

	return ', '.join(auts)



def strip_brackets(s):
	s = s.replace('{', '')
	s = s.replace('}', '')
	return s

# entry (dictionary) -> string
def construct_citation(entry):
	# I was getting a lot of arbitrary fields with latex capitalization brackets
	# thrown in. There didn't seem like a good systematic way to check so I
	# just removed them from all fields. I don't think this cause any issues
	# but can check
	entry = {k:strip_brackets(v) for k,v in entry.items()}

	authors = format_authors(entry['author']) if 'author' in entry else ''
	year = ' (' + entry['year'] + ')' if 'year' in entry else ''
	title = '. ' + entry['title'] if 'title' in entry else ''
	citation = authors + year + title

	if entry['ENTRYTYPE'] == 'article':
		# handle cases with unpublished papers
		volume = ', ' + entry['volume'] if 'volume' in entry else ''
		pages = ', ' + entry['pages'] if 'pages' in entry else ''

		# submitted special case?
		journal = ''
		if 'journal' in entry:
			if entry['journal'] != 'submitted':
				journal = '. In _' + entry['journal'] + '_'
			else:
				journal = '. submitted'
		# journal = '. In _' + entry['journal'] + '_' if entry['journal'].lower() != 'submitted' else '. Submitted'
		journal = journal.replace('\\', '')

		citation = citation + journal + volume + pages + '.'

	elif entry['ENTRYTYPE'] == 'inproceedings':
		# strange case Rational order effects in responsibility attributions
		conference = '. In _' + entry['booktitle'] + '_' if 'booktitle' in entry else ''
		address = ', ' + entry['address'] if 'address' in entry else ''
		year = ', ' + entry['year'] if 'year' in entry else ''
		pages = ' (pp. ' + entry['pages'] + ')' if 'pages' in entry else ''
		publisher = '. ' + entry['publisher'] if 'publisher' in entry else ''

		citation = citation + conference + address + year + pages + publisher + '.'

	elif entry['ENTRYTYPE'] == 'incollection':
		# fill in citation generation for in colleciton
		book = '. In _' + entry['booktitle'] + '_' if 'booktitle' in entry else ''
		pages = ' (pp. ' + entry['pages'] + ')' if 'pages' in entry else ''
		publisher = '. ' + entry['publisher'] if 'publisher' in entry else ''

		citation = citation + book + pages + publisher + '.'

	else:
		raise ValueError('Entry does not have a valid entry type')

	return '"' + citation + '"'


def print_citations(entrytype=None):

	if entrytype == None:
		for e in bib_database.entries:
			print(construct_citation(e))
			print()

	else:
		for e in bib_database.entries:
			if e['ENTRYTYPE'] == entrytype:
				print(construct_citation(e))
				print()





