import PyPDF2
import csv
import os

# Prompt for search directory
directory = input(r"Paste directory that you would like to search: ")

#Prompt for search terms
qty = int(input("How many terms would you like to search for simultaneously? "))

terms = [] # Container for search terms, will be iterated

# Prompt for multiple search terms
for i in range(qty):
    terms.append(input("Enter string you would like to search PDF's for: "))

# Define output CSV file
output = input("Enter description of output text file. ") + ".csv"

# Write summary of inputs to file
with open(output, 'w', newline = '') as csvfile:
    writer = csv.writer(csvfile, dialect='excel')
    csvfile.write('Search Directory: \n')
    csvfile.write(directory + '\n')
    csvfile.write("\nSearch Terms: \n")
    for term in terms:
        writer.writerow([term])
    csvfile.write("\nResults matching at least one term: \n")
    csvfile.close()

# Set up container for matching filenames
filenames = []

# Define fieldnames for CSV writing
fieldnames = ['Filename', 'Location']

# Walk specified directory looking for PDF files to search
for root, dirs, files in os.walk(directory):
    for name in files:
        
        try:
            # create a pdf reader object
            path_to_pdf = os.path.join(root, name)
            file = open(path_to_pdf, 'rb')
            pdfReader = PyPDF2.PdfFileReader(file)
            print(f"Found a PDF. {name}")

            # Create a page object
            pageObj = pdfReader.getPage(0)

            # extract text from page
            text = pageObj.extractText()

            # Set match flag to FALSE, only want matching file written to output ONCE
            found = 0

            # Iterage through search terms in current PDF file text
            for i in range(qty):
                check = text.find(terms[i])
                if check != -1:
                    found = 1
            
            # Found a match, write it to filenames
            if found == 1:
                entry = {'Filename' : name, 'Location' : path_to_pdf}
                filenames.append(entry)
            file.close()

        except:
            print(f"Skipped {name}")

# Write results to CSV file
with open(output, 'a', newline = '') as f:
    writer = csv.DictWriter(f, fieldnames = fieldnames, extrasaction = 'ignore')
    writer.writeheader()
    for data in filenames:
        writer.writerow(data)
    f.close()