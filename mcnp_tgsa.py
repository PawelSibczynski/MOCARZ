# Code developed by Pawel Sibczynski, mcnp_TGSA_v1.22
import textwrap as txtw
import os
import numpy as np
import pandas as pd
from PySide2 import QtWidgets
from PySide2.QtWidgets import (QApplication, QFileDialog, QProgressBar, QLineEdit)
# from GUI_main import Interactions
# import Tkinter as tk
import sys
import time
import matplotlib.pyplot as plt

if sys.version_info[0] < 3:
#    from tkinter import *
#    import tkFileDialog as filedialog
    print("Python V2.X used. Possible incompatibilites.")
else:
    from tkinter import filedialog
    from tkinter import *


from scipy.optimize import curve_fit
from numpy import trapz
import peakutils as pk
from math_mcnp import Gauss_fitting   # import mathemathics from my separately created file

#----
#---- Constant parameters
#----

#global header_text
#header_text = "XXX"

data_raw = [65536]
final_data = []

#Initial parameters
# cell_name = 'cell  2'
data_bins_number = 1100 # pierwotnie 1100, +1
# column_set = 5
# source_rate = 3.5E7*15
# source_rate = 3E8*100
# source_rate = 1E8*100 # max 1.6E8

list_of_elements = ['H', 'C', 'O', 'Si', 'S', 'Cl']

#aid_header = txtw.TextWrapper()
#aid_header = txtw.dedent("channels: "+str(data_bins_number+1)+";\nrealtime: 120.000000;\nlivetime: 120.000000;\ncalib: -1;\n")


# --- LaBr3 - for fitting with averaging
Si_peak = 178
Cl_peak_low = 212
S_peak = 223
H_peak = 223
C_peak = 444
Cl_peak = 612
O_peak = 613
N_peak = 1083

# spread_Si = 9
# spread_Cl_low = 7
# spread_S = 7
spread_H = 11
spread_C = 12
spread_Cl = 14
spread_O = 13
spread_N = 15


# --- BGO spreads ---
# spread_Si = 22
# spread_H = 22
# spread_C = 28
# spread_O = 33


# -----------------
# ---- END constant parameters
# -----------------


#dataset = openfiledialog_dataset()
#print(dataset)
#class APP()

class My_Files(Gauss_fitting):
    def __init__(self):
        self.df_store_data = pd.DataFrame()

    def RAW_DATA_SELECT(self, listoffiles):
        data = 1
        return data
    
    def read_json_peak_data(self):
        try:
            df = pd.read_json('peak_data.json')
            df['Element_index'] = df['Element'] + '_' + df['Peak'].astype(str)
            df = df.set_index('Element_index')
            print(df)
            return df
        except FileNotFoundError as E:
            print('JSON data file was not found!', E)
            return
        except:
            print('Other error when loading peak_data.json file.')
            return

    def fit_gaussian_peak(self, peak_energy, left_marker, right_marker):
        pass

