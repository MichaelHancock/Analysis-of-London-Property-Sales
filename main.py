import csv
import math
import json
import numpy as np

#   Pause program command line with custom message
def pause(message):
    programPause = raw_input(message)

#   Read CSV file and store in multidimensional array
def loadCSV(filename):
    print("Reading " + filename + "...")
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
    print ("Combining {} data sets...").format(len(arrayOfDictionaries))
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

def meanPriceVsLondonDataAttribute(londonData, attribute):
    salesData = {}
    result = {}

    #   Populate keys of salesData
    for key in londonData[attribute]:
        if (not (key in salesData)) and len(key) > 1:
            salesData.update({ key: [] })

    #   Add values to sub-arrays in salesData
    for index, key in enumerate(londonData[attribute]):
        if key in salesData:
            salesData[key].append(int(londonData["price"][index]))

    #   Find average prices in attribute range
    for sale in salesData:
        result.update({ sale: sum(salesData[sale]) / len(salesData[sale] )})

    return result

def medianPriceVsLondonDataAttribute(londonData, attribute):
    salesData = {}
    result = {}

    #   Populate keys of salesData
    for key in londonData[attribute]:
        if (not (key in salesData)) and len(key) > 1:
            salesData.update({ key: [] })

    #   Add values to sub-arrays in salesData
    for index, key in enumerate(londonData[attribute]):
        if key in salesData:
            salesData[key].append(int(londonData["price"][index]))

    #   Sort prices in sub-arrays
    for sale in salesData:
        salesData[sale] = sorted(salesData[sale])

    #   Get median value
    for sale in salesData:
        if (len(salesData[sale]) % 2) == 0:
            index = len(salesData[sale]) / 2
            result.update({ sale: (float(salesData[sale][index - 1]) + float(salesData[sale][index])) / 2 })
        else:
            index = int(math.floor(len(salesData[sale]) / 2))
            result.update({ sale: salesData[sale][index] })

    return result

def getMinOrMaxPricePerYear(londonData, londonBoroughs, getMaximum = False):
    prices = {}

    #   Populate keys of prices
    for year in londonData["year"]:
        if not (year in prices):
            prices.update({ year: "" })

    #   Calculate most expensive borough for each year
    currentBest = None
    currentBestBorough = ""
    for currentYear in prices:
        for borough in londonBoroughs:
            current = londonBoroughs[borough][currentYear]
            if getMaximum:
                if current > currentBest or currentBest == None:
                    currentBest = current
                    currentBestBorough = borough
            elif not getMaximum:
                if (current < currentBest and current > 0) or currentBest == None:
                    currentBest = current
                    currentBestBorough = borough
        prices[currentYear] = "{}: {:00,.2f} GBP".format(currentBestBorough, currentBest)
        currentBest = None
        currentBestBorough = ""

    return prices

def calculatePricePerBoroughOverTime(londonData):
    londonBoroughs = {}

    #   Populate keys of londonBoroughs
    for borough in londonData["borough_name"]:
        if (not (borough in londonBoroughs)) and len(borough) > 1:
            londonBoroughs.update({ borough: {} })

    #   Add sub-keys to londonBoroughs
    for borough in londonBoroughs:
        for year in londonData["year"]:
            if not (year in londonBoroughs[borough]):
                londonBoroughs[borough].update({ year: [] })

    #   Populate sub-arrays of prices
    for index, borough in enumerate(londonData["borough_name"]):
        if borough in londonBoroughs:
            londonBoroughs[borough][londonData["year"][index]].append(int(londonData["price"][index]))

    #   Calculate average for each sub-array
    for borough in londonBoroughs:
        for year in londonBoroughs[borough]:
            sumValue = sum(londonBoroughs[borough][year])
            if sumValue > 0:
                londonBoroughs[borough][year] = sum(londonBoroughs[borough][year]) / len(londonBoroughs[borough][year])
            else:
                londonBoroughs[borough][year] = 0

    return londonBoroughs

