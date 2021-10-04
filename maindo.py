from tkinter import *
import tkinter as tk
import re

root = Tk()
root.title("bullet list converter")


def runprogram():
	# get data from text input
	data = textarea.get("1.0","end")

	# split data in lines (code for filtering out empty lines does not work cuz I'm dumb)
	split_data = data.split('\n')
	split_data = [dataline for dataline in split_data if len(dataline) > 0]

	# initialize empty list that will be used to append new lines to
	new_data = []

	# tags 
	first_tag_start = '<step>\n<cmd>'
	first_tag_end = '</cmd>\n</step>'
	second_tag_start = '<substep>\n<cmd>'
	second_tag_end = '</cmd>\n</substep>'

	# check if line is step, substep or something else, remove bullet list items, and add tags to it
	for line in split_data:
		if '•	' in line:
			filtered_line = re.sub('•	', '', line)
			# if option toggled on: remove whitespace from line
			if var1.get():
				filtered_line = re.sub(r'\s{1,}$', '', filtered_line)
			final_line = first_tag_start + filtered_line + first_tag_end
			new_data.append(final_line)

		elif 'o	' in line:
			filtered_line = re.sub('o	', '', line)
			# if option toggled on: remove whitespace from line
			if var1.get():
				filtered_line = re.sub(r'\s{1,}$', '', filtered_line)
			final_line = second_tag_start + filtered_line + second_tag_end
			new_data.append(final_line)
		else:
			line = re.sub(r'\s{1,}$', '', line)
			final_line = '<draft-comment>' + line + '</draft-comment>'
			new_data.append(final_line)

	# code to add <substeps></substeps>
	echo = ''
	true_data = []
	new_data_len = len(new_data)-1

	for line, index in zip(new_data, enumerate(new_data)):
		is_step = re.match(r'^<step>\n.+\n</step>$', line)
		is_substep = re.match(r'^<substep>\n.+\n</substep>$', line)

		if index[0] == new_data_len and is_substep:
			if echo == 'step':
				line = '<substeps>\n' + line + '\n</substeps>'
				true_data.append(line)
			else:
				line = line + '\n</substeps>'
				true_data.append(line)

		elif is_step:
			if echo == 'substep':
				line = '</substeps>\n' + line
			echo = 'step'
			true_data.append(line)

		elif is_substep:
			if echo == 'step':
				line = '<substeps>\n' + line
			echo = 'substep'
			true_data.append(line)
		else:
			true_data.append(line)

	# turn back final list into string and add <steps></steps> to it
	final_data = '\n'.join(true_data)
	final_data = '<steps>\n' + final_data + '\n</steps>'

	# insert string in output area
	outputarea.config(state=NORMAL)
	outputarea.delete('1.0',END)
	outputarea.insert(END, final_data)
	outputarea.config(state=DISABLED)

	# copy output to clipboard if option is toggled on
	if var2.get():
		root.clipboard_clear()
		root.clipboard_append(final_data)

# code for clear button: clear fields' input and output
def clearfields():
	outputarea.config(state=NORMAL)
	outputarea.delete('1.0',END)
	outputarea.config(state=DISABLED)
	textarea.delete('1.0', END)


# GUI area
my_string_var = StringVar()
my_string_var.set("Paste your input here")
var1 = IntVar()
var2 = IntVar()

tk.Label(root, textvariable =my_string_var).grid(column=2, row=2, sticky=(W, E), padx=5, pady=5)
textarea = tk.Text(root, height=10, width=40)
textarea.grid(column=2, row=4, sticky=(W, E), padx=5, pady=5)

tk.Label(root, text="output in pseudo XML").grid(column=2, row=6, sticky=(W), padx=5, pady=5)
outputarea = tk.Text(root, height=10, width=40)
outputarea.grid(column=2, row=8, sticky=(W), padx=5, pady=5)

tk.Button(root, text="submit", command=runprogram).grid(column=2, row=10, sticky=(W, E), padx=5, pady=5)
tk.Button(root, text="clear", command=clearfields).grid(column=2, row=12, sticky=(W, E), padx=5, pady=5)
tk.Checkbutton(root, text="remove end-of-line whitespace", variable=var1).grid(column=2, row=14, sticky=(W, E))
tk.Checkbutton(root, text="copy output to clipboard", variable=var2).grid(column=2, row=16, sticky=(W, E))

root.mainloop()