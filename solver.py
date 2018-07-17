from heapq import heapify, heappush, heappop;
from linear import linear_cost
import time

start_time = time.time()

def manhattan (dim, grid, target):
	result = 0;
	for i in range (dim):
		for j in range (dim):
			if (target [i] [j] == 0):
				continue;
			for l in range (dim):
				for m in range (dim):
					if (target [i] [j] == grid [l] [m]):
						result += (abs (m - j) + abs (l - i));
						break;
	

	linear_conflicts = linear_cost(grid)

	return result + linear_conflicts;

def getNextStates (dim, current):
	nextStates = [];
	empty = None;

	for i in range (dim):
		try:
			empty = current [i].index (0);
		except Exception as e:
			continue;
		empty = (i, empty);
		break;

	if (empty [1] < (dim - 1)):
		a = [ i.copy () for i in current ];
		a [empty [0]] [empty [1]], a [empty [0]] [empty [1] + 1] = a [empty [0]] [empty [1] + 1], a [empty [0]] [empty [1]];
		nextStates.append (('RIGHT', a, (empty [0], empty [1] + 1)));

	if (empty [1] > 0):
		b = [ i.copy () for i in current ];
		b [empty [0]] [empty [1]], b [empty [0]] [empty [1] - 1] = b [empty [0]] [empty [1] - 1], b [empty [0]] [empty [1]];
		nextStates.append (('LEFT', b, (empty [0], empty [1] - 1)));

	if (empty [0] > 0):
		c = [ i.copy () for i in current ];
		c [empty [0]] [empty [1]], c [empty [0] - 1] [empty [1]] = c [empty [0] - 1] [empty [1]], c [empty [0]] [empty [1]];
		nextStates.append (('UP', c, (empty [0] - 1, empty [1])));

	if (empty [0] < (dim - 1)):
		d = [ i.copy () for i in current ];
		d [empty [0]] [empty [1]], d [empty [0] + 1] [empty [1]] = d [empty [0] + 1] [empty [1]], d [empty [0]] [empty [1]];
		nextStates.append (('DOWN', d, (empty [0] + 1, empty [1])));

	return (nextStates);

def getSequenceInfo (dim, grid):
	
	if dim == 3:
		target = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
	elif dim == 4:
		target = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]
	elif dim == 5:
		target = [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15], [16, 17, 18, 19, 20], [21, 22, 23, 24, 0]]
	else:
		print('dimension error, please use legal input')


	current = (manhattan (dim, grid, target), 0, [], grid)
	stateTree = [current]

	heapify (stateTree);
	while (not current [-1] == target):
		current = heappop (stateTree)

		for state in getNextStates (dim, current [-1]):
			heappush (stateTree, (manhattan (dim, state [1], target) + current [1] + 1, current [1] + 1, current [2] + [state [0]], state [1]))

	return (current [1], current [2])

if (__name__ == '__main__'):


	# read from file
	with open("n-puzzle.txt") as textFile:
		grid = [line.split() for line in textFile]
	
	dim = len(grid)

	for x in range(dim):
		for y in range(dim):
			grid[x][y] = int(grid[x][y])

	seqCount, sequence = getSequenceInfo (dim, grid);
	print(f'solved in {seqCount} moves')
	print("--- %s seconds ---" % (time.time() - start_time))
	print('\n'.join (sequence))