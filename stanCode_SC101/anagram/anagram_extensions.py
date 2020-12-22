"""
File: anagram.py
Name: Danny Tsai
----------------------------------
This program recursively finds all the anagram(s)
for the word input by user and terminates when the
input string matches the EXIT constant defined
at line 19

If you correctly implement this program, you should see the
number of anagrams for each word listed below:
    * arm -> 3 anagrams
    * contains -> 5 anagrams
    * stop -> 6 anagrams
    * tesla -> 10 anagrams
    * spear -> 12 anagrams
"""
import time
import tkinter as tk

# Constants
FILE = 'dictionary.txt'       # This is the filename of an English dictionary

# Global variable
dictionary = []               # List of dictionary load from txt


def main():
    """
    This function will make a GUI for Anagram Generator.
    """
    # Make GUI
    top = tk.Tk()
    top.title('stanCode "Anagram Generator"')
    make_gui(top)
    top.mainloop()


def make_gui(top):
    """
    Set up the GUI elements for Anagram Generator.
    :param top: (Tkinter object): The main window of GUI.
    """
    label = tk.Label(top, text='Type a word and press enter to find anagram:', font=18)
    label.grid(row=0, column=0, sticky='w')
    search_entry = tk.Entry(top, width=50, name='search_entry')
    search_entry.grid(row=1, column=0, sticky='w')
    search_entry.focus()

    label_out = tk.Label(top, text='Anagrams will show below:', font=18)
    label_out.grid(row=2, column=0, sticky='w')
    search_out = tk.Text(top, height=30, width=50, name='search_out')
    search_out.grid(row=3, column=0, sticky='w')

    search_entry.bind("<Return>", lambda event: handle_anagram_search(search_entry, search_out))
    top.update()


def handle_anagram_search(search_entry, search_out):
    """
    This function will called by return event of entry field,
    search anagram and show on text field.
    :param search_entry: (Tkinter Entry object)
    :param search_out: (Tkinter Text object)
    """
    target_s = search_entry.get().strip()
    start_time = time.time()
    target_s = target_s.lower()
    read_dictionary(target_s)
    ans, count = find_anagrams(target_s)
    end_time = time.time()
    print(f'Time spent: {round(end_time - start_time, 4)} seconds')
    # Show result on GUI
    search_out.delete('1.0', 'end')
    search_out.insert('end', f'Possible words: {len(dictionary)}\n')
    for ele in ans:
        search_out.insert('end', f'Found: {ele}\n')
    search_out.insert('end', f'\nTotal {len(ans)} anagrams found\n')
    search_out.insert('end', f'Recursive counts: {sum(count)}\n')
    search_out.insert('end', f'Time spent: {round(end_time - start_time, 4)} seconds')


def read_dictionary(target_s):
    """
    This function will load data from txt file,
    and change value of global variable dictionary.
    :param target_s: str, a word want to find anagrams.
    """
    global dictionary
    dictionary = []
    with open(FILE, 'r') as f:
        for line in f:
            word = line.strip()
            if len(word) == len(target_s) and alpha_check(word, target_s):
                dictionary.append(word)
    print(f'Possible words: {len(dictionary)}')


def alpha_check(word, target_s):
    """
    This function will check if every alphabets of word in target_s
    :param word: str, a word want to check alphabets
    :param target_s: str, a string of alphabet wanted.
    :return: bool, if every alphabets of word in target_s
    """
    for alpha in word:
        if alpha not in target_s:
            return False
    return True


def find_anagrams(s):
    """
    This function will set variable for find anagrams.
    :param s: str, a word want to find anagrams.
    :return ans: list[str], a list for record anagrams found
    :return count: list[int], sum of the value for count recursive times.
    """
    ans = []
    count = []
    print('Searching...')
    find_anagrams_helper(s, '', ans, count)
    print(f'{len(ans)} anagrams: {ans}')
    print(f'recursive times: {sum(count)}')
    return ans, count


def find_anagrams_helper(s, current_s, lst, count):
    """
    This function will help find_anagrams function find out anagrams.
    :param s: str, a word want to find anagrams.
    :param current_s: str, a string for record exhaustive search.
    :param lst: list[str], a list for record anagrams found.
    :param count: list[int], sum of the value for count recursive times.
    """
    count.append(1)
    if len(s) == 0:
        if current_s in dictionary and current_s not in lst:
            lst.append(current_s)
            print(f'Found: {current_s}')
            print('Searching...')
    else:
        for i in range(len(s)):
            # choose
            current_s += s[i]
            unused_s = s[0:i]+s[i+1:len(s)]
            # explore(recursive case)
            if has_prefix(current_s):
                find_anagrams_helper(unused_s, current_s, lst, count)
            # un-choose
            current_s = current_s[0:-1]


def has_prefix(sub_s):
    """
    This function will search dictionary by sub_s,
    control early stop of exhaustive search.
    :param sub_s: str, a string want to search in dictionary.
    :return: bool, whether or not a word start with sub_s in dictionary.
    """
    for word in dictionary:
        if word.startswith(sub_s):
            return True
    return False


if __name__ == '__main__':
    main()
