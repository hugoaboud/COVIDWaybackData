import time

## Load data

with open("data/preprocess_data.tsv","r") as file:
    data = [];
    for line in file:
        data.append(line.split("\t"))

## Remove repeated entries

unique_data = []
for i in range(1,len(data)):
    equal = True
    for j in range(1, 11):
        if (data[i][j] != data[i-1][j]):
            equal = False
            break
    if not equal:
        unique_data.append(data[i])

## Split data into day arrays

day_data = {}
for entry in unique_data:
    etime = time.strptime(entry[0], "%Y-%m-%d %H:%M:%S%z")
    eday = str(etime.tm_year)+str(etime.tm_mon)+str(etime.tm_mday)
    if (eday not in day_data):
        day_data[eday] = [entry]
    else:
        day_data[eday].append(entry)

## Get only the last timestamp

final_data = []

for day in day_data.keys():
    entries = day_data[day]
    max = time.gmtime(0)
    max_e = 0
    for e in range(len(entries)):
        etime = time.strptime(entries[e][0], "%Y-%m-%d %H:%M:%S%z")
        if (etime > max):
            max = etime
            max_e = e
    final_data.append(entries[max_e])

for entry in final_data:
    print(entry)

print("Original data samples: " + str(len(data)))
print("Unique data samples: " + str(len(unique_data)))
print("Last-of-day data samples: " + str(len(final_data)))

with open("data/clean_data.tsv","w") as file:
    for entry in final_data:
        line = ""
        for e in range(len(entry)):
            line += entry[e] + ("\t" if e < len(entry)-1 else "")
        file.write(line)
