import csv
import json
import numpy as np

#   Pause program command line with custom message
def pause(message):
    programPause = raw_input(message)

#   Read CSV file and store in multidimensional array
def loadCSV(filename):
    print('Reading ' + filename + '...')
    columns = []
    csvData = {}

    #   Read column headers
    with open(filename, "rb") as csvFile:
        reader = csv.reader(csvFile)
        columns = reader.next()

    #   Add object key to csvData for each column header
    for header in columns:
        csvData.update({ header: [] })

    #   Select row elements to store in array
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            for key in csvData:
                csvData[key].append(row[key])

    return csvData

def combineDictionaries(arrayOfDictionaries):
    print "Combining {} data sets...".format(len(arrayOfDictionaries))
    resultDictionary = {}
    primaryKeys = []
    toRemove = []

    #   Add keys from first dictionary to array primaryKeys
    for key in arrayOfDictionaries[0]:
        primaryKeys.append(key)

    #   Find keys which do not exist in all dictionaries
    for arr in arrayOfDictionaries:
        for key in primaryKeys:
            if not (key in arr):
                toRemove.append(key)

    #   Remove keys which do not exist in all dictionaries
    for key in toRemove:
        primaryKeys.remove(key)

    #   Initialise keys of resultDictionary
    for key in primaryKeys:
        resultDictionary.update({ key: [] })

    #   Combine values from each dictionary
    for key in resultDictionary:
        joinValues = []
        for arr in arrayOfDictionaries:
            joinValues = joinValues + arr[key]

        resultDictionary.update({ key: joinValues })

    return resultDictionary

def priceOfPropertyOverTime(londonData):
    print('Calculating price of property over time...')
    priceOverTime = {}
    resultPricePerYear = {}

    #   Populate keys of priceOverTime
    for year in londonData['year']:
        if not (year in priceOverTime):
            priceOverTime.update({ year: [] })

    for index, year in enumerate(londonData['year']):
        priceOverTime[year].append(int(londonData['price'][index]))

    for key in priceOverTime:
        resultPricePerYear.update({ key: sum(priceOverTime[key]) / len(priceOverTime[key])})

    return resultPricePerYear

def main():
    print("\nAnalysis of London Property Sales\n")

    #   Read config file to get paths to csv data
    configData = []
    with open('config.json') as data_file:
        configData = json.load(data_file)

    #   Read raw csv files
    csvData = []
    for path in configData['path_to_data_files']:
        csvData.append(loadCSV(path))

    #   Combine csv data to create dictionary containing all column data
    londonData = combineDictionaries(csvData)

    #   Calculate price changes over time
    pricePerYear = priceOfPropertyOverTime(londonData)

    for key in sorted(pricePerYear):
        print ("{} {}".format(key, '{:00,.2f} GBP'.format(pricePerYear[key])))

    pause("\nPress the enter key to continue...")

#   Program entry point
if __name__ == "__main__":
    main()
