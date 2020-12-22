"""
File: boggle.py
Name: Danny Tsai
----------------------------------------
This program will simulate boggle game,
search all words in dictionary base on given matrix of alpha.
"""
import time
import tkinter as tk
# Constants
# This is the file name of the dictionary txt file
# we will be checking if a word exists by searching through it
FILE = 'dictionary.txt'

SIZE = 4  		# Control matrix size of boggle game setting
MIN_LETTER = 4  # Minimum number of letters in answer we need

# Global variable
dictionary = []  # List of dictionary load from txt


def main():
	"""
	This program will simulate boggle game,
	search all words in dictionary base on given matrix of alpha.
	"""
	# Make GUI
	top = tk.Tk()
	top.title('stanCode "Anagram Generator"')
	make_gui(top)
	top.mainloop()


def make_gui(top):
	"""
	This function will make GUI for boggle search
	:param top: (Tkinter object): The main window of GUI.
	"""
	label = tk.Label(top, text='Type one alphabet for every entry:', font=18)
	label.grid(row=0, column=0, columnspan=12, sticky='w')

	entry_row = 1
	entry_dict = {}
	for y in range(1, SIZE+1):
		for x in range(1, SIZE+1):
			entry_dict[(x, y)] = tk.Entry(top, width=5)
			entry_dict[(x, y)].grid(row=entry_row+y, column=x-1)

	massage_out = tk.Label(top, font=18)
	massage_out.grid(row=entry_row+SIZE+1, column=0, columnspan=SIZE+1)

	label_out = tk.Label(top, text='Answer will show below:', font=18)
	label_out.grid(row=entry_row+SIZE+4, column=0, columnspan=SIZE+1, sticky='w')
	search_out = tk.Text(top, height=30, width=50, name='search_out')
	search_out.grid(row=entry_row+SIZE+5, column=0, columnspan=SIZE+1, sticky='w')

	start_button = tk.Button(
		top, text='Show Answer', command=lambda: input_check(entry_dict, massage_out, search_out))
	start_button.grid(row=entry_row+SIZE+3, column=0, columnspan=SIZE+1)


def input_check(entry_dict, massage_out, search_out):
	"""
	This function will check input format, and show error massage or result on GUI.
	:param entry_dict: dict{tuple: tkinter Entry object}, same key to alpha_dict.
	:param massage_out: (Tkinter Entry object)
	:param search_out: (Tkinter Text object)
	"""
	# Update massage
	search_out.delete('1.0', 'end')
	massage_out.configure(text='Searching...')
	# Check input
	alpha_dict = {}
	input_error = None
	for k in entry_dict:
		alpha_dict[k] = entry_dict[k].get()
		if len(alpha_dict[k]) != 1 or alpha_dict[k].isalpha() is not True:
			input_error = True
	if input_error:
		massage_out.configure(text='Illegal input, try again.')
	# Start Searching
	else:
		start_time = time.time()
		# load dictionary data
		read_dictionary(list(alpha_dict.values()))
		ans = []
		alpha_used = []
		current_s = ''
		count = []
		find_ans(alpha_dict, alpha_used, current_s, ans, count)

		# Show result in console
		print(f'There are {len(ans)} words in total.')
		print('recursive times:', sum(count))
		end_time = time.time()
		print(f'Time spent: {round(end_time - start_time, 4)} seconds')

		# Show result in GUI
		search_out.delete('1.0', 'end')
		search_out.insert('end', f'Possible words: {len(dictionary)}\n')
		for ele in ans:
			search_out.insert('end', f'Found: {ele}\n')
		search_out.insert('end', f'There are {len(ans)} words in total.\n')
		search_out.insert('end', f'Recursive counts: {sum(count)}\n')
		search_out.insert('end', f'Time spent: {round(end_time - start_time, 4)} seconds\n')


def find_ans(alpha_dict, alpha_used, current_s, ans, count):
	"""
	This function will find answer of boggle game.
	:param alpha_dict: (dict{tuple: str}), a dictionary of coordinate tuple as key, and alpha string as value.
	:param alpha_used: (list[tuple]), coordinate list of alpha used.
	:param current_s: (str), a string for record exhaustive search.
	:param ans: (list[str]), a list for record answer found.
	:param count: (list[int]), sum of the value for count recursive times.
	:return:
	"""
	count.append(1)
	alpha_usable = get_alpha_usable(alpha_dict, alpha_used)
	# base case
	if len(alpha_usable) == 0:
		return
	# recursive case
	else:
		for alpha in alpha_usable:
			# choose
			alpha_used.append(alpha)
			current_s += alpha_dict[alpha]
			if current_s in dictionary and current_s not in ans:
				print(f'Found: "{current_s}"')
				ans.append(current_s)
			# explore(recursive case)
			if has_prefix(current_s):
				find_ans(alpha_dict, alpha_used, current_s, ans, count)
			# un-choose
			alpha_used.pop()
			current_s = current_s[0: -1]


def get_alpha_usable(alpha_dict, alpha_used):
	"""
	This function will return usable alpha, use alpha_used[-1] as current position.
	:param alpha_dict: (dict{tuple: str}), a dictionary of coordinate tuple as key, and alpha string as value.
	:param alpha_used: (list[tuple]), coordinate list of alpha used.
	:return: alpha_usable: (list[tuple]), coordinate list of alpha usable.
	"""
	if len(alpha_used) == 0:
		return list(alpha_dict.keys())
	x = alpha_used[-1][0]
	y = alpha_used[-1][1]
	alpha_neighbor = []
	for j in range(max(1, y-1), min(y+1, SIZE)+1):
		for i in range(max(1, x-1), min(x+1, SIZE)+1):

			if i != x or j != y:
				alpha_neighbor.append((i, j))
	alpha_usable = [ele for ele in alpha_neighbor if ele not in alpha_used]
	return alpha_usable


def is_input_correct(s):
	"""
	This function will check input format.
	:param s: (str) input string
	:return: (bool) if string format correct
	"""
	if len(s) == SIZE*2-1:
		for i in range(len(s)):
			if i % 2 == 0:
				if s[i].isalpha() is not True:
					return False
			if i % 2 == 1:
				if s[i] != ' ':
					return False
		return True
	return False


def read_dictionary(alpha_wanted):
	"""
	This function reads file "dictionary.txt" stored in FILE
	and appends words in each line into a Python list
	:param alpha_wanted: list[str], alphabet wanted, element should be an alphabet.
	"""
	global dictionary
	dictionary = []
	with open(FILE, 'r') as f:
		for line in f:
			word = line.strip()
			if len(word) >= MIN_LETTER and alpha_check(word, alpha_wanted):
				# don't need words short than SIZE and not make up with alpha wanted
				dictionary.append(word)
	print(f'Possible words: {len(dictionary)}')


def alpha_check(word, alpha_wanted):
	"""
	This function will check if every alphabets of word in target_s
	:param word: str, a word want to check alphabets
	:param alpha_wanted: list[str], alphabet wanted, element should be an alphabet.
	:return: bool, if every alphabets of word in target_s
	"""
	for alpha in word:
		if alpha not in alpha_wanted:
			return False
	return True


def has_prefix(sub_s):
	"""
	:param sub_s: (str) A substring that is constructed by neighboring letters on a 4x4 square grid
	:return: (bool) If there is any words with prefix stored in sub_s
	"""
	for word in dictionary:
		if word.startswith(sub_s):
			return True
	return False


if __name__ == '__main__':
	main()
