import csv
import math
import json
import numpy as np
from numpy import mean

def pause(message):
    programPause = raw_input(message)

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

def trimmedMean(arr, percent):
    n = len(arr)
    k = int(round(n*(float(percent)/100)/2))
    return mean(arr[k+1:n-k])

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

def countSales(londonData):
    londonBoroughs = {}

    #   Populate keys of londonBoroughs
    for borough in londonData["borough_name"]:
        if (not (borough in londonBoroughs)) and len(borough) > 1:
            londonBoroughs.update({ borough: 0 })

    #   Count number of sales for each borough
    for saleLocation in londonData["borough_name"]:
        if len(saleLocation) > 1:
            londonBoroughs[saleLocation] = londonBoroughs[saleLocation] + 1

    return londonBoroughs

def countSalesOverTime(londonData):
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

    #   Calculate count for each sub-array
    for borough in londonBoroughs:
        for year in londonBoroughs[borough]:
            sumValue = sum(londonBoroughs[borough][year])
            londonBoroughs[borough][year] = len(londonBoroughs[borough][year])

    return londonBoroughs

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

def getMinOrMaxPerYear(londonData, londonBoroughs, getMaximum = False, formatCurrency = False):
    prices = {}
    outline = "{}: {}"

    if formatCurrency:
        outline = "{}: {:00,.2f} GBP"

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
        prices[currentYear] = outline.format(currentBestBorough, currentBest)
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

def calculatePercentageChangeInBoroughs(londonData, londonBoroughs, minYear, maxYear):
    boroughPercentageChange = {}

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

def calculateYearByYearPercentageChange(londonData, meanPricePerYear):
    years = []
    changePerYear = {}

    #   Populate value of years
    for currentYear in sorted(meanPricePerYear):
        years.append(currentYear)

    #   Calculate percentage change between each year
    for index, year in enumerate(sorted(meanPricePerYear)):
        if index < (len(meanPricePerYear) - 1):
            difference = meanPricePerYear[years[index + 1]] - meanPricePerYear[years[index]]
            percentageChange = float(difference) / float(meanPricePerYear[years[index]]) * 100
            changePerYear.update({
                "{} - {}".format(str(years[index]), str(years[index + 1])) :
                    percentageChange
                })

    return changePerYear

def calculateRangeInBoroughs(londonData):
    boroughs = {}

    #   Populate keys of boroughs
    for key in londonData['borough_name']:
        if (not (key in boroughs)) and len(key) > 1:
            boroughs.update({ key: [] })

    #   Add values to sub-arrays in boroughs
    for index, key in enumerate(londonData['borough_name']):
        if key in boroughs:
            boroughs[key].append(int(londonData["price"][index]))

    #   Find range of prices for each borough
    for key in boroughs:
        minimum = min(boroughs[key])
        maximim = max(boroughs[key])
        boroughs[key] = maximim - minimum

    return boroughs

