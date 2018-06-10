import bibtexparser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase

import importlib.util
spec = importlib.util.spec_from_file_location('citation_generator', '../citation_generator.py')
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)


inputfile = 'test_papers.bib'

with open(inputfile, encoding='utf8') as bibtex_file:
	bib_database = bibtexparser.load(bibtex_file)

print()

# This prints the markdown formatted citations for the publications in the test
# file. It's an eyeball test. I was going to make the exam more rigid and comprehensive
# but ultimately determined time could better be spent solving other problems since
# the citation generator seemed to be in mostly good shape. Could be something to come
# back to time permitting -- Ari Beller
for entry in bib_database.entries:
	print(c.construct_citation(entry))
	print()


