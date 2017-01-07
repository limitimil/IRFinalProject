import sys
from colors import red
class NHIRDParser:
	def __init__(self, fmt):
	# fmt is a list of tuple with 3 element (col_name, begin, start)
	# this ctor will check the validity of fmt and colision
		self.fmt = {}
		for record in fmt:
			if record[0] in self.fmt.keys():
				#stderr about colision
				sys.stderr.write('name colition of label %s\n' % record[0])
			if record[1] > record[2]:
				#stderr about invalid start: end pair
				sys.stderr.write('invalid start, end pair of label %s\n' % record[0])
			self.fmt[record[0]] = (int(record[1]),int(reocrd[2]) )
			# this transfer might lead to ValueError when the input value is invalid.
	def showInfo(self, s):
		labels = ''
		values = ''
		for x in self.fmt.items():
			labels +=\
			('%%-%ss' %	(x[1][1] - x[1][0] + 1) ) % x[0] + '\t'
			values += s[x[1][0]: x[1][1] +1] + '\t'
		print labels
		print values
if __name__ == '__main__':
	if len(sys.argv)<2 :
		sys.stderr.write('at least one input file need\n')
		exit(7)
	np = NHIRDParser([
		('ID_BIRTHDAY',84,91),
		('ID',92,123),
		('ACODE_ICD9_1',132,146),
		('ACODE_ICD9_2',147,161),
		('ACODE_ICD9_3',162,176),
		('ICD_OP_CODE',177,191),
	])
	
