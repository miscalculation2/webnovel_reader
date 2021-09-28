import os
import tkinter as tk
from tkinter import *

root = Tk()
root.title("editable HTML Reader 9000")

# < --- function to get text from text input, add it to HTML template, and save it in output folder

def runprogram():


	# get text data and clean it
	data = textarea.get("1.0","end")

	if len(data) < 2:
		from tkinter import messagebox
		messagebox.showerror("ERROR", "Input is empty")
	else:
		import re
		split_lines = data.split('\n')
		split_lines = [line for line in split_lines if len(line) > 0]

		new_lines = []
		for line in split_lines:
			line = line.strip(' ')
			line = re.sub(r'^\s{1,}', '', line)
			line = re.sub('　', '', line)
			new_lines.append(line)


	# file name option
	from pathvalidate import is_valid_filename, sanitize_filename

	file_name_opt = filenamearea.get()
	filename = sanitize_filename(file_name_opt)

	if len(filename) < 1:
		filename = 'output'
		error_string = 'ERROR: ' + file_name_opt + ' is not a valid file name.'
		my_string_var.set(error_string)
	else:
		stringmessage = "successfully written file " + str(filename)
		my_string_var.set(stringmessage)


	# add to HTML
	from bs4 import BeautifulSoup
	import pathlib

	with open('reader_template.html', 'r', encoding='utf-8') as g:
		html_doc = g.read()

	soup = BeautifulSoup(html_doc, 'html.parser')
	old_tag = soup.p
	new_tag = soup.new_tag('p')

	for data_line in new_lines:
		new_tag = soup.new_tag('p')
		new_tag.string=data_line
		old_tag.append(new_tag)

	old_sheet = soup.find('link', {'href':'styles/stylesheet.css'})
	old_sheet.decompose()

	new_sheet_tag = soup.new_tag('link')

	new_sheet_tag.attrs['href']='../styles/stylesheet.css'
	new_sheet_tag.attrs['rel']='stylesheet'
	soup.head.insert(0,new_sheet_tag)

	directory = 'output_html/'
	extension = '.html'
	full_filename = filename + extension

	current_directory = str(pathlib.Path(__file__).parent.resolve())
	to_save_directory = os.listdir(current_directory + '/' + directory)
	counter = 0

	soup = soup.prettify()

	while full_filename in to_save_directory:
		full_filename = filename + ' (' + str(counter) + ') ' + extension
		counter += 1
		continue
	to_save_path = str(pathlib.Path(__file__).parent.resolve()) + '/' + directory + full_filename

	with open(to_save_path, 'w', encoding='utf-8') as file:
		file.write(str(soup))

	textarea.delete('1.0', END)
	filenamearea.delete(0, END)


# < --- basic tkinter GUI

my_string_var = StringVar()
my_string_var.set("Paste your copypasta here")

tk.Label(root, textvariable =my_string_var).grid(column=2, row=2, sticky=(W, E), padx=5, pady=5)
textarea = tk.Text(root, height=10, width=40)
textarea.grid(column=2, row=4, sticky=(W, E), padx=5, pady=5)
tk.Label(root, text="file name").grid(column=2, row=6, sticky=(W), padx=5, pady=5)
filenamearea = tk.Entry(root, width=40)
filenamearea.grid(column=2, row=8, sticky=(W), padx=5, pady=5)
tk.Button(root, text="submit", command=runprogram).grid(column=2, row=10, sticky=(W, E), padx=5, pady=5)

root.mainloop()