# funtions to compute linear conflicts of a borad

# filter
def line_filter_as_row(row_number, input_rows):
	filtered = [item for item in input_rows[row_number] if (item-1) // len(input_rows) == row_number]
	return(filtered)

def line_filter_as_col(col_number, columns):
	filtered = [item for item in columns[col_number] if (item-1) % len(columns) == col_number]
	filtered[:] = (value for value in filtered if value != 0)
	return(filtered)

# core function to compute linear conflicts number
def compute_linear_conflicts(line, remove_min=0):

	conflicts_dict = {}

	# compute current conflicts
	for i, item in enumerate(line):
		
		current_conflicts = 0

		if i == 0:
			for left_item in line[1:]:
				if left_item < item:
					current_conflicts += 1
			conflicts_dict[item] = current_conflicts
		elif i == len(line) - 1:
			for left_item in line[:-1]:
				if left_item > item:
					current_conflicts += 1
			conflicts_dict[item] = current_conflicts
		else:
			for left_item in line[i+1:]:
				if left_item < item:
					current_conflicts += 1
			for left_item in line[:i]:
				if left_item > item:
					current_conflicts += 1
			conflicts_dict[item] = current_conflicts

	# recursion ends if the current seq is free of conflict
	if sum(conflicts_dict.values()) == 0:
		# print('no conflict to go, task complete')
		# print(f'remove_min is {remove_min}')
		return remove_min

	
	# for i in conflicts_dict:
	# 	print(f'i is {i} while j is {conflicts_dict[i]}')

	# remove the the one with most conflicts and recursion
	key_to_delete = max(conflicts_dict, key=lambda k: conflicts_dict[k])
	line.remove(key_to_delete)
	remove_min += 1
	return compute_linear_conflicts(line, remove_min)
	

# general function to be called
def linear_cost(input_rows):

	columns = list(zip(*input_rows))
	
	linear_conflicts = 0

	# dealing with rows conflicts
	for i in range(len(input_rows)):
		linear_conflicts += compute_linear_conflicts(line_filter_as_row(i, input_rows))

	# dealing with column conflicts
	for i in range(len(input_rows)):
		linear_conflicts += compute_linear_conflicts(line_filter_as_col(i, columns))

	# print(f'the board requires {linear_conflicts * 2} additional moves due to linear conflicts')
	return linear_conflicts * 2