import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from numpy import trapz
import peakutils as pk
import matplotlib.pyplot as plt

class Gauss_fitting:
    #  -----------------------------
    #  --- mathematical functions ---
    #  -----------------------------


    def bin_calculator(self, dataset, cell__name):
        bins_number = 0
        line_no = 0
        for line in dataset:
            line_no += 1
            if "cell  " + str(cell__name) in line:
                for line in dataset[line_no:]:
                    bins_number += 1
                    if not 'time' in line:
                        if 'total' in line:
                            print(str(bins_number-3)) # minus trzy wiersze z wyrazeniem energy, time and total
                            return(bins_number-3) # return value, do not loop for lines after total statement


    def SR_CONVERT(self, input_sr_str):
        source_rate = input_sr_str
        source_rate = source_rate.split('*')
        source_rate_flux = float(source_rate[0])
        source_rate_time = float(source_rate[1])
        source_rate = float(source_rate_flux*source_rate_time)
        source_rate = round(source_rate, 0)
        return source_rate

    def total_spect(self, x, y):  # x and y as list
        plt.plot(x, y, 'b+:', label='data', linestyle='-', markersize=1)
        plt.semilogy()
        plt.close()
 #       plt.ylim([1, 2E5])

    def Gauss(self, x, a, x0, sigma):
        return a * np.exp(-(x - x0) ** 2 / (2 * sigma ** 2))

    def Gauss_double(self, x, a, x0, sigma, a2, x02, sigma2):   # to test
        return a * np.exp(-(x - x0) ** 2 / (2 * sigma ** 2)) + a2 * np.exp(-(x - x02) ** 2 / (2 * sigma2 ** 2))

    def Linear(self, x, a, b):
        return a * x + b

    # ---
    # --- Gaussian fitting
    # ---

    def area_gauss_fit_pk(self, x, y):
        dataset = pk.gaussian_fit(x,y,center_only=False)
        return dataset

    def area_gauss_fit(self, x, y):  # x and y as list
        # lin_base_points = [10000]
        mat = Gauss_fitting()    # instacja klasy Math - niepotrzebna - dostęp przez self.
        Y_average_markers = []
        mean = sum(x * y) / sum(y)
        sigma = np.sqrt(sum(y * (x - mean) ** 2) / sum(y))
        try: 
            popt, pcov = curve_fit(self.Gauss, x, y, p0=[max(y), mean, sigma]) #p0 - initial guess of parameters
            maxim = np.max(x)
            minim = np.min(x)
            mean_ctr = np.mean([maxim, minim])
            FWHM = (2.3548*sigma)/(mean_ctr)*100  # expressed in percent

            # print("Fit parameters: " + str(popt), "FWHM: ", FWHM)
            print("Fit parameters:", popt, "FWHM: ", FWHM, '%')
    #            fitted_points = (self.Gauss(x, *popt))
            fitted_points = (self.Gauss(x, *popt))
            #        print("Fitted points:" + str(fitted_points))
            area_tot = trapz(fitted_points)
            area_tot_simple = trapz(y)  # just for debigging and results comparing

            # linear baseline remover
            x_data_linear = x[0], x[-1]
            y_data_linear = y[0], y[-1]

            # marker counts average
            #    Y_average_xl = np.mean(data[(xl_C_marker):(xl_C_marker + 2), 1] * n_flux_multiplier)
            #    Y_average_xr = np.mean(data[(xr_C_marker):(xr_C_marker + 2), 1] * n_flux_multiplier)
            Y_average_xl = int(np.mean(y[0:3]))  # pierwsze dwa elementy tablicy - dane punktów fitowania
            Y_average_xr = int(np.mean(y[-4:-1]))  # ostatnie dwa elementy tablicy - dane puntków fitowania
            Y_average_markers.append(Y_average_xl)
            Y_average_markers.append(Y_average_xr)
            print(str(Y_average_markers))
            print("Average markers: " + str(Y_average_xl) + str(Y_average_xr))

            #    popt1, pcov1 = curve_fit(Linear,  x_data_linear , y_data_linear)
    #            popt1, pcov1 = curve_fit(self.Linear, x_data_linear, Y_average_markers)  # wersja z usrednianiem markerow
            popt1, pcov1 = curve_fit(self.Linear, x_data_linear, Y_average_markers)
            # fitted_points_lin_base = (Linear(x_markers, *popt1))
            print("Linear baseline fit params: " + str(popt1))
    #            fitted_lin_points = (self.Linear(x, *popt1))
            fitted_lin_points = (self.Linear(x, *popt1))

            area_baseline = trapz(fitted_lin_points)

            area_net = area_tot - area_baseline

            print(area_net)
            # FWHM plotting - to be done
            print(popt)
            print("Adding FWHM line - to be done in future")
            #popt2, pcov2 = curve_fit(mat.Linear, x_data_linear, Y_average_markers) 

            #    plt.plot(x, y, 'b+:', label='data')
    #            plt.plot(x, self.Gauss(x, *popt), 'r-', label='fit')
    #            plt.plot(x, self.Linear(x, *popt1), label='baseline')
            plt.plot(x, self.Gauss(x, *popt), 'r-', label='fit')
            plt.plot(x, self.Linear(x, *popt1), label='baseline')
            plt.legend()
            plt.xlabel('Energy')
            plt.ylabel('Counts')
            
            return area_net, fitted_points, FWHM
        
        except:
            print("Low peak statisics. Simplified fitting launching.")
            # linear baseline remover
            x_data_linear = x[0], x[-1]
            y_data_linear = y[0], y[-1]

            # marker counts average
            #    Y_average_xl = np.mean(data[(xl_C_marker):(xl_C_marker + 2), 1] * n_flux_multiplier)
            #    Y_average_xr = np.mean(data[(xr_C_marker):(xr_C_marker + 2), 1] * n_flux_multiplier)
            Y_average_xl = int(np.mean(y[0:3]))  # pierwsze dwa elementy tablicy - dane punktów fitowania
            Y_average_xr = int(np.mean(y[-4:-1]))  # ostatnie dwa elementy tablicy - dane puntków fitowania
            Y_average_markers.append(Y_average_xl)
            Y_average_markers.append(Y_average_xr)
            print(str(Y_average_markers))
            print("Average markers: " + str(Y_average_xl) +" "+ str(Y_average_xr))

            #    popt1, pcov1 = curve_fit(Linear,  x_data_linear , y_data_linear)
