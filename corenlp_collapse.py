from pycorenlp import StanfordCoreNLP
import argparse

nlp = None

annotators = 'tokenize,ssplit,pos,depparse'

output_format = "json"

# startup_text = "The quick brown fox jumps over the lazy dog"

property_dict = {'annotators': annotators, 'outputFormat': output_format}

# output = nlp.annotate(startup_text, properties=property_dict)

def is_port_in_use(port):
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0
    
    
def create_corenlp_obj():
	if not is_port_in_use(9000):
		print("core nlp server is not running")
		return False
	global nlp
	nlp = StanfordCoreNLP('http://localhost:9000')
	return True

class Token:
	def __init__(self, string, index, pos=None):
		self.string = string
		self.index = index
		self.pos = pos
		
	def __hash__(self):
		return hash(self.index)
	
	def __eq__(self, other):
		if not hasattr(other, "index"):
			return False
		return self.index == other.index
	
	def __ne__(self, other):
		return not self.__eq__(other)
	
	def __repr__(self):
		return self.__str__()
	
	# def __str__(self):
		# return "{}:{}".format(self.index, self.string)

	def __str__(self):
		return "{}:{}({})".format(self.index, self.string, self.pos)


def getParse(txt):
	return nlp.annotate(txt, properties=property_dict)


def collapse(parse):
	# one sentence at a time
	always_first_sent = parse['sentences'][0]
	
	# universal dependency from
	ud_form = always_first_sent['enhancedPlusPlusDependencies']
	
	# tokens for pos
	corenlp_tokens = always_first_sent["tokens"]

	tokens = []
	
	print("\ndependencies:\n")
	for dict_item in ud_form:
		parent_index =  dict_item["governor"]
		child_index = dict_item["dependent"]
		if parent_index == 0:
			parent_pos = None
		else:
			parent_pos = corenlp_tokens[parent_index-1]["pos"]
		
		parent = Token(dict_item["governorGloss"], parent_index, parent_pos)
		child = Token(dict_item["dependentGloss"], child_index, corenlp_tokens[child_index-1]["pos"])
		if parent not in tokens:
			tokens.append(parent)
		if child not in tokens:
			tokens.append(child)
		relation = dict_item["dep"]
		print("{}\t({},\t{})".format(relation, parent, child))
		
	tokens.sort(key=lambda x: x.index)
	print("\ntokens: {}".format(tokens))


if __name__ == "__main__":
	""" 
	usage:
	python3 corenlp_collapse.py --text "how do i fulfill a money request?"
	"""

	parser = argparse.ArgumentParser(description="corenlp dep parse -- collapsed")
	parser.add_argument("--text=", dest="TEXT", default="What do i do with a money request?", help="put text here duh")
	args = parser.parse_args()
	
	# Create nlp object, or issue warning
	status = create_corenlp_obj()

	if status or nlp is None:
		parse = getParse(args.TEXT)
		collapse(parse)