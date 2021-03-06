import os
import sys
path = os.path.split(sys.argv[0])[0]
sys.path.append(
			'\\'.join(path.split('\\')[:-1]))

from analyzer.expression import exp
from analyzer.data import regex
from optimizer.optimizer import code_optimizer
import re


data = regex
ERR_RE_MSG = 'Error: invalid regular expression'

class Regex:
	
	'''Holds all the regular expression inside data.py file
	   and find all the matches with the passed code then
	   passes each match to the optimizer individually'''

	#reads the regular expressions from data.py and 
	#create object for each regex

	_data = [
		exp(re, data[re][0], data[re][1], data[re][2])
		for re in data
	] #exp(name, type, pattern, description)
	_numberOfRegex = len(_data) #Count the overall number of the regular expressions
	fixed_code = '' #Holds the optimized code

	def __len__(self): #returns number of regular expressions 
		return Regex._numberOfRegex 

	@staticmethod
	def read_code(file):
		'''Read file content and return it inside a variable'''
		
		with open(file) as f:
			content = f.read()

		return content

	@staticmethod
	def compile_regex(regex):
		''' Compiles the passed regular expression and test if it's valid
			,if so, it returns the compiled regex, otherwise it prints out
			an error message, but never stop, the reason behind that is to
			check the other regular expressions. '''
		
		try:
			pattern = re.compile(regex.pattern, re.VERBOSE)
		except:
			print(f'{ERR_RE_MSG}\nName:{regex.name}\nType:{regex.type}')
		else:
		 	return pattern

	@staticmethod
	def find_matches(pattern, name):
		"""Find matches the pass the matches to code_optimizer
		   class."""
		matches = pattern.finditer(Regex.fixed_code)
		Regex.fixed_code = code_optimizer.optimize(matches, name, Regex.fixed_code)

	@staticmethod
	def output_code():
		with open('optimizedCode.py', 'w') as output:
			output.write(Regex.fixed_code)

	@staticmethod
	def check_regex(code):
		'''Run over all the regular expression inside _data and check
		   there validity, then passes the expression to find_matches()
		   modular if any there's any match.'''
		Regex.fixed_code = code
		for regex in Regex._data:
			pattern = Regex.compile_regex(regex)
			if(not pattern.search(code)): continue
			else:
				Regex.find_matches(pattern, regex.name)

		Regex.output_code()

		

	@staticmethod
	def main(code_file):
		'''The analyzing starter porcess'''
		
		code = Regex.read_code(code_file)
		
		Regex.check_regex(code)

def run_analyzer(code_file):
	Regex.main(code_file)

if __name__ == '__main__':
	sys.exit()

