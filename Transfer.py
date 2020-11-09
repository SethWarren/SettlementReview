import pdftotext
import os

#  Need to wrap this up to cover multiple files at once!!
#  Use Covergrab for reference

driverinfo = []

print('\n\n\n    SETTLEMENT REVIEW \n\n\n')
pdf_directory = str(input('Please enter the file path for the Settlements: \n'))
#   Line below is set directory path when we are not trying to walk through the folder.
#s1 = open("/home/seth/PycharmProjects/SettlementReview/CurrentSettlements/settlement1.txt")

pdf_list = next(os.walk(pdf_directory))[2]

for each_pdf in pdf_list:
    print(str(each_pdf))
    extension = str(each_pdf[-4:])
    if extension == '.pdf':
        with open(each_pdf, "rb") as f:
            pdf = pdftotext.PDF(f)
        with open(str('current.txt'), "w") as f:
            f.write("\n\n".join(pdf))
"""
for each_txt in pdf_list:
    extension = str(each_txt[-4:])
    if extension == '.txt':
        s1 = open(each_txt, "r")
        words = s1.read()
        words = words.split()
        #to rejoin test[1:3] = [''.join(test[1:3])]

        #for (i, item) in enumerate(words, start=1(optional)):
        #    print(i, item)
        #   Reconfigure below to pull the necessary information and add it to driverinfo
        #   specword = words.index("Search Query")
        #   specvalue = words[specword + 9] ## +9 may be different...
        #   There is no consistency between

        driverinfo.append(words[40])    #   payee code
        driverinfo.append(words[41])    #   Last name plus comma
        driverinfo.append(words[39])    #   First name

        grossind = words.index("GROSS")
        grossval = words[grossind + 2]
        driverinfo.append(grossval)

        netind = words.index("NET")
        netval = words[netind + 2]
        driverinfo.append(netval)

        orderind = words.index("ORDERS:")
        orderval = words[orderind + 1]
        driverinfo.append(orderval)

        mileind = words.index("MILES:")
        mileval = words[mileind + 1]
        driverinfo.append(mileval)

print(driverinfo)
"""