def numberOfMillionPoundSales(londonData):
    boroughs = {}

    #   Populate keys of boroughs
    for key in londonData['borough_name']:
        if (not (key in boroughs)) and len(key) > 1:
            boroughs.update({ key: [] })

    #   Add values to sub-arrays in boroughs
    for index, key in enumerate(londonData['borough_name']):
        if key in boroughs:
            boroughs[key].append(int(londonData["price"][index]))

    #   Count the number of sales that cost over 1million
    for key in boroughs:
        salesOverOneMillion = 0
        for sale in boroughs[key]:
            if sale >= 1000000:
                salesOverOneMillion = salesOverOneMillion + 1
        boroughs[key] = salesOverOneMillion

    return boroughs


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

    #   Get Value of minYear and maxYear
    minYear = None
    maxYear = None
    for year in londonData['year']:
        if year > maxYear or maxYear == None:
            maxYear = year
        if year < minYear or minYear == None:
            minYear = year

    finalOutput = "Borough\t| Total Number of Sales\n".expandtabs(25)

    #   Count the number of cumulative sales
    print("\nCounting the total number of property sales between {} and {}").format(minYear, maxYear)
    cumulativeSales = countSales(londonData)
    for key, value in sorted(cumulativeSales.iteritems(), key=lambda (k,v): (v,k)):
        finalOutput = finalOutput + "{}\t| {}\n".format(key, value).expandtabs(25)
        print ("{} {}".format(key, "\t{}".format(value))).expandtabs(30)

    #   Count the number of sales over time
    print("\nCounting the total number of property sales between across time and boroughs").format(minYear, maxYear)
    boroughSaleCount = countSalesOverTime(londonData)
    maxSalesCount = getMinOrMaxPerYear(londonData, boroughSaleCount, True, False)
    minSalesCount = getMinOrMaxPerYear(londonData, boroughSaleCount, False, False)
    finalOutput = finalOutput + "\nYear | Borough With Most / Least Sales\n".expandtabs(25)
    for key in sorted(maxSalesCount):
        finalOutput = finalOutput + "{} | Most sales: {} \n       Least sales: {}\n".format(key, maxSalesCount[key], minSalesCount[key]).expandtabs(25)
        print("{}:\tMost sales: {}.\n\tLeast sales: {}.\n").format(key, maxSalesCount[key], minSalesCount[key])

    #   Output detailed number of sales per borough to file
    output = "Borough\t| Year | Number Of Sales\n\n".expandtabs(25)
    for borough in boroughSaleCount:
        for key, value in sorted(boroughSaleCount[borough].iteritems()):
            output = output + "{}\t| {} | {}\n".format(borough, key, boroughSaleCount[borough][key]).expandtabs(25)
    text_file = open("Output/London_Borough_Sales.txt", "w")
    text_file.write(output)
    text_file.close()
    boroughSaleCount = []
    maxSalesCount = []
    minSalesCount = []

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
    finalOutput = finalOutput + "\nBorough\t| Mean Sale Price\n".expandtabs(25)
    pricePerBorough = meanPriceVsLondonDataAttribute(londonData, "borough_name")
    for key, value in sorted(pricePerBorough.iteritems(), key=lambda (k,v): (v,k)):
        finalOutput = finalOutput + "{}\t| {}\n".format(key, "{:00,.2f} GBP".format(value)).expandtabs(25)
        print ("{} {}".format(key, "\t{:00,.2f} GBP".format(value))).expandtabs(30)

    #   Calculate median price over London boroughs
    print("\nCalculating median property prices in London boroughs")
    finalOutput = finalOutput + "\nBorough\t| Median Sale Price\n".expandtabs(25)
    medianPricePerBorough = medianPriceVsLondonDataAttribute(londonData, "borough_name")
    for key, value in sorted(medianPricePerBorough.iteritems(), key=lambda (k,v): (v,k)):
        finalOutput = finalOutput + "{}\t| {}\n".format(key, "{:00,.2f} GBP".format(value)).expandtabs(25)
        print ("{} {}".format(key, "\t{:00,.2f} GBP".format(value))).expandtabs(30)
    medianPricePerBorough = []

    #   Calculate price changes over time in London boroughs
    print("\nCalculating average property price changes over time in London boroughs")
    pricePerBoroughOverTime = calculatePricePerBoroughOverTime(londonData)
    maxPropertyPrices = getMinOrMaxPerYear(londonData, pricePerBoroughOverTime, True, True)
    minPropertyPrices = getMinOrMaxPerYear(londonData, pricePerBoroughOverTime, False, True)
    finalOutput = finalOutput + "\nYear | Borough With Most Expensive / Least Expensive Sales\n".expandtabs(25)
    for key in sorted(maxPropertyPrices):
        finalOutput = finalOutput + "{} | Most expensive borough: {} \n       Least expensive borough: {}\n".format(key, maxPropertyPrices[key], minPropertyPrices[key])
        print("{}:\tMost expensive borough: {}. \n\tLeast expensive borough: {}.\n").format(key, maxPropertyPrices[key], minPropertyPrices[key])

    #   Output borough statistics to file
    output = "Borough\t| Year | Average Price\n\n".expandtabs(25)
    for borough in pricePerBoroughOverTime:
        for key, value in sorted(pricePerBoroughOverTime[borough].iteritems()):
            output = output + "{}\t| {} | {:00,.2f}\n".format(borough, key, pricePerBoroughOverTime[borough][key]).expandtabs(25)
    text_file = open("Output/London_Borough_Prices.txt", "w")
    text_file.write(output)
    text_file.close()

    #   Calculate percentage change in borough average prices
    print ("\nCalculating percentage change in average prices for London boroughs between {} and {}").format(minYear, maxYear)
    finalOutput = finalOutput + "\nBorough\t| Percentage Change in Price Between {} and {}\n".format(minYear, maxYear).expandtabs(25)
    boroughPercentageChange = calculatePercentageChangeInBoroughs(londonData, pricePerBoroughOverTime, minYear, maxYear)
    for key, value in sorted(boroughPercentageChange.iteritems(), key=lambda (k,v): (v,k)):
        if (not int(boroughPercentageChange[key]) == 0):
            finalOutput = finalOutput + "{}\t| {}%\n".format(key, round(boroughPercentageChange[key], 2)).expandtabs(25)
            print("{}\t{}%").format(key, round(boroughPercentageChange[key], 2)).expandtabs(30)
    boroughPercentageChange = []

    #   Calculate year by year percentage price change
    print ("\nCalculating year by year percentage change")
    yearByYearPercentageChange = calculateYearByYearPercentageChange(londonData, meanPricePerYear)
    finalOutput = finalOutput + "\nYear\t| Percentage Change\n".expandtabs(25)
    for years in sorted(yearByYearPercentageChange):
        finalOutput = finalOutput + "{}\t| {}%\n".format(years, round(yearByYearPercentageChange[years], 2)).expandtabs(25)
        print("{}\t{}%").format(years, round(yearByYearPercentageChange[years], 2)).expandtabs(30)

    #   Calculate average percentage change year by year
    sumValue = 0
    prices = []
    for year in yearByYearPercentageChange:
        sumValue = yearByYearPercentageChange[year] + sumValue
        prices.append(yearByYearPercentageChange[year])
    averageChangeYearByYear = sumValue / len(yearByYearPercentageChange)
    trimmedPercentageChange = trimmedMean(sorted(prices), 80)
    prices = []

    print("Average percentage change:\t{}%").format(round(averageChangeYearByYear), 2).expandtabs(30)
    print("Trimmed percentage change:\t{}%").format(round(trimmedPercentageChange), 2).expandtabs(30)
    finalOutput = finalOutput + ("Average percentage change:\t{}%\n").format(round(averageChangeYearByYear), 2).expandtabs(30)
    finalOutput = finalOutput + ("Trimmed percentage change:\t{}%\n").format(round(trimmedPercentageChange), 2).expandtabs(30)

    #   Predict future prices using average percentage change for mean price values
    print ("\nCalculating future mean prices using average percentage change")
    currentPrice = meanPricePerYear[maxYear]
    decimalChange = averageChangeYearByYear / 100
    currentPrice = round(currentPrice + (currentPrice * (decimalChange)), 2)
    currentYear = int(maxYear) + 1
    meanPricePerYear.update({ currentYear : currentPrice })
    for index in range(6):
        if index > 0:
            currentYear = currentYear + 1
            currentPrice = round(currentPrice + (currentPrice * (decimalChange)), 2)
            meanPricePerYear.update({ currentYear : currentPrice })

    finalOutput = finalOutput + "\nYear | Mean Price of Sales\n"
    for key, value in sorted(meanPricePerYear.iteritems(), key=lambda (k,v): (v,k)):
        if int(key) > int(maxYear):
            print ("{} {}".format(key, "\t{:00,.2f} GBP (Predicted)".format(meanPricePerYear[key]))).expandtabs(30)
            finalOutput = finalOutput + ("{} | {}".format(key, "{:00,.2f} GBP (Predicted)\n".format(meanPricePerYear[key]))).expandtabs(30)
        else:
            print ("{} {}".format(key, "\t{:00,.2f} GBP".format(meanPricePerYear[key]))).expandtabs(30)
            finalOutput = finalOutput + ("{} | {}".format(key, "{:00,.2f} GBP\n".format(meanPricePerYear[key]))).expandtabs(30)

    #   Calculate range of prices in London Boroughs
    print ("\nCalculating price ranges in London boroughs")
    finalOutput = finalOutput + "\nBorough\t| Range of Sale Prices\n".expandtabs(25)
    boroughRange = calculateRangeInBoroughs(londonData)
    for key, value in sorted(boroughRange.iteritems(), key=lambda (k,v): (v,k)):
        finalOutput = finalOutput + "{}\t| {}\n".format(key, "{:00,.2f} GBP".format(value)).expandtabs(25)
        print ("{} {}".format(key, "\t{:00,.2f} GBP".format(value))).expandtabs(30)

    #   Calculate number of million pound sales in boroughs
    print ("\nCalculating number of million pound property sales across London Boroughs")
    finalOutput = finalOutput + "\nBoroughs\t| Range of Sale Prices\n".expandtabs(25)
    millionPoundSales = numberOfMillionPoundSales(londonData)
    for key, value in sorted(millionPoundSales.iteritems(), key=lambda (k,v): (v,k)):
        finalOutput = finalOutput + "{}\t| {}\n".format(key, "{:00,.2f} GBP".format(value)).expandtabs(25)
        print ("{}\t{}".format(key, value)).expandtabs(30)

    #   Predict future prices using average percentage change for median price values
    print ("\nCalculating future median prices using average percentage change")
    yearByYearPercentageChange = calculateYearByYearPercentageChange(londonData, medianPricePerYear)
    sumValue = 0
    prices = []
    for year in yearByYearPercentageChange:
        sumValue = yearByYearPercentageChange[year] + sumValue
        prices.append(yearByYearPercentageChange[year])
    averageChangeYearByYear = sumValue / len(yearByYearPercentageChange)
    trimmedPercentageChange = trimmedMean(sorted(prices), 80)
    prices = []
    decimalChange = averageChangeYearByYear / 100
    currentPrice = medianPricePerYear[maxYear]
    currentPrice = round(currentPrice + (currentPrice * (decimalChange)), 2)
    currentYear = int(maxYear) + 1
    medianPricePerYear.update({ currentYear : currentPrice })
    for index in range(6):
        if index > 0:
            currentYear = currentYear + 1
            currentPrice = round(currentPrice + (currentPrice * (decimalChange)), 2)
            medianPricePerYear.update({ currentYear : currentPrice })

    finalOutput = finalOutput + "\nYear | Median Price of Sales\n"
    for key, value in sorted(medianPricePerYear.iteritems(), key=lambda (k,v): (v,k)):
        if int(key) > int(maxYear):
            print ("{} {}".format(key, "\t{:00,.2f} GBP (Predicted)".format(medianPricePerYear[key]))).expandtabs(30)
            finalOutput = finalOutput + ("{} | {}".format(key, "{:00,.2f} GBP (Predicted)\n".format(medianPricePerYear[key]))).expandtabs(30)
        else:
            print ("{} {}".format(key, "\t{:00,.2f} GBP".format(medianPricePerYear[key]))).expandtabs(30)
            finalOutput = finalOutput + ("{} | {}".format(key, "{:00,.2f} GBP\n".format(medianPricePerYear[key]))).expandtabs(30)

    text_file = open("Output/London_Sales_Basic.txt", "w")
    text_file.write(finalOutput)
    text_file.close()

    pause("\nPress the enter key to continue...")

#   Program entry point
if __name__ == "__main__":
    main()