def calculatePercentageChangeInBoroughs(londonData, londonBoroughs):
    minYear = None
    maxYear = None
    boroughPercentageChange = {}

    #   Get Value of minYear and maxYear
    for year in londonData['year']:
        if year > maxYear or maxYear == None:
            maxYear = year
        if year < minYear or minYear == None:
            minYear = year

    #   Calculate percentage change
    for borough in londonBoroughs:
        if not (borough in boroughPercentageChange):
            currentMin = londonBoroughs[borough][minYear]
            currentMax = londonBoroughs[borough][maxYear]
            difference = currentMax - currentMin
            if (not difference == 0) and (not currentMin == 0) and (not currentMax == 0):
                boroughPercentageChange.update({ borough : (float(difference) / float(currentMin)) * 100 })
            else:
                boroughPercentageChange.update({ borough : 0 })

    return boroughPercentageChange

def main():
    print("\nAnalysis of London Property Sales\n")

    #   Read config file to get paths to csv data
    configData = []
    with open("config.json") as data_file:
        configData = json.load(data_file)

    #   Read raw csv files
    csvData = []
    for path in configData["path_to_data_files"]:
        csvData.append(loadCSV(path))

    #   Combine csv data to create dictionary containing all column data
    londonData = combineDictionaries(csvData)

    #   Calculate average price over time
    print("\nCalculating average property price changes over time")
    meanPricePerYear = meanPriceVsLondonDataAttribute(londonData, "year")
    for key in sorted(meanPricePerYear):
        print ("{} {}".format(key, "\t{:00,.2f} GBP".format(meanPricePerYear[key]))).expandtabs(30)

    #   Calculate median price over time
    print("\nCalculating median property price changes over time")
    medianPricePerYear = medianPriceVsLondonDataAttribute(londonData, "year")
    for key in sorted(medianPricePerYear):
        print ("{} {}".format(key, "\t{:00,.2f} GBP".format(medianPricePerYear[key]))).expandtabs(30)

    #   Calculate average price over London boroughs
    print("\nCalculating average property prices in London boroughs")
    pricePerBorough = meanPriceVsLondonDataAttribute(londonData, "borough_name")
    for key, value in sorted(pricePerBorough.iteritems(), key=lambda (k,v): (v,k)):
        print ("{} {}".format(key, "\t{:00,.2f} GBP".format(value))).expandtabs(30)

    #   Calculate median price over London boroughs
    print("\nCalculating median property prices in London boroughs")
    medianPricePerBorough = medianPriceVsLondonDataAttribute(londonData, "borough_name")
    for key, value in sorted(medianPricePerBorough.iteritems(), key=lambda (k,v): (v,k)):
        print ("{} {}".format(key, "\t{:00,.2f} GBP".format(value))).expandtabs(30)

    #   Calculate price changes over time in London boroughs
    print("\nCalculating average property price changes over time in London boroughs")
    pricePerBoroughOverTime = calculatePricePerBoroughOverTime(londonData)
    maxPropertyPrices = getMinOrMaxPricePerYear(londonData, pricePerBoroughOverTime, True)
    minPropertyPrices = getMinOrMaxPricePerYear(londonData, pricePerBoroughOverTime, False)
    print("\nDetailed output of price per year in London boroughs saved at Output/London_Borough_Statistics.txt\n")
    for key in sorted(maxPropertyPrices):
        print("{}:\tMost expensive borough: {}. \n\tLeast expensive borough: {}.\n").format(key, maxPropertyPrices[key], minPropertyPrices[key])

    #   Output borough statistics to file
    output = "Borough\t| Year | Average Price\n\n".expandtabs(25)
    for borough in pricePerBoroughOverTime:
        for key, value in sorted(pricePerBoroughOverTime[borough].iteritems(), key=lambda (k,v): (v,k)):
            output = output + "{}\t| {} | {:00,.2f}\n".format(borough, key, pricePerBoroughOverTime[borough][key]).expandtabs(25)
    text_file = open("Output/London_Borough_Statistics.txt", "w")
    text_file.write(output)
    text_file.close()

    #   Calculate percentage change in borough average prices
    print ("Calculating percentage change in average prices for London boroughs")
    boroughPercentageChange = calculatePercentageChangeInBoroughs(londonData, pricePerBoroughOverTime)
    for key, value in sorted(pricePerBorough.iteritems(), key=lambda (k,v): (v,k)):
        if (not int(boroughPercentageChange[key]) == 0):
            print("{}\t{}%").format(key, round(boroughPercentageChange[key], 2)).expandtabs(30)

    pause("\nPress the enter key to continue...")

#   Program entry point
if __name__ == "__main__":
    main()
