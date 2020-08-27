import pandas as pd
import os


class Converter():
    def __init__(self):
        print("MCF backend initalized.")
        self.file_to_write = ""
        pass

    def getImportancesStr(self, cellNum):
        '''
        Get a standard F8 tally importance card template. 
        Parameters need to be checked and eventually corrected by user.
        '''
        self.s =   "\
imp:p   1 12r 0                $ importances in cells for photons \n\
c ----- \n\
c F8 processing - FWHM \n\
c ----- \n\
sdef cel="+cellNum+" pos=24 -54 0 rad=d1 par=2 erg=d2    $ source definition  \n\
F8:p 2 \n\
e8 0 1099i 11                  $ energy bins \n\
FT8 GEB 2.00E-04 2.20E-02 0.5  $ FWHM \n\
si1 0 8                        $ radius \n\
"
        return self.s

    def F4toF8(self, fileList, setCellNum, setImportaces, F4column):
        ''' read F4 tally based MCNP file content, convert it to F8 and save to new file.
        Returns F4 energy spectrum as pandas dataframe 
        fileList - a list of F4 output files to convert
        setCellNum - cell number (i.e. detector cell) data to convert, taken from F4
        setImportances - Importances and source definition from GUI textbox. It is a basic settings,
        currently must be adapt by end user.
        F4column - an F4 spectrum distribution column output to be converted.
        '''
        
        InputCode = []
        spec_tab = []

        for f in fileList[0]:
            file = open(f, "r+")
            basepath = os.path.dirname(f)

            try:
                g = os.path.basename(f)
                if not os.path.exists(basepath+"/F8/"):
                    os.mkdir(basepath+"/F8/")
                    print("Folder F8 created.")
                file_to_write = open(basepath+"/F8/"+g.replace("F4", "F8").replace('_out.o', '.m'), "w")
            except IOError as e:
                print("Error during creation of F8 file", e)

            data = file.readlines()


            starter = 0
            specRead = False # do not read spectrum intil source input writing to file
            lineCount = 0
            stopInpCode = 0

            # writing source code until IMPORTANCES appears in line
            for line in data:
                if line.__contains__("probid") and line[1:6] == '*****':
                    starter = 1
                    print("Start input reading...")
                
                if starter == 1 and lineCount >= 1:
                    if len(line) > 8 and line[10].__contains__('-') and line[9].isdigit():
                        InputCode.append(line[18:])
                        line.replace("\t", " ")  # remove all tabs in file
                        if line.__contains__("*** Importances ***"):
                            line.replace("\n", "")
                            file_to_write.writelines(InputCode)
                            break # stop writing code when you find IMPORTANCES in source code
                
                lineCount = lineCount + 1  


            if line.__contains__("*** Importances ***"):
                Imp = True
                InputCode = []
                print("Start Importances taking from GUI...")
                file_to_write.writelines(setImportaces)


            for line in data:
                if line.__contains__("cell  "+str(setCellNum)):
                    specRead = True
                    specLineNo = 0
                    print("Start spectra reading, start at line number:", lineCount)

                if specRead == True:
                    specLineNo = specLineNo + 1
                    if specLineNo > 3 and specLineNo < 1105:  # to do: automatically assign number of bins
                        specLine = line
                        specLine.replace('\t', ' ')
                        specLine = specLine.split()
                        spec_tab.append(specLine)



            df = pd.DataFrame(spec_tab, columns=['Energy', 'Prompt', 'Prompt_err', 'Delayed', 'Delayed_err', 'Total', 'Total_err'])
            df["Delimiter"] = '&'
            df = df[['Energy', 'Delimiter', 
                     'Prompt', 'Prompt_err', 
                     'Delayed', 'Delayed_err', 
                     'Total', 'Total_err']]
            
            return df



            def _axisToMCInput(df, mcColumn):
                '''build input data from F4 out to F8 input. Function must be run twice:
                First time for E=energy, second time for histogram data
                '''
                energy = df.loc[:, mcColumn]
                delim = df.loc[:, 'Delimiter']
                delim[-1:] = ""
                axis = energy+" "+delim
                axis = list(axis)
                return axis

            axisX = _axisToMCInput(df, "Energy")
            axisY = _axisToMCInput(df, F4column)


            for row, i in enumerate(axisX):
                if row == 0:
                    file_to_write.writelines("si2 A &\n")
                file_to_write.writelines(str(i)+"\n")

            for row, j in enumerate(axisY):
                if row == 0:
                    file_to_write.writelines("sp2 &\n")
                file_to_write.writelines(str(j)+"\n")


            file_to_write.writelines("nps 1E8\n")
            file_to_write.writelines("print 110\n")
            print("File converted successfully.\n")



            # Zero all counters
            starter = 0
            specRead = 0
            lineCount = 0
            spec_tab = []


            file_to_write.close()