#            popt1, pcov1 = curve_fit(self.Linear, x_data_linear, Y_average_markers)  # wersja z usrednianiem markerow
            popt1, pcov1 = curve_fit(mat.Linear, x_data_linear, Y_average_markers)
            # fitted_points_lin_base = (Linear(x_markers, *popt1))
            print("Linear baseline fit params: " + str(popt1))
#            fitted_lin_points = (self.Linear(x, *popt1))
            fitted_lin_points = (mat.Linear(x, *popt1))

            area_baseline = trapz(fitted_lin_points)

            print("Unable to fit peak, conditions not met. Run simplified peak area integration.")
            area_tot = trapz(y) # y as a list
            area_net = area_tot - area_baseline
            print("Simplified area total:" + str(area_net))
        # plt.show()

            area_net = area_tot - area_baseline
            if area_net < 0:
                print("area_net<0")
                area_net = 1E-10
            print("Area tot: " + str(int(area_tot)))
            print("Area baseline: " + str(int(area_baseline)))
            print("Area net: " + str(int(area_net)))

#            plt.plot(x, self.Linear(x, *popt1), label='baseline')
            plt.plot(x, mat.Linear(x, *popt1), label='baseline')
            plt.legend()
            plt.xlabel('Energy')
            plt.ylabel('Counts')


            return area_net, fitted_lin_points
        