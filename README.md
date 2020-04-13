# MCF
MCF - A Monte Carlo n-particle F-tally converter

The program converts MCNP F4 average flux tally with histogram flux distribution for a single selected cell to F8 pulse height tally input used for further spectra processing - gaussian broadening and detection efficiency in a cell volume.

To run the application, open Anaconda Prompt or Command Line/Terminal and type:

python gui_main.py

In the application GUI window, you can select the F4 output file names to be converted to F8 input, geometry cell number, and modify importances. 

Your F4 input (from which you receive F4 output) structe must follow the schema below (respectively):
1. cells definition
2. surfaces definition
3. materials definition
4. *** Importances ***  (written exactly like this just after materials definition)



Important notices before use!

- please note that the F4 output file name at the end must be exactly equal to '_out.o'.
- check how many columns you have in you F4 average flux histogram output. At this early stage, Prompt states for 1st column, Delayed for 3rd column, Total for 5th column. (TO DO - improve the column selection method)
This parts can be modified in "Geometry importance description" Text Box in GUI:
- the number of importances imp:p must match to the number of active cells in your geometry calculation. (TO DO - automatic match)
- the e8 energy binning must match to the number of energy bins in your geometry problem. (TO DO - automatic match)


Feedback is more than welcome! :)
