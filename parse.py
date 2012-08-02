from modgrammar import *
import tax

class TaxonName (Grammar):
	grammar = (WORD("A-Za-z "))

class TaxonExtension (Grammar):
	grammar = (L("children") | L("parent") | L("siblings"))

class TaxonFull (Grammar):
	grammar = ( TaxonName, OPTIONAL(':', TaxonExtension) )


class TaxonList (Grammar):
	grammar = (  '(' , LIST_OF(OR(TaxonFull, REF('TaxonList')), sep=",") , ')'  )

class Tree (Grammar):
	grammar = (  TaxonList  )


tree_parser = Tree.parser()

def list_subtrees(tree, level = 0):
	for subtree in tree.find_all(TaxonList):
		print('   ' * level + repr(subtree))
		list_subtrees(subtree, level+1)


def expand_taxon(taxon):
	print(repr(taxon))
	taxon_name = taxon.elements[0].string
	taxon_extension = taxon.elements[1]
	# if the extension is none, then just add the name 
	if taxon_extension == None:
		return [taxon_name]
	else:
		print(taxon_extension)
		# deal with children
		if taxon_extension.string == ':children':
			return (tax.get_children(taxon_name))
		if taxon_extension.string == ':parent':
			return [tax.get_parent(taxon_name)]
		if taxon_extension.string == ':siblings':
			return tax.get_siblings(taxon_name)

def expand_list(list):
	result = []
	for taxon in list.find_all(TaxonFull):
		result.extend(expand_taxon(taxon))
	return result

def get_taxon_list(input):
	parsed = tree_parser.parse_string(input)

	result = []
	for tax_list in parsed.find_all(TaxonList):
		print(repr(tax_list))
		result.extend(expand_list(tax_list))

	return result

print(get_taxon_list('(nematoda)'))
print(get_taxon_list('(nematoda, arthropoda, sea spiders)'))
print(get_taxon_list('(Nematoda:children, arthropoda, sea spiders)'))
print(get_taxon_list('(Coleoptera:parent, Nematoda, Eutheria)'))
print(get_taxon_list('(Coleoptera:siblings)'))

# test_tree = tree_parser.parse_string('(alpha, (beta, gamma))')
# list_subtrees(test_tree)

