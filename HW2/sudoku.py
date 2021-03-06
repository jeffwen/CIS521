# sudoku.py
# written by Nathan Fraenkel & Boyang Zhang

import Queue
import copy
import random


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
		while "" in out:
			out.remove("")
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
				if self.board[tup[0]][tup[1]] in unused: 
					unused.remove(self.board[tup[0]][tup[1]])		
		return unused	

	def isSolved(self):
		solved = True
		for s in self.__constraints: 
			if self.computeUnusedNums(s) != set([]):
				solved = False
				break
		return solved

	def violates(self, constraint):
		unused = set([1,2,3,4,5,6,7,8,9])
		found = []
		booleano = False
		for loc in constraint:
			if self.board[loc[0]][loc[1]] != 0:
				if self.board[loc[0]][loc[1]] in unused:
					unused.remove(self.board[loc[0]][loc[1]])
					found.append(self.board[loc[0]][loc[1]])
				else:
					if self.board[loc[0]][loc[1]] in found:
						return True					
		return booleano

	def inform(self, board):
		for s in self.__constraints:
			if self.violates(s):
				return False #False implies that this board should NOT be expanded
		return True

	def DFSsuccessor(self, q, board):
		for i in range(len(board)):
			for j in range(len(board[i])):
				if board[i][j] == 0:
					for k in [1,2,3,4,5,6,7,8,9]:
						temp = copy.deepcopy(board)
						temp[i][j] = k
						q.put(temp)
					return

	def DFS(self):
		time = 0
		space = 0
		q = Queue.LifoQueue(0)
		q.put(self.board)
		while (not q.empty()):
			if q.qsize() > space:
				space = q.qsize()
			self.board = q.get()
			if self.isSolved():
				return (self.board, time, space, 'solved')
			else:	
				if self.inform(copy.deepcopy(self.board)):
					self.DFSsuccessor(q, copy.deepcopy(self.board))
					time = time + 1
				else:	
					continue
		return (self.board, time, space, 'not solved')	

	def BFSsuccessor(self, q, board):
		for i in range(len(board)):
			for j in range(len(board[i])):
				if board[i][j] == 0:
					for k in [1,2,3,4,5,6,7,8,9]:
						temp = copy.deepcopy(board)
						temp[i][j] = k
						q.put(temp)
					return

	def BFS(self):
		time = 0
		space = 0
		q = Queue.Queue(0)
		q.put(self.board)
		while (not q.empty()):
			if q.qsize() > space:
				space = q.qsize()
			self.board = q.get()
			if self.isSolved():
				return (self.board, time, space, 'solved')
			else:	
				if self.inform(copy.deepcopy(self.board)):
					self.BFSsuccessor(q, copy.deepcopy(self.board))
					time = time + 1
				else: 
					continue
		return (self.board, time, space, 'not solved')

	def count(self, constraint, board):
		unused = set([1,2,3,4,5,6,7,8,9])
		for t in constraint:
			if board[t[0]][t[1]] != 0:
				if board[t[0]][t[1]] in unused:
					unused.remove(board[t[0]][t[1]])		
		return len(unused)

	def cost(self, board):
		sum = 0
		for s in self.__constraints:
			sum = sum + self.count(s, board)	
		return sum

	def initialize(self, board):
		col_constr = []
		col = 0
		for s in self.__constraints: #for each constraint (= a set of locations)
			elem = s.pop()
			s.add(elem)
			for loc in s: #for each location in s
				booleano = True
				col = loc[1] #col = col value
				if not col == elem[1]:
					booleano = False
					break
			if booleano == True:
				col_constr.append(s)
		#now col_constr contains all constraits related to columns
		for s in col_constr:
			if self.computeUnusedNums(s) != set([]):
				unused = self.computeUnusedNums(s)
				for t in s:
					if board[t[0]][t[1]] == 0:
						board[t[0]][t[1]] = unused.pop()
		return 
		

	def annealSuccessor(self, board, l):
		length = len(l)
		one = random.randint(0, length-1)
		two = random.randint(0, length-1)
		loc1 = l[one]
		loc2 = l[two]
		temp = board[loc1[0]][loc1[1]]
		board[loc1[0]][loc1[1]] = board[loc2[0]][loc2[1]]
		board[loc2[0]][loc2[1]] = temp
		return board

	def anneal(self, maxx):
		t = 0 # t = our iteration counter
		rej = 0 # rej = num of rejected uphill moves
		up = 0 # up = num of taken uphill moves
		down = 0 # down = num of taken downhill moves
		non_fixed = []
		p = 0.7
		random.seed(12345.6789)
		for i in range(len(self.board)):
			for j in range(len(self.board[i])):
				if self.board[i][j] == 0:
					non_fixed.append((i,j))
		#now, non_fixed is a list of all non-fixed locations
		self.initialize(self.board) #this will initialize our initially unfilled board
		while (not self.isSolved()) and (t != maxx) :
			b1 = copy.deepcopy(self.board)
			b2 = self.annealSuccessor(copy.deepcopy(b1), non_fixed) #b2 = potential successor of b1
			b1_cost = self.cost(b1)
			b2_cost = self.cost(b2)
			if b2_cost < b1_cost:
				self.board = b2
				down = down + 1
			else: #b2_cost > b1_cost, so b2 is a WORSE board than b1
				q = random.random()
				if q <= p:
					self.board = b2
					up = up + 1
				else:
					self.board = b1
					rej = rej + 1
			p = p * 0.99
			t = t + 1
		return (self.board, down, rej, up, self.isSolved())





