import csv
import numpy as np

#   Pause program command line with custom message
def pause(message):
    programPause = raw_input(message)

#   Read CSV file and store in multidimensional array
def loadCSV(filename):
    print(filename)
    price = []
    dateProcessed = []
    postcode = []

    #   Select row elements to store in array
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            price.append(int(row['price']))
            dateProcessed.append(row['date_processed'])
            postcode.append(row['post_code'])

    return [postcode, price, dateProcessed];

def main():
    print("\n\nAnalysis of London Property Sales\n")
    print("Reading data files...")
    dataGroup1 = loadCSV("London Year_1995-2000.csv")
    dataGroup2 = loadCSV("London Year_2001-2006.csv")
    dataGroup3 = loadCSV("London Year_2007-2012.csv")
    dataGroup4 = loadCSV("London Year_2013-2014.csv")

    #   Get average price of each data group
    sum1 = sum(dataGroup1[1])
    average1 = sum1 / len(dataGroup1[1])
    sum2 = sum(dataGroup2[1])
    average2 = sum2 / len(dataGroup2[1])
    sum3 = sum(dataGroup3[1])
    average3 = sum3 / len(dataGroup3[1])
    sum4 = sum(dataGroup4[1])
    average4 = sum4 / len(dataGroup4[1])
    average1 = ('{:20,.2f}'.format(average1))
    average2 = ('{:20,.2f}'.format(average2))
    average3 = ('{:20,.2f}'.format(average3))
    average4 = ('{:20,.2f}'.format(average4))
    print("Average Price of London Properties Sold Between 1995 and 2000:\n" + str(average1))
    print("Average Price of London Properties Sold Between 2001 and 2006:\n" + str(average2))
    print("Average Price of London Properties Sold Between 2007 and 2012:\n" + str(average3))
    print("Average Price of London Properties Sold Between 2013 and 2014:\n" + str(average4))

    pause("\nPress the enter key to continue...")

#   Program entry point
if __name__ == "__main__":
    main()
