from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import date2num

DATA_FILE = "data/clean_data.tsv"
data = []

class Entry:
    def __init__(self, time, cases, deaths, recovered, active, serious, tests):
        self.time = time
        self.cases = cases
        self.deaths = deaths
        self.recovered = recovered
        self.active = active
        self.serious = serious
        self.tests = tests
    def __str__(self):
        return str(self.time) + "," + str(self.cases) + "," + str(self.deaths) + "," + str(self.recovered) + "," + str(self.active) + "," + str(self.serious) + "," + str(self.tests)

with open(DATA_FILE,"r") as file:
    for line in file:
        entry = line.split("\t")
        data.append(Entry(datetime.strptime(entry[0], "%Y-%m-%d %H:%M:%S%z"),
                            int(entry[2].replace(',','')),
                            int(entry[4].replace(',','')),
                            int(entry[6].replace(',','')),
                            int(entry[7].replace(',','')),
                            int(entry[8].replace(',','')),
                            int(entry[11].replace(',',''))))
data = data[::-1]

times = np.array([d.time.date() for d in data])
cases = np.array([d.cases for d in data])
deaths = np.array([d.deaths for d in data])
tests = np.array([d.tests for d in data])
t = np.linspace(times[0].toordinal(),times[-1].toordinal(),100)

def lin_graph(output):
    plt.suptitle('Total de Testes e Casos de COVID-19 por dia')
    #fit_cases = np.poly1d(np.polyfit([t.toordinal() for t in times], cases/1000000.0, 2))
    #fit_tests = np.poly1d(np.polyfit([t.toordinal() for t in times], tests/1000000.0, 2))
    plt.plot(times,tests/1000000.0, label='Testes', color='blue', linewidth=1)
    #plt.plot(t, fit_tests(t), label='Testes', color='blue', linewidth=0.7, alpha=0.5)
    plt.plot(times,cases/1000000.0, label='Casos', color='red', linewidth=1)
    #plt.plot(t, fit_cases(t), label='Casos', color='red', linewidth=0.7, alpha=0.5)
    plt.ylabel("milhões")
    plt.legend(loc="upper left")
    plt.axes().xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))
    plt.locator_params(axis='y', nbins=20)
    plt.savefig(output)
    plt.close()

def log_graph(output):
    plt.suptitle('Total de Testes e Casos de COVID-19 por dia, escala log')
    #fit_cases = np.poly1d(np.polyfit([t.toordinal() for t in times], np.log(cases), 2))
    #fit_tests = np.poly1d(np.polyfit([t.toordinal() for t in times], np.log(tests), 2))
    plt.plot(times,np.log(tests), label='Testes', color='blue', linewidth=1)
    #plt.plot(t, fit_tests(t), label='Testes', color='blue', linewidth=0.7, alpha=0.5)
    plt.plot(times,np.log(cases), label='Casos', color='red', linewidth=1)
    #plt.plot(t, fit_cases(t), label='Casos', color='red', linewidth=0.7, alpha=0.5)
    plt.ylabel("log()")
    plt.legend(loc="upper left")
    plt.axes().xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))
    plt.locator_params(axis='y', nbins=20)
    plt.savefig(output)
    plt.close()

cases_diff = cases[1:]-cases[:-1]
tests_diff = tests[1:]-tests[:-1]

def by_week(output):
    plt.suptitle('Novos Testes e Casos de COVID-19 por semana')
    week_cases = []
    week_days = []
    for i in range(len(cases_diff)):
        if i%7 == 0:
            week_cases.append(0)
            week_days.append(times[i+1])
        week_cases[-1] += cases_diff[i]/1000000.0
    week_tests = []
    for i in range(len(tests_diff)):
        if i%7 == 0: week_tests.append(0)
        week_tests[-1] += tests_diff[i]/1000000.0
    plt.bar(date2num(week_days)-1.5,week_tests,3,color="blue",label="Testes")
    plt.bar(date2num(week_days)+1.5,week_cases,3,color="red",label="Casos")
    plt.axes().xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))
    plt.ylabel("milhões")
    plt.xticks(week_days)
    plt.legend(loc="upper left")
    plt.savefig(output)
    plt.close()

def cases_by_tests(output, delay=0):
    if (delay > 0):
        plt.suptitle('Relação entre Casos e Testes (com atraso de '+str(delay)+' dias) de COVID-19 por dia')
        plt.plot(times[delay:],cases[:-delay]/tests[delay:], linewidth=1)
    else:
        plt.suptitle('Relação entre Casos e Testes de COVID-19 por dia')
        plt.plot(times,cases/tests, linewidth=1)
    plt.axes().xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))
    plt.savefig(output)
    plt.close()

def deaths_by_cases(output, delay):
    plt.suptitle('Relação entre Mortes (com atraso de '+str(delay)+' dias) e Casos de COVID-19 por dia')
    plt.plot(times[delay:],deaths[delay:]/cases[:-delay], linewidth=1)
    plt.axes().xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))
    plt.savefig(output)
    plt.close()

lin_graph("plot/linear.png")
log_graph("plot/log.png")
by_week("plot/week.png")
deaths_by_cases("plot/deaths_by_cases.png",20)
cases_by_tests("plot/cases_by_tests0.png")
cases_by_tests("plot/cases_by_tests7.png",7)
