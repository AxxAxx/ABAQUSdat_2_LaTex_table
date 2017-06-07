#-------------------------------------------
# Script to automatically read in the eigenfrequency 
# data from a ABAQUS .dat file and convert it to  
# LaTex code. The code created is used to create tables for 
# the ABB Technical report. 
#
# Version 1.0 - Initial version - Axel Johansson 2016-07-02
#-------------------------------------------

import tkinter as tk
from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
from tkinter import filedialog
from math import floor

class Application(tk.Frame):
	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		self.grid()
		self.createWidgets()

	def createWidgets(self):
	
		# Availibility to include ABB logo to the GUI, this feature requires the image file to be placed in the 
		# same folder. This feature is therefore commented to be able to run the program without requiring other files. 
		#self.logo = tk.PhotoImage(file="abb.gif")
		#self.logotype = tk.Label(self, image=self.logo)
		#self.logotype.grid(row=30, column=0, sticky=tk.W, pady=(0,10))
	
		# Create GUI text
		tk.Label(self, text = " ").grid(row=0, column=0)
		tk.Label(self, text = "Path to ABAQUS .dat file:").grid(row=1, column=0,sticky=tk.W)
		tk.Label(self, text = "Specify number of eigevalues or scan file").grid(row=2, column=0,sticky=tk.W)
		tk.Label(self, text = "Output LOG").grid(row=7, column=0,sticky=tk.W)
		tk.Label(self, text = "Ctrl-A + Ctrl-C to copy formatted LaTex code").grid(row=19, column=0, columnspan=3,sticky=tk.W )
		
		tk.Label(self, text = "Axel.Johansson@se.abb.com").grid(row=32, column=0,sticky=tk.W)

		# Create GUI Buttons	
		self.hi_there = tk.Button(self)
		self.hi_there["text"] = "Specify ABAQUS .dat file path"
		self.hi_there["command"] = self.say_hi
		self.hi_there.grid(row=1, column=2,sticky=tk.W,padx=(10,10))
		
		self.latexpath_button = tk.Button(self)
		self.latexpath_button["text"] = "Scan ABAQUS .dat file"
		self.latexpath_button["command"]= self.scan_file_for_eigvalues
		self.latexpath_button.grid(row=2, column=2,sticky=tk.W,padx=(10,10))

		self.ConvertButton = tk.Button(self)
		self.ConvertButton["text"] = "Create LaTex table!"
		self.ConvertButton["font"] = "-weight bold"
		self.ConvertButton["command"]= command=self.convert
		self.ConvertButton["bg"] = "green"
		self.ConvertButton.grid(row=5, column=1, rowspan=2, pady=(10,10))

		self.RadioButtonValue_MassUnit = IntVar()
		self.MakeAppendix = tk.Radiobutton(self, text="Mass unit: 10^3 kg", variable=self.RadioButtonValue_MassUnit, value=1).grid(row=3, column=0, pady=(0,0),sticky=tk.W+tk.S)
		self.MakeAppendix = tk.Radiobutton(self, text="Mass unit: kg", variable=self.RadioButtonValue_MassUnit, value=2).grid(row=4, column=0, pady=(0,0),sticky=tk.W+tk.N)
		self.RadioButtonValue_MassUnit.set(1)
		
		
		self.RadioButtonValue = IntVar()
		self.MakeAppendix = tk.Radiobutton(self, text="Complete LaTex Appendix", variable=self.RadioButtonValue, value=1).grid(row=3, column=1, pady=(0,0),sticky=tk.W+tk.S)
		self.MakeAppendix = tk.Radiobutton(self, text="Simple LaTex table", variable=self.RadioButtonValue, value=2).grid(row=4, column=1, pady=(0,0),sticky=tk.W+tk.N)
		self.RadioButtonValue.set(1)
			
		
		self.QUIT = tk.Button(self, text="Exit",font="-weight bold", command=root.destroy)
		self.QUIT.grid(row=31, column=2,sticky=tk.W, padx=(10,10))
		
		self.QUIT = tk.Button(self, text="Clear Output",font="-weight bold", command=self.clear_output)
		self.QUIT.grid(row=31, column=1,sticky=tk.W, padx=(10,10))
		

		self.datpath = tk.Entry(self)
		self.datpath.grid(row=1, column=1)

		self.number_of_eigValues = tk.Entry(self)
		self.number_of_eigValues.grid(row=2, column=1)
		
		self.outputTextBox = tk.Text(self, width=50, height=10)
		self.outputTextBox.grid(row=8, column=0, columnspan=3, rowspan=10,sticky=tk.E+tk.W+tk.S+tk.N, padx=(5,5), pady=(0,10))
		
		self.ResultOutputTextBox = tk.Text(self, width=50, height=10)
		self.ResultOutputTextBox.grid(row=20, column=0, columnspan=3, rowspan=10,sticky=tk.E+tk.W+tk.S+tk.N, padx=(5,5), pady=(0,10))
		
	def convert(self):
	
		EigenNumber=[]
		EigenFreq=[]
		EigenEffMassX=[]
		EigenEffMassY=[]
		EigenEffMassZ=[]
		try:
			Number_of_scanned_eigenvalues=int(self.number_of_eigValues.get())
		except:
			self.outputTextBox.insert(tk.END, 'You have to specify number of eigenmodes! \n')

		EigenOutputLine=0
		EffectiveMassLine=0
		LineCounter=9999

		try:
			DatFile = open(root.filename, "r")
		except:
			self.outputTextBox.insert(tk.END, 'You have to specify an ABAQUS .dat path!\n')
			
		for line in DatFile:
			LineCounter=LineCounter+1
			if "E I G E N V A L U E    O U T P U T" in line: 
				#print('EIGENVALUE OUTPUT FOUND!')
				self.outputTextBox.insert(tk.END, 'EIGENVALUE OUTPUT FOUND!\n')
				#self.outputTextBox.insert(tk.END,Number_of_scanned_eigenvalues)
				EigenOutputLine=LineCounter
			if LineCounter>=EigenOutputLine+6 and LineCounter<=EigenOutputLine+5+Number_of_scanned_eigenvalues:
				EigenNumber.append(line.split()[0])
				EigenFreq.append(line.split()[3])
			
			if "E F F E C T I V E   M A S S" in line: 
				#print('EFFECTIVE MASS FOUND!\n')
				self.outputTextBox.insert(tk.END, 'EFFECTIVE MASS FOUND!\n')

				EffectiveMassLine=LineCounter
			if LineCounter>=EffectiveMassLine+4 and LineCounter<=EffectiveMassLine+3+Number_of_scanned_eigenvalues:
				EigenEffMassX.append(line.split()[1])
				EigenEffMassY.append(line.split()[2])
				EigenEffMassZ.append(line.split()[3])
		
		if self.RadioButtonValue.get() == 1:
			self.ResultOutputTextBox.insert(tk.END, '\\section*{APPENDIX A. Full list of eigenfrequencies and their effective mass}')
			self.ResultOutputTextBox.insert(tk.END, '\n')
			self.ResultOutputTextBox.insert(tk.END, '\\label{Full_list_eigenfrequencies}')
			self.ResultOutputTextBox.insert(tk.END, '\n')
			self.ResultOutputTextBox.insert(tk.END, '\\addcontentsline{toc}{subsection}{A. Full list of eigenfrequencies}')
			self.ResultOutputTextBox.insert(tk.END, '\n')
		
		if int(self.number_of_eigValues.get())< 37:
			self.StartTable(1,self.number_of_eigValues.get())
		else:
			self.StartTable(1,36)


		PrintOutIndex = 0
		for index in range (0,Number_of_scanned_eigenvalues):
			PrintOutIndex += 1 
			self.ResultOutputTextBox.insert(tk.END, EigenNumber[index])
			self.ResultOutputTextBox.insert(tk.END, ' & ')
			self.ResultOutputTextBox.insert(tk.END, EigenFreq[index])
			self.ResultOutputTextBox.insert(tk.END, ' & ')
			self.ResultOutputTextBox.insert(tk.END, EigenEffMassX[index])
			self.ResultOutputTextBox.insert(tk.END, ' & ')
			self.ResultOutputTextBox.insert(tk.END, EigenEffMassY[index])
			self.ResultOutputTextBox.insert(tk.END, ' & ')
			self.ResultOutputTextBox.insert(tk.END, EigenEffMassZ[index])
			self.ResultOutputTextBox.insert(tk.END, ' \\\\')
			self.ResultOutputTextBox.insert(tk.END, '\n')
		
			if PrintOutIndex==36:
				self.EndTable()
				self.ResultOutputTextBox.insert(tk.END, '\n')
				self.ResultOutputTextBox.insert(tk.END, '\n')
				self.StartTable(37,80)
			
			#print(floor(PrintOutIndex-34)/46)
			#print((PrintOutIndex-34)/46)
			if PrintOutIndex>36:
				if floor((PrintOutIndex-34)/46)==((PrintOutIndex-34)/46):
					self.EndTable()
					self.ResultOutputTextBox.insert(tk.END, '\n')
					self.ResultOutputTextBox.insert(tk.END, '\n')
					if PrintOutIndex+46>int(self.number_of_eigValues.get()):
						self.StartTable(PrintOutIndex+1,int(self.number_of_eigValues.get()))
					else:
						self.StartTable(PrintOutIndex+1,PrintOutIndex+46)
				
		
		if self.RadioButtonValue.get()==1:
			self.scan_file_for_total()
		
		
		self.outputTextBox.insert(tk.END, '\nConvertion DONE !! \n')
			
		self.EndTable()


		DatFile.close()
		
	def say_hi(self):
		root.filename =  filedialog.askopenfilename(title = "Choose your ABAQUS .dat file",filetypes = (("ABAQUS .dat files","*.dat"),("all files","*.*")))
		self.datpath.insert(0, root.filename)
		self.outputTextBox.insert(tk.END, 'File path sucessfully specified\n')

	def scan_file_for_eigvalues(self):
		try:
			DatFile = open(root.filename, "r")
			#print('opened')
			Lines=DatFile.read().splitlines()
			#print('Lines splitted')

		except:
			self.outputTextBox.insert(tk.END, 'You have to specify an ABAQUS .dat path!\n')
			print('Failed to open')
		for i_temp, line in enumerate(Lines):
			if "TOTAL    " in line: 
				self.number_of_eigValues.delete(0, 'end')
				number_of_eigenvalues_variable=Lines[i_temp-2].split()[0]
				self.number_of_eigValues.insert(tk.END, number_of_eigenvalues_variable)
				#print(Lines[i_temp-2].split()[0])
				self.outputTextBox.insert(tk.END, 'Number of eigenvalues found: ')
				self.outputTextBox.insert(tk.END, number_of_eigenvalues_variable)
				self.outputTextBox.insert(tk.END, '\n')

		DatFile.close()
		
	
	def clear_output(self):
		self.outputTextBox.delete('1.0', 'end')
		self.ResultOutputTextBox.delete('1.0', 'end')

	def scan_file_for_total(self):
		try:
			DatFile = open(root.filename, "r")
		except:
			self.outputTextBox.insert(tk.END, 'You have to specify an ABAQUS .dat path!\n')
		
		for line in DatFile:
			if "TOTAL      " in line: 
				self.ResultOutputTextBox.insert(tk.END, ' & ')
				self.ResultOutputTextBox.insert(tk.END, '\\textbf{TOTAL}')
				self.ResultOutputTextBox.insert(tk.END, ' & \\textbf{')
				self.ResultOutputTextBox.insert(tk.END, line.split()[1])
				self.ResultOutputTextBox.insert(tk.END, '} & \\textbf{')
				self.ResultOutputTextBox.insert(tk.END, line.split()[2])
				self.ResultOutputTextBox.insert(tk.END, '} & \\textbf{')
				self.ResultOutputTextBox.insert(tk.END, line.split()[3])
				self.ResultOutputTextBox.insert(tk.END, '} \\\\')
				self.ResultOutputTextBox.insert(tk.END, '\n')
		DatFile.close()

	def EndTable(self):
		self.ResultOutputTextBox.insert(tk.END, '\\bottomrule')
		self.ResultOutputTextBox.insert(tk.END, '\n')
		self.ResultOutputTextBox.insert(tk.END, '\\end{tabular}')
		self.ResultOutputTextBox.insert(tk.END, '\n')
		self.ResultOutputTextBox.insert(tk.END, '\\label{tab:addlabel}')
		self.ResultOutputTextBox.insert(tk.END, '\n')
		self.ResultOutputTextBox.insert(tk.END, '\\end{table}')
	
	def StartTable(self, start, stop):
		self.ResultOutputTextBox.insert(tk.END, '\\begin{table}[htbp]')
		self.ResultOutputTextBox.insert(tk.END, '\n')
		self.ResultOutputTextBox.insert(tk.END, '\\small')
		self.ResultOutputTextBox.insert(tk.END, '\n')
		self.ResultOutputTextBox.insert(tk.END, '\\centering')
		self.ResultOutputTextBox.insert(tk.END, '\n')
		self.ResultOutputTextBox.insert(tk.END, '\\caption{Eigenfrequencies ')
		self.ResultOutputTextBox.insert(tk.END, start)
		self.ResultOutputTextBox.insert(tk.END, '-')
		self.ResultOutputTextBox.insert(tk.END, stop)
		self.ResultOutputTextBox.insert(tk.END, '}')
		self.ResultOutputTextBox.insert(tk.END, '\n')
		self.ResultOutputTextBox.insert(tk.END, '\\begin{tabular}{rrrrr}')
		self.ResultOutputTextBox.insert(tk.END, '\n')
		self.ResultOutputTextBox.insert(tk.END, '\\toprule')
		self.ResultOutputTextBox.insert(tk.END, '\n')
		self.ResultOutputTextBox.insert(tk.END, 'Mode nr. & Frequency [Hz] & \multicolumn{3}{c}{Effective mass [')
		if self.RadioButtonValue_MassUnit.get() == 1:
			self.ResultOutputTextBox.insert(tk.END, '10\\textsuperscript{3} ')
		self.ResultOutputTextBox.insert(tk.END,'kg]} \\\\')
		self.ResultOutputTextBox.insert(tk.END, '\n')
		self.ResultOutputTextBox.insert(tk.END, '\\midrule')
		self.ResultOutputTextBox.insert(tk.END, '\n')
		self.ResultOutputTextBox.insert(tk.END, '      &       & X-COMPONENT & Y-COMPONENT & Z-COMPONENT \\\\')
		self.ResultOutputTextBox.insert(tk.END, '\n')
				
root = tk.Tk()
root.wm_title("ABAQUS 2016 Seismic Modes to LaTex Table Converter")
root.resizable(0,0)
app = Application(master=root)
app.mainloop()