#    def Open_file_F8(self, cell_name):
    def Open_file_F8(self):     # działa z PyQT5
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
#        list_of_files_F8 = filedialog.askopenfilenames(filetypes = ((".o output files","*.o"),
#           ("all files","*.*")))
        list_of_files_F8, _ = QFileDialog.getOpenFileNames(None, "QFileDialog.getOpenFileNames()", "", "Output files (*.o);;All Files (*)", options=options)
     #   print(str(list_of_files_F8))
        return list_of_files_F8

  #  def Open_file_F4(self, cell_name):
    def Open_file_F4(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
#        list_of_files_F4 = filedialog.askopenfilenames(filetypes = ((".o output files","*.o"),
#           ("all files","*.*")))
        list_of_files_F4, _ = QFileDialog.getOpenFileNames(None, "QFileDialog.getOpenFileNames()", "", "Output files (*.o);;All Files (*)", options=options)
        return list_of_files_F4

    def Open_file_F4xF8(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
#        list_of_files_F4 = self.Open_file_F4(cell_name)
#        list_of_files_F8 = self.Open_file_F8(cell_name)
        list_of_files_F4, _ = QFileDialog.getOpenFileNames(None, "QFileDialog.getOpenFileNames()", "", "Output files (*.o);;All Files (*)", options=options)
        list_of_files_F8, _ = QFileDialog.getOpenFileNames(None, "QFileDialog.getOpenFileNames()", "", "Output files (*.o);;All Files (*)", options=options)
        full_list = np.column_stack((list_of_files_F4, list_of_files_F8))
        full_list = np.array(full_list)
        print(full_list)
        return full_list

    # ------------------------------------------
    # ------------ analyse files ---------------
    # ------------------------------------------

    # ------------------------------
    #  --- PULSE HEIGHT ANALYSIS ---
    # ------------------------------

    def Analyse_File_F8(self, file_path, cell_name, source_rate='1E8*1', f4_integral=1):
        # c = My_Files() #instancja klasy My_Files
        df_peak_data = self.read_json_peak_data()
        print(df_peak_data)


        # cell_name = self.Window.lineEdit.text() #self.LINE_EDIT_CELL()   # pobiera tekst z textboxa
        # w funkcji stworzyłem instancję klasy wewnątrz tej samej klasy, po to
        # aby zaimportować metodę tej klasy do tej metody
        #source_rate = self.SET_SOURCE_RATE()
        #f4_integral = self.GET_F4_INTEGRAL()
        source_rate = Gauss_fitting.SR_CONVERT(self, source_rate) * f4_integral
        line_no = 0
        

        #listoffiles = c.Open_file_F8() # listoffiles = self.Open_file_F8 - tak było wcześniej

        # max_file = len(listoffiles)

        energy = []
        counts = []

#        global header_text
#        header_text = "test headrr"

#        listoffiles = filedialog.askopenfilenames()
        # initial directory
        #file_path = 0
     
        log_output_data = 0
        log_output_data_str = 0
        i = 0
        j = 0

        no_of_files = 1
        #for m in listoffiles:
#        try:
        # self.PROGRESS(no_of_files/max_file*100) # to działa! Ponieważ przez self dostajesz się do poziomu nadrzędnego.
        # Ważne: w klasie interactions masz klasę Analyse_File_F8 z self,
        # które daje Tobie możiwość nawiązania kontaktu miedyz tymi obiktami
        #no_of_files += 1
        
#        self.progress()  # progress po analizowanej zawartości pliku. A ja chcę po liście plików!
        # file_path = m
        file_name = os.path.basename(file_path)
        print(file_name)
        

        directory_path = os.path.dirname(file_path)

        #   READ MCNP FILE
        f = open(file_path, "r")

        output_file_name = file_name.replace(".o", "_") + "_sorted_" + str(cell_name.replace("  ", "__")) + ".out"
        output_file_destination = directory_path + "/" + output_file_name

        

#           --- bins calculation ---
        dataset = f.readlines()
        bins_total = Gauss_fitting.bin_calculator(self, dataset, cell_name)
        print("Bins total: " + str(bins_total))
#           ------------------------

        #   WRITE OUTPUT FROM MCNP
        g = open(output_file_destination, "w")
        #            g.write(header_text)

        # read number of header lines
        # with open(output_file_destination) as out:
        #    for header_line_no, l in enumerate(out):
        #        pass
        #    header_line_no = header_line_no + 1

        #    input_file = file.read(open_input_file)

        #            g.write("test"+"\n")  # dziala
#           g.write(self.header_description.get("1.0", END))
#           header_line_count = int(self.header_description.index('end-1c').split('.')[0])  # returns line count
        # print(header_line_count)



#          bins_total = Gauss_fitting.bin_calculator(f, cell_name)

        # aid_file.write(aid_header)

#        for line in f:
        print(dataset)

        line_no = 0  # previously 0  -  this is start line in output file
        for line in dataset:
            if 'cell  '+str(cell_name) in line:
                start_line = line_no
                new_output_list = []
                log_data = []

                output_data = dataset[start_line + 2:start_line + bins_total + 2]

                print(output_data)

                for line in output_data:
                    print(line)
                    new_output_list.append([float(elem) for elem in line.split()])
                    
                data_array = np.asarray(new_output_list)

            #       print(new_array)
                print(output_data[bins_total-1])

                for i in range(bins_total):
                    val = new_output_list[i][1]  # dostęp do elementu listy w liście 
                    if val == 0: #'0.00000E+00':
                        log_data.append(1E-10)
                    else:
                        log_data.append(val)
                    

                data_array_log = np.column_stack((data_array[:, 0], data_array[:, 1], log_data, data_array[:, 2]))
                print(data_array_log) # works well

                df = pd.DataFrame(data_array_log, columns=['E (MeV)', 'Counts', 'Counts(log)', 'Error(%)'])
                df = df.astype(float)
                print(df.values)


                # g.write(str(output_data[0]) + "  " + str(output_data[1]) + " " + str(log_output_data_str) + " " + str(output_data[2]) + " " + "\n")
                
                # data_sqrt = np.sqrt(float(output_data[1])*source_rate)




                np.savetxt(output_file_destination, df.values, fmt='%1.8f')

            line_no = line_no + 1
            
        f.close()
        g.close()

        print('Columns type: int, float, float')


        ############################################
        ### Peak fitting & visualization process ###
        ############################################

        energy, counts = np.loadtxt(output_file_destination, skiprows=0, usecols=(0, 2), unpack=True)

        print(energy, counts)

        plt.semilogy()
        plt.xlabel("Energy (MeV)")
#            plt.ylim([0.0000000001, 0.001])
        plt.ylabel("Counts")
#            plt.show()
        '''
        plt.annotate("Cl Eff:" + str(float(Eff_net_Cl)), xy=(2.12, counts[212]), xytext=(4.44, 0.00001),
                    arrowprops=dict(arrowstyle="->"))
        plt.annotate("S Eff:" + str(float(Eff_net_S)), xy=(2.23, counts[223]), xytext=(2.23, 0.00001), arrowprops=dict(arrowstyle="->"))
        '''

        data = np.column_stack((energy, counts))
    #            h.close()

        plt.plot(data[10:, 0], data[10:, 1] * source_rate)  # plot data without fits


        ### Fit peak data from table
        df_peak_data = df_peak_data.loc[df_peak_data['Fit_peak'] == True]


        print(df_peak_data)
        for e in df_peak_data.index:
            print(e)
            line = df_peak_data.loc[e]
            print(line)
            print()


            peak = int(line['Peak']*100)
            left_marker = int(line['Left_marker'])
            right_marker = int(line['Right_marker'])

            #obsolete fitting
            '''
            peak_fit = Gauss_fitting.area_gauss_fit(self, data[H_peak - spread_H + i:H_peak + spread_H - i, 0],
                                        data[H_peak - spread_H + i:H_peak + spread_H - i, 1]
                                        * source_rate)
            '''

            # new fitting
            print(data[peak - left_marker:peak + right_marker, 0])
            print(data[peak - left_marker:peak + right_marker, 1])
            peak_area = Gauss_fitting.area_gauss_fit(self, data[peak - left_marker:peak + right_marker, 0],
                                        data[peak - left_marker:peak + right_marker, 1] * source_rate)


            df_peak_data.loc[e, 'Area_net'] = peak_area[0] # function result under [0] stands for area

        df_peak_data.to_csv(output_file_destination.replace(".out", "_report.csv"))


        """
        # ----- BEGIN PROMPT
        for i in np.arange(1): # wpisz tu później 3
            # spread for LaBr3
            #                spread_Si = 12
            #                spread_H = 7
            #                spread_C = 14
            #                spread_O = 14
            #                print(i)

            # Total = Gauss_fitting.total_spect(data[10:, 0], data[10:, 1] * source_rate)  # plot data without fits
            # Total = plt.plot(data[10:, 0], data[10:, 1] * source_rate)  # plot data without fits
            # Si = Gauss_fitting.area_gauss_fit(self, data[Si_peak - spread_Si + i:Si_peak + spread_Si - i, 0],
            #                           data[Si_peak - spread_Si + i:Si_peak + spread_Si - i, 1]
            #                           * source_rate)

            # Cl_low = Gauss_fitting.area_gauss_fit(self, data[Cl_peak_low - spread_Cl_low + i:Cl_peak_low + spread_Cl_low - i, 0],
            #                        data[Cl_peak_low - spread_Cl_low + i:Cl_peak_low + spread_Cl_low - i, 1]
            #                        * source_rate)

            #S = Gauss_fitting.area_gauss_fit(self, data[S_peak - spread_S + i:S_peak + spread_S - i+3, 0],
            #                        data[S_peak - spread_S + i:S_peak + spread_S - i+3, 1]
            #                        * source_rate)

            H = Gauss_fitting.area_gauss_fit(self, data[H_peak - spread_H + i:H_peak + spread_H - i, 0],
                                        data[H_peak - spread_H + i:H_peak + spread_H - i, 1]
                                        * source_rate)
            # Pb208 = area_gauss_fit(data[xl_Pb208_marker:xr_Pb208_marker, 0], data[xl_Pb208_marker:xr_Pb208_marker, 1] * n_flux_multiplier)
            #                Cl = area_gauss_fit(data[xl_Cl_marker:xr_Cl_marker, 0], data[xl_Cl_marker:xr_Cl_marker, 1] * n_flux_multiplier)

            C = Gauss_fitting.area_gauss_fit(self, data[C_peak - spread_C + i:C_peak + spread_C - i+1, 0],
                                        data[C_peak - spread_C + i:C_peak + spread_C - i+1, 1]
                                        * source_rate)

            O = Gauss_fitting.area_gauss_fit(self, data[O_peak - spread_O + i:O_peak + spread_O - i, 0],
                                        data[O_peak - spread_O + i:O_peak + spread_O - i, 1]
                                        * source_rate)

            #Cl = Gauss_fitting.area_gauss_fit(self, data[Cl_peak - spread_Cl + i:Cl_peak + spread_Cl - i, 0],
            #                            data[Cl_peak - spread_Cl + i:Cl_peak + spread_Cl - i, 1]
            #                            * source_rate)


#                Cl_low_to_O = np.round(Cl_low[0] / O[0], 4)
#                S_to_O = np.round(S[0] / O[0], 4)
#                C_to_O = np.round(C[0] / O[0], 4)
            C_to_O = np.round(C[0] / O[0], 4)

#            plt.text(6, 3E7, "Peak@2.23: "+str(int(peak_H)) + "\n" + "Peak@5.91: "+str(int(peak_Cl)) + "\n" + "Counts 0.5-10 MeV: "+str(int(data_sum)))
#            plt.title('Ratios: Cl_low/O: ' + str(Cl_low_to_O)  + ' S/O: ' + str(S_to_O) + ' C/O: ' + str(C_to_O))
        plt.title('Ratios: C/O: ' + str(C_to_O))

        print("File_name:" + file_name)
        print("Area net summary:")
        # print("Peak Si: " + str(Si[0]))
#            print("Peak Cl_low: " + str(Cl_low[0]))
#            print("Peak S: " + str(S[0]))
        print("Peak H: " + str(H[0]))
        print("Peak C: " + str(C[0]))
        print("Peak O: " + str(O[0]))

        print("Ratios:"+'\n')
#            print("Cl_low/O: " + str(Cl_low_to_O))
#            print("S/O: " + str(S_to_O))
        print("C/O: " + str(C_to_O) + '\n')

# ----- END PROMPT
        """
        '''
# ----- BEGIN DELAYED
        for i in np.arange(1):  # wpisz tu później 3

            # Total = Gauss_fitting.total_spect(data[10:, 0], data[10:, 1] * source_rate)  # plot data without fits
            Total = plt.plot(data[10:, 0], data[10:, 1] * source_rate)  # plot data without fits
            #               Si = area_gauss_fit(data[xl_Si_marker:xr_Si_marker, 0],
            #                              data[xl_Si_marker:xr_Si_marker, 1] * n_flux_multiplier)

            #           H = area_gauss_fit(data[xl_H_marker:xr_H_marker, 0], data[xl_H_marker:xr_H_marker, 1] * n_flux_multiplier)


            #H = Gauss_fitting.area_gauss_fit(self, data[H_peak - spread_H+2 + i:H_peak + spread_H - i, 0],
            #                        data[H_peak - spread_H+2 + i:H_peak + spread_H - i, 1]
            #                        * source_rate)

            
            H = Gauss_fitting.area_gauss_fit(self, data[H_peak - spread_H+2 + i:H_peak + spread_H - i, 0],
                                    data[H_peak - spread_H+2 + i:H_peak + spread_H - i, 1]
                                    * source_rate)

            # Pb208 = area_gauss_fit(data[xl_Pb208_marker:xr_Pb208_marker, 0], data[xl_Pb208_marker:xr_Pb208_marker, 1] * n_flux_multiplier)
            #                Cl = area_gauss_fit(data[xl_Cl_marker:xr_Cl_marker, 0], data[xl_Cl_marker:xr_Cl_marker, 1] * n_flux_multiplier)



            Cl = Gauss_fitting.area_gauss_fit(self, data[Cl_peak - spread_Cl + i:Cl_peak + spread_Cl - i, 0],
                                        data[Cl_peak - spread_Cl + i:Cl_peak + spread_Cl - i, 1]
                                        * source_rate)
            
            
            # Cu = Gauss_fitting.area_gauss_fit(self, data[Cu_peak - spread_Cu + i:Cu_peak + spread_Cu - i, 0],
            #                            data[Cu_peak - spread_Cu + i:Cu_peak + spread_Cu - i, 1]
            #                            * source_rate)
        #     N = [1.0, 1.0]
            
            
            
            #N = Gauss_fitting.area_gauss_fit(self, data[N_peak - spread_N + i:N_peak + spread_N - i, 0],
            #                            data[N_peak - spread_N + i:N_peak + spread_N - i, 1]
            #                            * source_rate)
            

            N_range = data[-100:-1]
            print(N_range)
            N_range = sum(data[-100:-1, 1])  # from 10 - 11 MeV
            N_range = N_range * source_rate
            print(N_range)
            
#            Cu_to_H = np.round(float(Cu[0]) / float(H[0]), 4)
            Cl_to_H = np.round(float(Cl[0]) / float(H[0]), 4)
            # N_to_Cl = np.round(float(N[0])/float(Cl[0]), 4)
#                N_to_H = np.round(float(N[0])/float(H[0]), 4)  # for peak integral calculation
            N_to_H = np.round(float(N_range)/float(H[0]), 7)  # for energy range calculation


#            plt.title('Ratios: Cl/H: ' + str(Cl_to_H))
            plt.title('Ratios: Cl/H: ' + str(Cl_to_H) + ', Ratios: N/H: ' + str(N_to_H))
#            plt.title('Ratios: Cl/H: ' + str(Cl_to_H) + " " + 'N/Cl: ' + str(N_to_Cl))
#            plt.title('Ratios: N/H: ' + str(N_to_H))

        print("File_name:" + file_name)
        print("Area net summary:")
        print("Peak H: " + str(H[0]))
        #print("Peak Cu: " + str(Cu[0]))
        print("Peak Cl: " + str(Cl[0]))
#            print("Peak N: " + str(N[0]))
        print("N range: " + str(N_range))
        print("Ratios:" + '\n')
        #print("Cu/H: " + str(Cu_to_H))
        print("Cl/H: " + str(Cl_to_H))
        # print("Cl/N: " + str(N_to_Cl))
        print("N/H: " + str(N_to_H))
        
        # ----- END DELAYED
        '''

        
        """
#               --- Begin others ---
        for i in np.arange(1):
            Th = Gauss_fitting.area_gauss_fit(self, data[Th_peak - spread_Th + 2 + i:Th_peak + spread_Th - i, 0],
                                    data[Th_peak - spread_Th + 2 + i:Th_peak + spread_Th - i, 1]
                                    * source_rate)

        print("Peak Th: " + str(Th[0]))
        """
        

    # plt.show() # jeśli potrzebujemy do wizualizacji
        plt.ylim(0.01, np.max((df.loc[10:, "Counts"])*source_rate*1.5))
        plt.savefig(output_file_destination.replace(".out", "_graph.png"),
                    dpi=None, facecolor='w', edgecolor='w',
                    orientation='portrait', papertype=None, format='png',
                    transparent=False, bbox_inches=None, pad_inches=0.1) # frameon=None


        plt.close()

        #            plt.show()
        energy = [0] * len(energy)
        counts = [0] * len(energy)
#        except:
        #print("Błąd otwarcia pliku!")
    

        print("Processing finished")
    # plt.close()
        return cell_name

    # ------------------------------
    #  --- PULSE HEIGHT ANALYSIS ---
    # ------------------------------

    def Analyse_File_F8_old(self, file_path, cell_name, source_rate='1E8*1', f4_integral=1):
        # c = My_Files() #instancja klasy My_Files
        df_peak_data = self.read_json_peak_data()
        print(df_peak_data)


        # cell_name = self.Window.lineEdit.text() #self.LINE_EDIT_CELL()   # pobiera tekst z textboxa
        # w funkcji stworzyłem instancję klasy wewnątrz tej samej klasy, po to
        # aby zaimportować metodę tej klasy do tej metody
        #source_rate = self.SET_SOURCE_RATE()
        #f4_integral = self.GET_F4_INTEGRAL()
        source_rate = Gauss_fitting.SR_CONVERT(self, source_rate) * f4_integral
        line_no = 0
        

        #listoffiles = c.Open_file_F8() # listoffiles = self.Open_file_F8 - tak było wcześniej

        # max_file = len(listoffiles)

        energy = []
        counts = []

#        global header_text
#        header_text = "test headrr"

#        listoffiles = filedialog.askopenfilenames()
        # initial directory
        #file_path = 0
     
        log_output_data = 0
        log_output_data_str = 0
        i = 0
        j = 0

        no_of_files = 1
        #for m in listoffiles:
#        try:
        # self.PROGRESS(no_of_files/max_file*100) # to działa! Ponieważ przez self dostajesz się do poziomu nadrzędnego.
        # Ważne: w klasie interactions masz klasę Analyse_File_F8 z self,
        # które daje Tobie możiwość nawiązania kontaktu miedyz tymi obiktami
        #no_of_files += 1
        
#        self.progress()  # progress po analizowanej zawartości pliku. A ja chcę po liście plików!
        # file_path = m
        file_name = os.path.basename(file_path)
        print(file_name)
        

        directory_path = os.path.dirname(file_path)

        #   READ MCNP FILE
        f = open(file_path, "r")

        output_file_name = file_name.replace(".o", "_") + "_sorted_" + str(cell_name.replace("  ", "__")) + ".out"
        output_file_destination = directory_path + "/" + output_file_name

        

#           --- bins calculation ---
        dataset = f.readlines()
        bins_total = Gauss_fitting.bin_calculator(self, dataset, cell_name)
        print("Bins total: " + str(bins_total))
#           ------------------------

        #   WRITE OUTPUT FROM MCNP
        g = open(output_file_destination, "w")
        #            g.write(header_text)

        # read number of header lines
        # with open(output_file_destination) as out:
        #    for header_line_no, l in enumerate(out):
        #        pass
        #    header_line_no = header_line_no + 1

        #    input_file = file.read(open_input_file)

        #            g.write("test"+"\n")  # dziala
#           g.write(self.header_description.get("1.0", END))
#           header_line_count = int(self.header_description.index('end-1c').split('.')[0])  # returns line count
        # print(header_line_count)



#          bins_total = Gauss_fitting.bin_calculator(f, cell_name)

        # aid_file.write(aid_header)

#        for line in f:
        print(dataset)

        line_no = 0  # previously 0  -  this is start line in output file
        for line in dataset:
            if 'cell  '+str(cell_name) in line:
                start_line = line_no
                new_output_list = []
                log_data = []

                output_data = dataset[start_line + 2:start_line + bins_total + 2]

                print(output_data)

                for line in output_data:
                    print(line)
                    new_output_list.append([float(elem) for elem in line.split()])
                    
                data_array = np.asarray(new_output_list)

            #       print(new_array)
                print(output_data[bins_total-1])

                for i in range(bins_total):
                    val = new_output_list[i][1]  # dostęp do elementu listy w liście 
                    if val == 0: #'0.00000E+00':
                        log_data.append(1E-10)
                    else:
                        log_data.append(val)
                    

                data_array_log = np.column_stack((data_array[:, 0], data_array[:, 1], log_data, data_array[:, 2]))
                print(data_array_log) # works well

                df = pd.DataFrame(data_array_log, columns=['E (MeV)', 'Counts', 'Counts(log)', 'Error(%)'])
                df = df.astype(float)
                print(df.values)


                # g.write(str(output_data[0]) + "  " + str(output_data[1]) + " " + str(log_output_data_str) + " " + str(output_data[2]) + " " + "\n")
                
                # data_sqrt = np.sqrt(float(output_data[1])*source_rate)




                np.savetxt(output_file_destination, df.values, fmt='%1.8f')

            line_no = line_no + 1
            
        f.close()
        g.close()

        print('Columns type: int, float, float')

        energy, counts = np.loadtxt(output_file_destination, skiprows=0, usecols=(0, 2), unpack=True)

        print(energy, counts)

        plt.semilogy()
        plt.xlabel("Energy (MeV)")
#            plt.ylim([0.0000000001, 0.001])
        plt.ylabel("Counts")
#            plt.show()
        '''
        plt.annotate("Cl Eff:" + str(float(Eff_net_Cl)), xy=(2.12, counts[212]), xytext=(4.44, 0.00001),
                    arrowprops=dict(arrowstyle="->"))
        plt.annotate("S Eff:" + str(float(Eff_net_S)), xy=(2.23, counts[223]), xytext=(2.23, 0.00001), arrowprops=dict(arrowstyle="->"))
        '''

        data = np.column_stack((energy, counts))
    #            h.close()

        plt.plot(data[10:, 0], data[10:, 1] * source_rate)  # plot data without fits
        # plt.show()


        for e in df_peak_data.index:
            print(e)
           
        # ----- BEGIN PROMPT
        for i in np.arange(1): # wpisz tu później 3
            # spread for LaBr3
            #                spread_Si = 12
            #                spread_H = 7
            #                spread_C = 14
            #                spread_O = 14
            #                print(i)

            # Total = Gauss_fitting.total_spect(data[10:, 0], data[10:, 1] * source_rate)  # plot data without fits
            Total = plt.plot(data[10:, 0], data[10:, 1] * source_rate)  # plot data without fits
            # Si = Gauss_fitting.area_gauss_fit(self, data[Si_peak - spread_Si + i:Si_peak + spread_Si - i, 0],
            #                           data[Si_peak - spread_Si + i:Si_peak + spread_Si - i, 1]
            #                           * source_rate)

            # Cl_low = Gauss_fitting.area_gauss_fit(self, data[Cl_peak_low - spread_Cl_low + i:Cl_peak_low + spread_Cl_low - i, 0],
            #                        data[Cl_peak_low - spread_Cl_low + i:Cl_peak_low + spread_Cl_low - i, 1]
            #                        * source_rate)

            #S = Gauss_fitting.area_gauss_fit(self, data[S_peak - spread_S + i:S_peak + spread_S - i+3, 0],
            #                        data[S_peak - spread_S + i:S_peak + spread_S - i+3, 1]
            #                        * source_rate)

            H = Gauss_fitting.area_gauss_fit(self, data[H_peak - spread_H + i:H_peak + spread_H - i, 0],
                                        data[H_peak - spread_H + i:H_peak + spread_H - i, 1]
                                        * source_rate)
            # Pb208 = area_gauss_fit(data[xl_Pb208_marker:xr_Pb208_marker, 0], data[xl_Pb208_marker:xr_Pb208_marker, 1] * n_flux_multiplier)
            #                Cl = area_gauss_fit(data[xl_Cl_marker:xr_Cl_marker, 0], data[xl_Cl_marker:xr_Cl_marker, 1] * n_flux_multiplier)

            C = Gauss_fitting.area_gauss_fit(self, data[C_peak - spread_C + i:C_peak + spread_C - i+1, 0],
                                        data[C_peak - spread_C + i:C_peak + spread_C - i+1, 1]
                                        * source_rate)

            O = Gauss_fitting.area_gauss_fit(self, data[O_peak - spread_O + i:O_peak + spread_O - i, 0],
                                        data[O_peak - spread_O + i:O_peak + spread_O - i, 1]
                                        * source_rate)

            #Cl = Gauss_fitting.area_gauss_fit(self, data[Cl_peak - spread_Cl + i:Cl_peak + spread_Cl - i, 0],
            #                            data[Cl_peak - spread_Cl + i:Cl_peak + spread_Cl - i, 1]
            #                            * source_rate)


#                Cl_low_to_O = np.round(Cl_low[0] / O[0], 4)
#                S_to_O = np.round(S[0] / O[0], 4)
#                C_to_O = np.round(C[0] / O[0], 4)
            C_to_O = np.round(C[0] / O[0], 4)

#            plt.text(6, 3E7, "Peak@2.23: "+str(int(peak_H)) + "\n" + "Peak@5.91: "+str(int(peak_Cl)) + "\n" + "Counts 0.5-10 MeV: "+str(int(data_sum)))
#            plt.title('Ratios: Cl_low/O: ' + str(Cl_low_to_O)  + ' S/O: ' + str(S_to_O) + ' C/O: ' + str(C_to_O))
        plt.title('Ratios: C/O: ' + str(C_to_O))

        print("File_name:" + file_name)
        print("Area net summary:")
        # print("Peak Si: " + str(Si[0]))
#            print("Peak Cl_low: " + str(Cl_low[0]))
#            print("Peak S: " + str(S[0]))
        print("Peak H: " + str(H[0]))
        print("Peak C: " + str(C[0]))
        print("Peak O: " + str(O[0]))

        print("Ratios:"+'\n')
#            print("Cl_low/O: " + str(Cl_low_to_O))
#            print("S/O: " + str(S_to_O))
        print("C/O: " + str(C_to_O) + '\n')

# ----- END PROMPT
        
        '''
# ----- BEGIN DELAYED
        for i in np.arange(1):  # wpisz tu później 3

            # Total = Gauss_fitting.total_spect(data[10:, 0], data[10:, 1] * source_rate)  # plot data without fits
            Total = plt.plot(data[10:, 0], data[10:, 1] * source_rate)  # plot data without fits
            #               Si = area_gauss_fit(data[xl_Si_marker:xr_Si_marker, 0],
            #                              data[xl_Si_marker:xr_Si_marker, 1] * n_flux_multiplier)

            #           H = area_gauss_fit(data[xl_H_marker:xr_H_marker, 0], data[xl_H_marker:xr_H_marker, 1] * n_flux_multiplier)


            #H = Gauss_fitting.area_gauss_fit(self, data[H_peak - spread_H+2 + i:H_peak + spread_H - i, 0],
            #                        data[H_peak - spread_H+2 + i:H_peak + spread_H - i, 1]
            #                        * source_rate)

            
            H = Gauss_fitting.area_gauss_fit(self, data[H_peak - spread_H+2 + i:H_peak + spread_H - i, 0],
                                    data[H_peak - spread_H+2 + i:H_peak + spread_H - i, 1]
                                    * source_rate)

            # Pb208 = area_gauss_fit(data[xl_Pb208_marker:xr_Pb208_marker, 0], data[xl_Pb208_marker:xr_Pb208_marker, 1] * n_flux_multiplier)
            #                Cl = area_gauss_fit(data[xl_Cl_marker:xr_Cl_marker, 0], data[xl_Cl_marker:xr_Cl_marker, 1] * n_flux_multiplier)



            Cl = Gauss_fitting.area_gauss_fit(self, data[Cl_peak - spread_Cl + i:Cl_peak + spread_Cl - i, 0],
                                        data[Cl_peak - spread_Cl + i:Cl_peak + spread_Cl - i, 1]
                                        * source_rate)
            
            
            # Cu = Gauss_fitting.area_gauss_fit(self, data[Cu_peak - spread_Cu + i:Cu_peak + spread_Cu - i, 0],
            #                            data[Cu_peak - spread_Cu + i:Cu_peak + spread_Cu - i, 1]
            #                            * source_rate)
        #     N = [1.0, 1.0]
            
            
            
            #N = Gauss_fitting.area_gauss_fit(self, data[N_peak - spread_N + i:N_peak + spread_N - i, 0],
            #                            data[N_peak - spread_N + i:N_peak + spread_N - i, 1]
            #                            * source_rate)
            

            N_range = data[-100:-1]
            print(N_range)
            N_range = sum(data[-100:-1, 1])  # from 10 - 11 MeV
            N_range = N_range * source_rate
            print(N_range)
            
#            Cu_to_H = np.round(float(Cu[0]) / float(H[0]), 4)
            Cl_to_H = np.round(float(Cl[0]) / float(H[0]), 4)
            # N_to_Cl = np.round(float(N[0])/float(Cl[0]), 4)
#                N_to_H = np.round(float(N[0])/float(H[0]), 4)  # for peak integral calculation
            N_to_H = np.round(float(N_range)/float(H[0]), 7)  # for energy range calculation


#            plt.title('Ratios: Cl/H: ' + str(Cl_to_H))
            plt.title('Ratios: Cl/H: ' + str(Cl_to_H) + ', Ratios: N/H: ' + str(N_to_H))
#            plt.title('Ratios: Cl/H: ' + str(Cl_to_H) + " " + 'N/Cl: ' + str(N_to_Cl))
#            plt.title('Ratios: N/H: ' + str(N_to_H))

        print("File_name:" + file_name)
        print("Area net summary:")
        print("Peak H: " + str(H[0]))
        #print("Peak Cu: " + str(Cu[0]))
        print("Peak Cl: " + str(Cl[0]))
#            print("Peak N: " + str(N[0]))
        print("N range: " + str(N_range))
        print("Ratios:" + '\n')
        #print("Cu/H: " + str(Cu_to_H))
        print("Cl/H: " + str(Cl_to_H))
        # print("Cl/N: " + str(N_to_Cl))
        print("N/H: " + str(N_to_H))
        
        # ----- END DELAYED
        '''

        
        """
#               --- Begin others ---
        for i in np.arange(1):
            Th = Gauss_fitting.area_gauss_fit(self, data[Th_peak - spread_Th + 2 + i:Th_peak + spread_Th - i, 0],
                                    data[Th_peak - spread_Th + 2 + i:Th_peak + spread_Th - i, 1]
                                    * source_rate)

        print("Peak Th: " + str(Th[0]))
        """
        

    # plt.show() # jeśli potrzebujemy do wizualizacji
        plt.ylim(0.01, np.max((df.loc[10:, "Counts"])*source_rate*1.5))
        plt.savefig(output_file_destination.replace(".out", "_graph.png"),
                    dpi=None, facecolor='w', edgecolor='w',
                    orientation='portrait', papertype=None, format='png',
                    transparent=False, bbox_inches=None, pad_inches=0.1) # frameon=None


        plt.close()

        #            plt.show()
        energy = [0] * len(energy)
        counts = [0] * len(energy)
#        except:
        #print("Błąd otwarcia pliku!")
    

        print("Processing finished")
    # plt.close()
        return cell_name # data - nie ma potrzeby zwracania ostatniej listy danych
#  jeśli je chcemy zwracać, to trzeba zadeklarować data jako pustą macierz, 
#  inaczej będzie błąd 'data' referenced before assignment
#  ja przeniosłem dane do innej pętli
       
    ''' 
# --- if only sole picture without fitting is needed----
        Total = plt.plot(data[10:, 0], data[10:, 1] * source_rate)  # plot data without fits
        plt.savefig(output_file_destination.replace(".out", "_graph.png"), 
                    dpi=None, facecolor='w', edgecolor='w',
                    orientation='portrait', papertype=None, format='png',
                    transparent=False, bbox_inches=None, pad_inches=0.1,
                    frameon=None)
        
#            plt.show()
#            time.sleep(3)
        plt.close()

        #            plt.show()
        energy = [0] * len(energy)
        counts = [0] * len(energy)
#        except:
        #print("Błąd otwarcia pliku!")
        

        print("Processing finished")
        plt.close()
        return listoffiles, cell_name # data - nie ma potrzeby zwracania ostatniej listy danych
    #  jeśli je chcemy zwracać, to trzeba zadeklarować data jako pustą macierz, 
    #  inaczej będzie błąd 'data' referenced before assignment
    #  ja przeniosłem dane do innej pętli
    '''

    # ------------------------------
    #  --- AVERAGE FLUX ANALYSIS ---
    # ------------------------------

    # def Analyse_File_F4(self):
    def Analyse_File_F4(self, file_path, cell_name, data_column, source_rate='1E8*1'):

#        cell_name = 'cell  2'
        # c = My_Files()
    #    listoffiles = self.Open_file_F4(cell_name)

        source_rate = Gauss_fitting.SR_CONVERT(self, source_rate)

        listoffiles = self.Open_file_F4()
        
        source_rate = float(source_rate)
        print(source_rate)
        # cell_name = self.window.self.lineEdit.text() #self.LINE_EDIT_CELL()   # pobiera tekst z textboxa

        #source_rate = self.SET_SOURCE_RATE() to delete
        #source_rate = Gauss_fitting.SR_CONVERT(self, source_rate) # to delete

        # for j in listoffiles:
        # try:
        input_file_path = file_path
        directory_path = os.path.dirname(input_file_path)   # directory path
        print(input_file_path)
        file_a = open(input_file_path, 'r')                 # open input file
        input_file_name = os.path.basename(input_file_path) # select input file name
        print(input_file_name)
        data = file_a.readlines()           # read all lines in the input file


#   open output file
        output_file_name = input_file_name.replace(".o", "_") + "_sorted_" + str(cell_name.replace("  ", "__")) + ".out"
        output_file_name_select = input_file_name.replace(".o", "_") + "_sorted_" + str(
            cell_name.replace("  ", "__")) + "_selected.out"
        output_file_raw = open(directory_path +"/"+ output_file_name, 'w')
        output_file_col_sel = open(directory_path +"/"+ output_file_name_select, 'w') # write file with selected columns
        dataset = data
    #     print(dataset)
        
        bins_total = Gauss_fitting.bin_calculator(self, dataset, cell_name)
        print("Bins total: " + str(bins_total))

        line_no = 0
        for lines in dataset:
            if cell_name in lines:
                start_line = line_no
                #            print (start_line)
                print ("Start data collection")
            line_no = line_no + 1
        #        print (line_no)
        final_data = dataset[start_line + 3:start_line + bins_total + 3] #data_bins_number

        # -----
        # preparation of python string elements in list to convert to floats
        print('Data filtering to float')
        data_float_conv = []
        ampersand = np.zeros(bins_total, dtype=str) #data_bins_number
        raw_data = np.array(final_data)
        for line in raw_data:
            data_float_conv.append(
                [float(elem) for elem in line.split()])  # split dzieli po kazdym bialym znaku (enter, spacja, tab)
        #    print(raw_data)
        data_float_conv = np.array(data_float_conv)  # tablica floatow
        np.savetxt(output_file_raw, data_float_conv)
        # column_set = 5
        column_set = int(data_column)

        energy = data_float_conv[:, 0]
        counts_raw = data_float_conv[:, column_set]

        np.ndarray.tolist(ampersand)
        ampersand[:] = '&'
        # print(ampersand)

        counts_onensour = data_float_conv[:, column_set]
        counts = data_float_conv[:, column_set] * source_rate
        #    if counts_onensour == 0:
        #        counts_onensour = 1E-10
        error = data_float_conv[:, column_set+1]


        data_sum = np.sum(counts[50:1000])

        print(len(energy))
        print(len(counts_raw))
        print(len(ampersand))
        print(len(counts_onensour))
        print(len(counts))
        print(len(error))


    #     data_total = np.column_stack((energy, counts_raw, ampersand, counts_onensour, counts, error))
        data_f4 = np.column_stack((counts_raw, ampersand))
        print(data_f4)

        #    np.savetxt(file_selected_c, data_selected)  # works only with the same data type

        #   ---- data for full output save
        #   for row in data_data_total:
        #       file_selected_c.write("\t".join([str(elem) for elem in row]) + "\n")  # save all elements in matrix row to file

        # --- data for f4 input

        line_no = len(data_f4)
        print(line_no)
        x = 0
        for row in data_f4:
            if x < line_no-1:
                output_file_col_sel.write(" ".join([str(elem) for elem in row]) + "\n")
            if x == line_no-1:
#                output_file_col_sel.write(row[0] + " &\n")
                output_file_col_sel.write(row[0] + "\n")
#                output_file_col_sel.write(0 + "\n")
            x = x + 1

#       -------------
#       ---- SBT ----
#       -------------
        
        peak_H = counts[223]
        peak_Cl = counts[612]
        print("Peak Cl:" + str(peak_Cl))
        print('Number of counts raw:' + str(sum(counts_raw)))

        plt.plot(energy, counts)   # sprawdz dlaczego zbiera dane tylko do 10.8 MeV
        plt.semilogy()


        plt.text(6, 3E5, "Peak@2.23: "+str(int(peak_H)) + "\n" + "Peak@6.12: "+str(int(peak_Cl)) + "\n" + "Counts 0.5-10 MeV: "+str(int(data_sum)))
        plt.errorbar(energy, counts, yerr=counts*error,
            #marker = 'o',
            color='k',
            ecolor='k',
            markerfacecolor='g',
            label="series 2",
            capsize=5,
            linestyle='None'
                    )
        plt.ylim([0.01, 1E7])
        plt.savefig(directory_path+"/"+output_file_name.replace('.out', '.png'), format="png")
        plt.show()
        
        

        print(energy)
        print(counts)
    
        file_a.close()
        output_file_col_sel.close()


        return listoffiles, cell_name

        #except:
        #    print("Błąd otwarcia pliku!")
            #--------------------
            #----- END F4 -------
            #--------------------

#       ---------------------------------------------------
#       --- AVERAGE FLUX x PH CONVOLUTION ---
#       ---------------------------------------------------


    def Analyse_File_F4xF8(self):
      #  cell_name = 30
      #  column_set = 5
       # source_rate = 3E8*100
        cell_name = self.LINE_EDIT_CELL()
        source_rate = self.SET_SOURCE_RATE()
        source_rate = Gauss_fitting.SR_CONVERT(self, source_rate)
        
        
        # dataset_list = self.Open_file_F4xF8       # to be done based on file list
        # print(dataset_list)
        # return 0
#       ---------------------------------------------------
#       --- AVERAGE FLUX FILE SELECTION FOR CONVOLUTION ---
#       ---------------------------------------------------

        print('Select file:')
        input_file_path = filedialog.askopenfilename(filetypes=((".o output files","*.o"),("all files","*.*"))) # input file path
        directory_path = os.path.dirname(input_file_path)   # directory path
        print(input_file_path)

        file_a = open(input_file_path, 'r')                 # open input file
        input_file_name = os.path.basename(input_file_path) # select input file name
        print(input_file_name)

        data = file_a.readlines()           # read all lines in the input file


#   open output file
        output_file_name = input_file_name.replace(".o", "_") + "_sorted_" + str(cell_name.replace("  ", "__")) + ".out" # change file name
        output_file_name_select = input_file_name.replace(".o", "_") + "_sorted_" + str(
            cell_name.replace("  ", "__")) + "_selected.out" # change file name with mcnp pulse height distribution

        output_file_raw = open(directory_path + "/" + output_file_name, 'w') # write raw file
        output_file_col_sel = open(directory_path + "/" + output_file_name_select, 'w')  # write file with selected columns
        dataset = data
        print (dataset)

#   search for exact cell name
        line_no = 0
        for lines in dataset:
            if cell_name in lines:
                start_line = line_no
                #            print (start_line)
                print ("Start data collection")
            line_no = line_no + 1
        #        print (line_no)
        final_data = dataset[start_line + 3:start_line + data_bins_number + 3]
        # final_data_splitted = [i.split('\n') for i in final_data]

        #    print(final_data_splitted)
        #    energy = final_data_splitted[:]
        #    print(energy)

        #   metoda zapisu danych
        #    for i in final_data:
        #        file_b.writelines("%s" % i)

        #        print(str(final_data_splitted))
        #            for lines in dataset:
        #                if line_no > 0 and line_no <data_bins_number:
        #                    print (lines)
        # while line_no == data_bins_number:
        #    print(line_no +"\n")

        #               print (line)
        #               print("OK")
        #               print (line_no)
        #    print(data_raw)

        #   data filtering

        # -----
        # preparation of python string elements in list to convert to floats
        print('Data filtering to float')
        data_float_conv = []
        ampersand = np.zeros(data_bins_number, dtype=str)
        raw_data = np.array(final_data)
        for line in raw_data:
            data_float_conv.append(
                [float(elem) for elem in line.split()])  # split dzieli po kazdym bialym znaku (enter, spacja, tab)
        #    print(raw_data)
        data_float_conv = np.array(data_float_conv)  # tablica floatow
        np.savetxt(output_file_raw, data_float_conv)

        column_set = int(self.SET_F4_COLUMN())

        energy = data_float_conv[:, 0]
        counts_raw = data_float_conv[:, column_set]

        np.ndarray.tolist(ampersand)
        ampersand[:] = '&'
        print (ampersand)

        counts_onensour = data_float_conv[:, column_set]
        counts = data_float_conv[:, column_set] * source_rate
        #    if counts_onensour == 0:
        #        counts_onensour = 1E-10
        error = data_float_conv[:, column_set+1]


        data_sum = np.sum(counts[50:1000])

        print(len(energy))
        print(len(counts_raw))
        print(len(ampersand))
        print(len(counts_onensour))
        print(len(counts))
        print(len(error))

        # data_total = np.column_stack((energy, counts_raw, ampersand, counts_onensour, counts, error))
        data_f4 = np.column_stack((counts_raw, ampersand))
        print (data_f4)

        sum_data = np.sum(counts_onensour)
        print(sum_data)
        #    np.savetxt(file_selected_c, data_selected)  # works only with the same data type

        #   ---- data for full output save
        #   for row in data_data_total:
        #       file_selected_c.write("\t".join([str(elem) for elem in row]) + "\n")  # save all elements in matrix row to file

        # --- data for f4 input

        line_no = len(data_f4)
        print(line_no)
        x = 0
        for row in data_f4:
            if x < line_no-1:
                output_file_col_sel.write(" ".join([str(elem) for elem in row]) + "\n")
            if x == line_no-1:
#                output_file_col_sel.write(row[0] + " &\n")
                output_file_col_sel.write(row[0] + "\n")
#                output_file_col_sel.write(0 + "\n")
            x = x + 1

            #       -------------
            #       ---- SBT ----
            #       -------------
        """
        peak_H = counts[223]
        peak_Cl = counts[612]
        print("Peak Cl:" + str(peak_Cl))

        plt.plot(energy, counts)
        plt.semilogy()

        plt.text(6, 3E5, "Peak@2.23: " + str(int(peak_H)) + "\n" + "Peak@6.12: " + str(
                 int(peak_Cl)) + "\n" + "Counts 0.5-10 MeV: " + str(int(data_sum)))
        plt.errorbar(energy, counts, yerr=counts * error,
                         # marker = 'o',
                         color='k',
                         ecolor='k',
                         markerfacecolor='g',
                         label="series 2",
                         capsize=5,
                         linestyle='None'
                     )
        plt.ylim([0.01, 1E6])
        plt.savefig(directory_path + "/" + output_file_name.replace('.out', '.png'), format="png")
        plt.show()
        plt.close()
        """

        print(energy)
        print(counts)
    # -----
#        file_a.close()
#        output_file_col_sel.close()



#       ---------------------------------------------------
#       --- PULSE HEIGHT FILE SELECTION FOR CONVOLUTION ---
#       ---------------------------------------------------

        print('Select ph file:')
#        input_ph_file_path = filedialog.askopenfilename()  # open dialog input file path
      #  input_ph_file_path = self.Open_file_F8(cell_name)

  
#        input_ph_file_path = self.Analyse_File_F8()[:] #z funkcji wysłuskuje dwa parametry, lista krotek
       # print(data_new)
        input_ph_file_path = self.Analyse_File_F8(self)[0]  # to działa dla F4xF8!!
        # tylko trzeba otworzyć plik po analizie
        
   #     directory_path = os.path.dirname(str(input_ph_file_path[1][0]))  # directory path
        directory_path = os.path.dirname(str(input_ph_file_path[0])) 
       # print(input_ph_file_path)

#        file_ph = open(input_ph_file_path[1][0], 'r')  # open input file
        fnam = input_ph_file_path[0].replace('.o', '__sorted_'+str(cell_name).replace('  ','__')+'.out')
        file_ph = open(fnam, 'r')  # open input file
#        input_ph_file_name = os.path.basename(input_ph_file_path[1][0])  # select input file name
        input_ph_file_name = os.path.basename(input_ph_file_path[0])  # select input file name
        print(input_ph_file_name)


        data_ph = np.loadtxt(file_ph, dtype=float)
        print(str(data_ph))


        energy = data_ph[:, 0]*100  # take energy from column_stack
        counts_processed = data_ph[:,1]*sum_data*source_rate # take counts from column_stack and multipy them
        counts_processed = [int(elem) for elem in counts_processed]
        data_processed = np.column_stack((energy, counts_processed))
        
      #  data_processed = np.array(data_processed, dtype = int)
#        data_processed = [int(elem) for elem in data_processed]

        np.savetxt(directory_path+"/"+input_ph_file_name.replace('.o', '_processed.outs'), data_processed, fmt="%d")

   #     plt.plot(data_ph_float[:,0], data_ph_float[:,2]*sum_data*source_rate)




#    ------ start data fitting for processed file
        for i in np.arange(1):
# spread for LaBr3
#                spread_Si = 12
#                spread_H = 7
#                spread_C = 14
#                spread_O = 14
#                print(i)

            # Total = Gauss_fitting.total_spect(data[10:, 0], data[10:, 1] * source_rate)  # plot data without fits
 #               Si = area_gauss_fit(data[xl_Si_marker:xr_Si_marker, 0],
  #                              data[xl_Si_marker:xr_Si_marker, 1] * n_flux_multiplier)

#           H = area_gauss_fit(data[xl_H_marker:xr_H_marker, 0], data[xl_H_marker:xr_H_marker, 1] * n_flux_multiplier)
            H = Gauss_fitting.area_gauss_fit(self, data_processed[H_peak - spread_H + 2 + i:H_peak + spread_H - i, 0],
                           data_processed[H_peak - spread_H + 2 + i:H_peak + spread_H - i, 1]) 

            # Pb208 = area_gauss_fit(data[xl_Pb208_marker:xr_Pb208_marker, 0], data[xl_Pb208_marker:xr_Pb208_marker, 1] * n_flux_multiplier)
#                Cl = area_gauss_fit(data[xl_Cl_marker:xr_Cl_marker, 0], data[xl_Cl_marker:xr_Cl_marker, 1] * n_flux_multiplier)
#            Cl = Gauss_fitting.area_gauss_fit(data_processed[Cl_peak-spread_Cl+i:Cl_peak+spread_Cl-i, 0], data_processed[Cl_peak-spread_Cl+i:Cl_peak+spread_Cl-i, 1])


            Cl = Gauss_fitting.area_gauss_fit(self, data_processed[Cl_peak - spread_Cl + i:Cl_peak + spread_Cl - i, 0],
                            data_processed[Cl_peak - spread_Cl + i:Cl_peak + spread_Cl - i, 1]) 


#            Cu = Gauss_fitting.area_gauss_fit(self, data_processed[Cu_peak - spread_Cu + i:Cu_peak + spread_Cu - i, 0],
#                            data_processed[Cu_peak - spread_Cu + i:Cu_peak + spread_Cu - i, 1])

            Cl_to_H = np.round(float(Cl[0]) / float(H[0]), 4)


            print(str(round(Cl_to_H, 4)))
#            print(str(round(Cu_to_H, 4)))


        plt.semilogy()
        plt.text(3*100, 1E4, "Peak@2.23: "+str(int(H[0])) + "\n" + "Cu/H: "+ str(round(Cl_to_H, 4))
                 + "\n" + "Counts 0.5-10 MeV: "+str(int(sum(data_processed[50:,1]))) + "\n" + "Flux: " + str(int(source_rate)))
        plt.plot(data_processed[:, 0], data_processed[:, 1])
        plt.savefig(directory_path + "/" + input_ph_file_name.replace('.o', '_processed.png'), format="png")
        plt.show()
        plt.close()
        


        
'''
# ------------------
# --- GUI design ---
# ------------------
class App(Frame, My_Files):
    def __init__(self, master):
        # create the application

        Frame.__init__(self, master) # https://stackoverflow.com/questions/43767988/typeerror-super-argument-1-must-be-type-not-classobj
       # super(App, self).__init__(master) - Frame to klasa starego typu, super z nia nie dziala
        self.grid() #jest tez self.pack()
        self.master.title("MCNP TGSA")  # title, TGSA - time gated spectra analysis
        self.master.geometry("700x300")
        self.master.maxsize(1000, 400)  # max size of the window
        self.create_widgets()

    def create_widgets(self):
        c = My_Files()  # aby zaimportowac funkcje (metodę) z klasy zewnetrznej, trzeba utworzyc INSTANCJE KLASY !!!
        # tutaj tworzę instancje klasy My_Files, w której również jest analiza danych w pliku

     #   self.openfilebutton = Button(self)
     #   self.openfilebutton["text"] = "Analyse pulse height"
     #   self.openfilebutton["command"] = self.data_selection_F8 # run fuction called openfiledialog - written by me
     #   self.openfilebutton.grid()

        self.openfilebutton = Button(self)
        self.openfilebutton["text"] = "Analyse pulse height"
        self.openfilebutton["command"] = c.Analyse_File_F8 # run method from my class - written by me
        self.openfilebutton.grid()

        self.openfilebutton = Button(self)
        self.openfilebutton["text"] = "Open av. flux file"
   #     self.openfilebutton["command"] = self.data_selection # run fuction called openfiledialog - written by me
        self.openfilebutton["command"] = c.Analyse_File_F4
        self.openfilebutton.grid()

        self.openfilebutton = Button(self)
        self.openfilebutton["text"] = "Process flux x ph files"
        self.openfilebutton["command"] = c.Analyse_File_F4xF8  # run fuction called openfiledialog - written by me
        self.openfilebutton.grid()

        self.openfilebutton = Button(self)
        self.openfilebutton["text"] = "Experimental process raw file"
        self.openfilebutton["command"] = c.Open_file_F4xF8 # !!! DO ROZWIĄZANIA! Z Analyse_File_F4xF8
        self.openfilebutton.grid()


        self.header_description = Text(self)
   #     self.header_description.insert(END, header_text)  # Default header
        self.header_description.grid()
#        self.header_description = Text(self)
#        self.header_description.insert(END, header_text)  # Default header
#        self.header_description.grid()


# ------- run the GUI program - MAINFRAME --------
#def main():
root = Tk()
root.geometry('200x150')
app = App(root)
print("GUI opened...")
root.mainloop()
'''