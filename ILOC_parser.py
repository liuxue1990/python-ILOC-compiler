"""
"""
import re
from ILOC_grammer import *
from Instruction import *

ILOC_SYNTAX_ERROR = """File %(filename)s, in line %(line_number)s:
	%(line)s
ILOCSyntaxError: invalid syntax"""

class ILOCSyntaxError(Exception):
	"""docstring for ILOCSyntaxError"""
	def __init__(self, filename, line, line_number):
		self.filename = filename
		self.line = line
		#normally line number start on 1
		self.line_number = line_number + 1
	def  __str__(self):
		return ILOC_SYNTAX_ERROR % {"filename": self.filename.name, 
						"line_number": self.line_number, 
						"line": self.line}

class ILOCParser():
	"""docstring for Scanner"""
	def __init__(self, source_file):
		self.source_file = source_file
		self.source_line = []
		self.instruction_list = []
		self.parser_operation_re =  re.compile(GRAMMER_OPERATION_RE)
		self.parser_comment_re =  re.compile(GRAMMER_COMMENT_RE)

	def scan(self):
		self.source_line = self.source_file.readlines()
		self.source_file.close()
	
	def parse(self):
		""""""
		def add_instruction_list(new_line_number, a_line, line_number):
			""""""
			#really slow version of implementation,
			#and not clean way to handle three operator instructions
			def is_register(a_register):
				if not a_register:
					return False
				if not a_register.find("r") == -1:
					return True
				return False

			def operator_allocate(source):
				if is_register(source):
					return {"source" : source, "virtual" : None, "physical" : None, "nextuse" : None}
				else:
					return source

			def preprocess(a_line):
				comment_index = a_line.find("//")
				if not comment_index == -1:
					a_line = a_line[0 : comment_index]
				a_line = a_line.replace(",", " ", 1)
				a_line = a_line.replace("=>", " ", 1)
				# a_line = a_line.
				new_line_list =  a_line.split()
				return new_line_list

			def instruction_factory(new_line_list):
				new_line_list_len = len(new_line_list)
				if new_line_list_len == 3:
					if new_line_list[0] == "store":
						return Instruction(new_line_number, new_line_list[0], 
						InstructionType.store,
						op_one =  operator_allocate(new_line_list[1]),
						op_two = operator_allocate(new_line_list[2]))
					else:
						return Instruction(new_line_number, new_line_list[0], 
						InstructionType.two_op,
						op_one =operator_allocate(new_line_list[1]),
						op_three = operator_allocate(new_line_list[2]))
				if new_line_list_len == 4:
					return Instruction(new_line_number,new_line_list[0], 
						InstructionType.three_op,
						op_one = operator_allocate(new_line_list[1]),
						op_two = operator_allocate(new_line_list[2]),
						op_three = operator_allocate(new_line_list[3]))
				if new_line_list_len == 2:
					return Instruction(new_line_number,new_line_list[0], 
						InstructionType.one_op,
						op_one =operator_allocate(new_line_list[1]))
				if new_line_list_len ==1:
					return Instruction(new_line_number,new_line_list[0], InstructionType.none_op)
				print new_line_list
				raise ILOCSyntaxError(self.source_file, a_line, line_number)

			new_line_list = preprocess(a_line)
			self.instruction_list.append(instruction_factory(new_line_list))
			
		new_line_number = 0
		for line_number, a_line in enumerate(self.source_line):
			#we assume code lines are much greater than empty lines
			if self.parser_operation_re.match(a_line):
				add_instruction_list(new_line_number, a_line, line_number)
				new_line_number += 1
			elif self.parser_comment_re.match(a_line):
				pass
			else:
				raise ILOCSyntaxError(self.source_file, a_line, line_number)

	def get_instruction_list(self):
		return self.instruction_list

	def print_instruction_list(self):
		for a_instruction in self.instruction_list:
			print a_instruction.get_str("source")


		