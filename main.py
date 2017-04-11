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

def priceVsLondonDataAttribute(londonData, attribute):
    salesData = {}
    result = {}

    #   Populate keys of salesData
    for key in londonData[attribute]:
        if (not (key in salesData)) and len(key) > 1:
            salesData.update({ key: [] })

    #   Add values to sub-arrays in salesData
    for index, key in enumerate(londonData[attribute]):
        if key in salesData:
            salesData[key].append(int(londonData['price'][index]))

    #   Find average prices in attribute range
    for key in salesData:
        result.update({ key: sum(salesData[key]) / len(salesData[key] )})

    return result

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
    print("\nCalculating property price changes over time")
    pricePerYear = priceVsLondonDataAttribute(londonData, 'year')
    for key in sorted(pricePerYear):
        print ("{} {}".format(key, '\t{:00,.2f} GBP'.format(pricePerYear[key]))).expandtabs(30)

    #   Calculate price changes over time in London boroughs
    print("\nCalculating average property prices in London boroughs")
    pricePerBorough = priceVsLondonDataAttribute(londonData, 'borough_name')
    for key, value in sorted(pricePerBorough.iteritems(), key=lambda (k,v): (v,k)):
        print ("{} {}".format(key, '\t{:00,.2f} GBP'.format(value))).expandtabs(30)

    pause("\nPress the enter key to continue...")

#   Program entry point
if __name__ == "__main__":
    main()
