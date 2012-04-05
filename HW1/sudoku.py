# sudoku.py
# written by Nathan Fraenkel
# worked with: Boyang Zhang

class SudokuBoard:
	def __init__(self, name):
		self.filename = name
		self.board = self.parseBoard(name)
		self.__constraints = self.__computeConstraintSets()
		self.__pointDict = self.__computePointDict() 
	
	def parseBoard(self, name):
		board = []
		f = open(name, 'r')
		j = f.read()
		out = j.replace('*', '0').split('\n')
		out = [list(i) for i in out]
		for x in range(len(out)):
			board.append([int(b) for b in out[x]])
		return board
	
	def printBoard(self):
		string = ""
		for x in range(len(self.board)):
			for y in range(len(self.board)):
				if y == 3 or y == 6:
					string = string + ' |  '
				if y != 8 and self.board[x][y] == 0:
					string = string + '* '
				elif y == 8 and self.board[x][y] == 0:
					string = string + '*'
				elif y == 8 and self.board[x][y] != 0:
					string = string + str(self.board[x][y])
				else:
					string = string + str(self.board[x][y]) + ' '
			string = string + '\n'
			if x == 2 or x == 5:
				string = string + '-------+---------+-------\n'
		print string,

	def __computeConstraintSets(self): 
		cons = []
		cons.extend([set([(x,y) for x in range(9)]) for y in range(9)])
		cons.extend([set([(y,x) for x in range(9)]) for y in range(9)])
		cons.extend([set([(x,y) for x in range(z, z+3) for y in range(z2, z2+3)]) for z2 in [0,3,6] for z in [0, 3, 6]])
		return cons

	def __computePointDict(self):
		new_dict = {}
		for x in range(len(self.__constraints[0])): 
			for y in range(len(self.__constraints[0])): 
				new_dict[(x,y)] = [s for s in self.__constraints if (x,y) in s]	
		return new_dict
	
	def getConstraintSets(self, loc):
		return self.__pointDict[loc] 

	def computeUnusedNums(self, constraint): 
		unused = set([1,2,3,4,5,6,7,8,9])
		for tup in constraint:
			if self.board[tup[0]][tup[1]] != 0: 
				unused.remove(self.board[tup[0]][tup[1]])		
		return unused	

	def isSolved(self):
		solved = True
		for s in self.__constraints: 
			if self.computeUnusedNums(s) != set([]):
				solved = False
				break
		return solved


