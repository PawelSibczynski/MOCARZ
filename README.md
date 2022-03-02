# MOCARZ
MOCARZ- MOnte CARlo analyZer

The program converts MCNP F4 average flux tally with histogram flux distribution for a single selected cell to F8 pulse height tally input used for further spectra processing - gaussian broadening and detection efficiency in a cell volume.

The tool also perform gaussian fitting for a MCNP F8 pulse height spectra.


# Required libraries
Install Python version 3.9 (suggested).

Windows: install from Microsoft Store (the fastest way). Advanced users can also install Pyt
Linux: sudo apt install python3.9

To verify installation, type in terminal: python --version

To install required libraries, go to cloned repository and type:
pip install -U requirements.txt


# How to run
To run the application, open Anaconda Prompt or Command Line/Terminal and type:

python main_gui.py

In the application GUI window, you can select the F4 output file names to be converted to F8 input, geometry cell number, and modify importances. 

Your F4 and F8 input structe must follow the schema below (order is extremely important):
1. cells definition
2. surfaces definition
3. materials definition
4. *** Importances ***  (written exactly like this just after materials definition to be detected by software)



Important notices before use!

- please note that the F4 output file name at the end must be exactly equal to '_out.o'.
- check how many columns you have in you F4 average flux histogram output. At this early stage, Prompt states for 1st column, Delayed for 3rd column, Total for 5th column. (TO DO - improve the column selection method)
This parts can be modified in "Geometry importance description" Text Box in GUI:
- the number of importances imp:p must match to the number of active cells in your geometry calculation. (TO DO - automatic match)
- the e8 energy binning must match to the number of energy bins in your geometry problem. (TO DO - automatic match)


This is an early development version.
Your feedback is always welcome!
