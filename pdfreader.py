import PyPDF2
import os

directory = input(r"Paste directory that you would like to search: ")
term = input("Enter string you would like to search PDF's for: ")
output = input("Enter description of output text file. ") + ".txt"

# create a pdf file object

filenames = []

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
            check = text.find(term)
            if check != -1:
                filenames.append(name)
            file.close()

        except:
            print(f"Skipped {name}")

with open(output, 'w') as f:
    for line in filenames:
        f.write(line)
        f.write('\n')

print(filenames)