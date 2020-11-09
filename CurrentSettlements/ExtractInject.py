import pdftotext
import os
import openpyxl

driver_info = []
holder_list = []

print('\n\n\n    SETTLEMENT REVIEW \n\n\n')

pdf_directory = "/home/seth/PycharmProjects/SettlementReview/CurrentSettlements"
pdf_list = next(os.walk(pdf_directory))[2]

#convert pdf to txt
for each_pdf in pdf_list:
    extension = str(each_pdf[-4:])
    if extension == '.pdf':
        with open(each_pdf, "rb") as f:
            pdf = pdftotext.PDF(f)
        with open(str('current.txt'), "w") as f:
            f.write("\n\n".join(pdf))

txt_file = "/home/seth/PycharmProjects/SettlementReview/CurrentSettlements/current.txt"
with open(txt_file, "r") as f:
    text = f.read()
    lines = text.splitlines()

    page_1_indices = []
    for (i, j) in enumerate(lines):
        if "Page 1" in j:
            page_1_indices.append(i)

    #PAYEE CODE, LAST NAME, FIRST NAME
    words_in_lines = []
    for each in lines:
        words_in_lines.append(each.split())

    for each in page_1_indices:
        holder_list = []
        payee_code = words_in_lines[each+5][1]
        holder_list.append(payee_code)

        if words_in_lines[each+5][3] == "JR," or words_in_lines[each+5][3] == "SR," \
                or words_in_lines[each+5][3] == "DE" or words_in_lines[each+5][3] == "LA" \
                or words_in_lines[each+5][3] == "II" or words_in_lines[each+5][3] == "III":
            driver_first_name = words_in_lines[each+5][4]
            holder_list.append(driver_first_name)
        else:
            driver_first_name = words_in_lines[each+5][3]
            holder_list.append(driver_first_name)

        driver_last_name = words_in_lines[each+5][2]
        holder_list.append(driver_last_name[:-1])

        driver_info.append(holder_list)

    #GROSS EARNING
    gross_indices = [i for i,s in enumerate(lines) if "GROSS" in s]
    for each in gross_indices:
        page_1_indices.append(each)
        page_1_indices.sort()
        target_driver = page_1_indices.index(each)-1
        if lines[each].split()[-1][0] == "-":
            driver_info[target_driver].append(float(lines[each].split()[-1].replace("$", "").replace(",", "")))
        else:
            driver_info[target_driver].append(float(lines[each].split()[-1].replace("$", "").replace(",", "")))
        page_1_indices.pop(target_driver)

    for i in driver_info:
        if len(i) < 4:
            i.append("---")
        #print(i)

    #NET PAY
    order_indices = [i for i,s in enumerate(lines) if "NET PAY" in s and "DRIVER" not in s]
    if order_indices[-1] > page_1_indices[-1]:
        if lines[order_indices[-1]].split()[-1][0] == "-":
            driver_info[-1].append(float(lines[order_indices[-1]].split()[-1].replace("$", "").replace(",", "")))
        else:
            driver_info[-1].append(float(lines[order_indices[-1]].split()[-1].replace("$", "").replace(",", "")))
    for each in range(len(order_indices)-1):
        if order_indices[each] >= page_1_indices[each] and order_indices[each] < page_1_indices[each+1]:
            if lines[order_indices[each]].split()[-1][0] == "-":
                driver_info[each].append(float(lines[order_indices[each]].split()[-1].replace("$", "").replace(",", "")))
            else:
                driver_info[each].append(float(lines[order_indices[each]].split()[-1].replace("$", "").replace(",", "")))
    for i in driver_info:
        if len(i) < 5:
            i.append("---")
        #print(i)

    #TOTAL ORDERS
    order_indices = [i for i,s in enumerate(lines) if "ORDERS:" in s]
    if order_indices[-1] > page_1_indices[-1]:
        driver_info[-1].append(float(lines[order_indices[-1]].split()[-1]))
    for each in range(len(order_indices)-1):
        if order_indices[each] >= page_1_indices[each] and order_indices[each] < page_1_indices[each+1]:
            driver_info[each].append(float(lines[order_indices[each]].split()[-1]))
    for i in driver_info:
        if len(i) < 6:
            i.append("---")
        #print(i)

    #LOADED MILES
    order_indices = [i for i, s in enumerate(lines) if "LOADED MILES:" in s]
    if order_indices[-1] > page_1_indices[-1]:
        driver_info[-1].append(float(lines[order_indices[-1]].split()[-1]))
    for each in range(len(order_indices) - 1):
        if order_indices[each] >= page_1_indices[each] and order_indices[each] < page_1_indices[each + 1]:
            driver_info[each].append(float(lines[order_indices[each]].split()[-1]))
    for i in driver_info:
        if len(i) < 7:
            i.append("---")
        # print(i)

    #FUEL TOTALS - driver_info[8]
    outside_fuel_indices = [i for i,s in enumerate(lines) if "Deduction" in s and "Fuel" in s]
    terminal_fuel_indices = [i for i,s in enumerate(lines) if "Fuel Purch" in s]
    all_fuel = outside_fuel_indices + terminal_fuel_indices
    for each in all_fuel:
        page_1_indices.append(each)
        page_1_indices.sort()
        target_driver = page_1_indices.index(each)
        if lines[each].split()[-1][0] == "-":
            driver_info[target_driver].append(float(lines[each].split()[-2].replace("$", "").replace(",", "")))
        else:
            driver_info[target_driver].append(float(lines[each].split()[-2].replace("$", "").replace(",", "")))
        page_1_indices.pop(target_driver)

    for driver in driver_info:
        if len(driver) > 8:
            driver[7] = round(sum(driver[7:]), 2)
            del driver[8:]
        elif len(driver) < 8:
            driver.append("---")

    #TAGS
    tag_indices = [i for i,s in enumerate(lines) if "TAG DEPOSITS" in s and "2013.0" in s]
    for each in tag_indices:
        if "DEPOSITS:" in lines[each+2]:
            each = each+4
        else:
            each = each+1
        page_1_indices.append(each)
        page_1_indices.sort()
        target_driver = page_1_indices.index(each)-1
        driver_info[target_driver].append(float(lines[each].split()[-1].replace("$", "").replace(",", "")))
        page_1_indices.pop(target_driver)

    for i in driver_info:
        if len(i) < 9:
            i.append("---")
        #print(i)

    #2290's
    tag_indices = [i for i,s in enumerate(lines) if "2290'S" in s and "2010.0" in s]
    for each in tag_indices:
        if "DEPOSITS:" in lines[each+2]:
            each = each+4
        else:
            each = each+1
        page_1_indices.append(each)
        page_1_indices.sort()
        target_driver = page_1_indices.index(each)-1
        driver_info[target_driver].append(float(lines[each].split()[-1].replace("$", "").replace(",", "")))
        page_1_indices.pop(target_driver)

    for i in driver_info:
        if len(i) < 10:
            i.append("---")
        #print(i)

    #MAIN ESCROW PLACEHOLDER
    for driver in driver_info:
        driver.append("Escrow")

    #FUEL DEPOSITS
    for driver in driver_info:
        driver.append("fuel")

    #REPAIR ESCROW
    tag_indices = [i for i,s in enumerate(lines) if "DRIVER REPAIR ESCROW" in s and "2014.0" in s]
    for each in tag_indices:
        if "DEPOSITS:" in lines[each+2]:
            each = each+4
        else:
            each = each+1
        page_1_indices.append(each)
        page_1_indices.sort()
        target_driver = page_1_indices.index(each)-1
        driver_info[target_driver].append(float(lines[each].split()[-1].replace("$", "").replace(",", "")))
        page_1_indices.pop(target_driver)

    for i in driver_info:
        if len(i) < 13:
            i.append("---")
        #print(i)

    #ELD ESCROW
    for driver in driver_info:
        driver.append("eld")


    #xlsx SECTION
    wb = openpyxl.load_workbook("CLEB.SETTLEMENT.SHEET.xlsx")
    curr_sheet = wb.active
    new_sheet = wb.copy_worksheet(curr_sheet)
    sheets=wb._sheets
    new_sheet = sheets.pop(-1)
    sheets.insert(0, new_sheet)
    new_sheet.title = "10-09-20"
    new_sheet["A1"] = "10/09/20"
    blank_col_list = [3, 5, 7, 8, 10, 11, 12, 13, 14, 15, 16]
    for row in range(100):
        for col in blank_col_list:
            new_sheet[row+3][col].value = ""
    for row in range(len(driver_info)):
        row = new_sheet[row+3]
        for driver in driver_info:
            if row[1].value == driver[0]:
                row[3].value = driver[3]
                row[5].value = driver[4]
                row[7].value = driver[5]
                row[8].value = driver[6]
                row[10].value = driver[7]
                row[11].value = driver[8]
                row[12].value = driver[9]
                row[13].value = driver[10]
                row[14].value = driver[11]
                row[15].value = driver[12]
                row[16].value = driver[13]

    wb.save("TESTING2.xlsx")

print("SETLEMENT REVIEW IS NOW COMPLETE")

""" MAIN ESCROW & FUEL DEPOSITS & ELD ESCROW
    #MAIN ESCROW
    tag_indices = [i for i,s in enumerate(lines) if "ESCROW-OTHER" in s and "2015.0" in s]
    for each in tag_indices:
        if "FUEL" in lines[each+2]:
            each = each+1
        elif "NEW BALANCE" in lines[each+4]:
            each = each+4
        elif "FUEL" in lines[each+13]:
            each = each+12
        elif "New Balance" in lines[each+15]:
            each = each+15
        page_1_indices.append(each)
        page_1_indices.sort()
        target_driver = page_1_indices.index(each)-1
        driver_info[target_driver].append(float(lines[each].split()[-1].replace("$", "").replace(",", "")))
        page_1_indices.pop(target_driver)

    for i in driver_info:
        if len(i) < 11:
            i.append("---")
        #print(i)
        
    #FUEL DEPOSITS
    tag_indices = [i for i,s in enumerate(lines) if "FUEL DEPOSITS" in s and "2012.0" in s]
    for each in tag_indices:
        if "DEPOSITS:" in lines[each+2]:
            each = each+4
        else:
            each = each+1
        page_1_indices.append(each)
        page_1_indices.sort()
        target_driver = page_1_indices.index(each)-1
        driver_info[target_driver].append(float(lines[each].split()[-1].replace("$", "").replace(",", "")))
        page_1_indices.pop(target_driver)

    for i in driver_info:
        if len(i) < 12:
            i.append("---")
        #print(i)

    #ELD ESCROW
    tag_indices = [i for i,s in enumerate(lines) if "DRIVER ESCROW-ELD" in s and "2016.0" in s]
    for each in tag_indices:
        if "DEPOSITS:" in lines[each+2]:
            each = each+4
        else:
            each = each+1
        page_1_indices.append(each)
        page_1_indices.sort()
        target_driver = page_1_indices.index(each)-1
        driver_info[target_driver].append(float(lines[each].split()[-1].replace("$", "").replace(",", "")))
        page_1_indices.pop(target_driver)

    for i in driver_info:
        if len(i) < 14:
            i.append("---")
        #print(i)

        """
"""

    line_delete_keywords = ['Paid Settlement Summary', 'Tutle & Tutle Trucking', '(817) 556-2131',
                            'Check #', 'Pay period', 'Email', 'Origin',
                            '---------------------------------------------------',
                            '___________________________________________________']
    for line in lines:
        if any(word in line for word in line_delete_keywords):
            del line"""
"""
#formulas
if driver[7] != "---" and driver[7] > 0:
    row[4].value = driver[3]/driver[7]
    row[6].value = driver[5]/driver[7]
    row[9].value = driver[8]/driver[7]
else:
    row[4].value = 0
    row[6].value = 0
    row[9].value = 0
"""
"""     GROSS SECTION HALF ASS WORKING
        for each2 in range(len(page_1_indices)-1):
            if gross_indices[each] >= page_1_indices[each2] and gross_indices[each] < page_1_indices[each2+1]:
                if lines[gross_indices[each]].split()[-1][0] == "-":
                    driver_info[each].append(float(lines[gross_indices[each-2]].split()[-1][2:].replace(",", "")))
                else:
                    driver_info[each].append(float(lines[gross_indices[each-2]].split()[-1][1:].replace(",", "")))
"""

"""
        #print(new_sheet[row+3][1].value)
        #print(driver_info[row][0])
        if new_sheet[row+3][1].value == driver_info[row][0]:
            new_sheet[row+3][3].value = driver_info[row][3]
            new_sheet[row+3][5].value = driver_info[row][4]
            new_sheet[row+3][7].value = driver_info[row][5]
            new_sheet[row+3][8].value = driver_info[row][6]
    wb.save("TESTING1.xlsx")
    wb.close()
"""



    #TOTAL MILES
"""    order_indices = [i for i, s in enumerate(lines) if "LOADED MILES" in s]
    if order_indices[-1] > page_1_indices[-1]:
        driver_info[-1].append(lines[order_indices[-1]].split()[-1])
    for each in range(len(order_indices) - 1):
        if order_indices[each] >= page_1_indices[each] and order_indices[each] < page_1_indices[each + 1]:
            driver_info[each].append(lines[order_indices[each]].split()[-1])
    for i in driver_info:
        if len(i) < 7:
            i.append("---")
        print(i)
"""

"""        
WORKING    #GROSS PER ORDER
    for i in driver_info:
        gross = i[3]
        orders = i[5]
        if gross != "---" and orders != "---":
            gross = float(i[3][1:].replace(',',''))
            orders = float(i[5])
            if gross > 0 and orders > 0:
                #print(i[0], round(int(gross)/int(orders), 2))
"""

"""
    for each in lines:
        if "GROSS" in each:
            each_index = lines.index(each)
            page_1_indices.append(each_index)
            page_1_indices.sort()
            key_index = page_1_indices.index(each_index)-1
            driver_info[key_index].append(each.split()[-1])
            print(driver_info[key_index])
        else:
            pass
    for i in driver_info:
        if len(i) < 4:
            i.append("---")
        print(i)
"""
"""
    #GROSS PAY
    for line in lines:
        if "GROSS EARNINGS:" in line:
            line_ind = lines.index(line)
            for i in range(len(page_1_indices)-1):
                if line_ind >= page_1_indices[i] and line_ind < page_1_indices[i+1] and \
                        len(driver_info[i]) < 4:
                    driver_info[i].append(line.split()[-1])

    #NET PAY BELOW (RELATIVE TO GROSS)
    for line in lines:
        if "NET PAY:" in line and "DRIVER" not in line:
            line_ind = lines.index(line)
            for i in range(len(page_1_indices)-1):
                if line_ind >= page_1_indices[i] and line_ind < page_1_indices[i+1] and \
                        len(driver_info[i]) < 5:
                    driver_info[i].append(line.split()[-1])
    for i in driver_info:
        if len(i) < 5:
            i.append("---")
"""

"""            line_ind = lines.index(line)
            order_total = line.split()[-1]
            #print(order_total)
            for i in range(len(page_1_indices)):
                print(i)
                print(line_ind)
                print(page_1_indices[i])
                print(page_1_indices[i+1])
                print(" ")
                if line_ind >= page_1_indices[i] and line_ind < page_1_indices[i+1] and \
                        len(driver_info[i]) < 6:
                    driver_info[i].append(order_total)
                    print(driver_info[i])
                    print(" ")
                    #print(line_ind)
                    #print(page_1_indices[i])
                    #print(page_1_indices[i+1])
                    #print(' ')
                else:
                    continue
    for i in driver_info:
        if len(i) < 6 and i[3] != "---":
            i.append("---")
"""
#below comparing two
#    print(lines[7647].split())
#    print(lines[10315].split())
#    for i in driver_info:
#        if i[0] == "KANYOROP" or i[0] == "MORENO1":
#            print(i)

# NORMAL PRINT
#    for i in driver_info:
#        print(i)

#    for (i,j) in enumerate(driver_info):
#        print(i, j)

"""
    for (i,j) in enumerate(lines):
        if "GROSS" in j:
            print(i)
#            print(j.split()[-1])
            if i < len(driver_info):
                print(i)
                print(driver_info[i])
#               driver_info[i].append(j.split()[-1])


#            grossind = lines.index("GROSS")
#            grossval = grossind.split()[-1]
#            holder_list.append(grossval)
#            print(grossind)
#            print(grossval)


            Now search for each parameter between the first two page 1 indices
            put them into a list and if no result a zero into the list then append
            that list into the master list.
            After that we will have a list of all info from each settle ment or if not then zeroes. 
            Next step is to put the sublists indices into a spreadsheet.
        *** Before inserting them into the spreadsheet we need to build the spreadsheet format first ***
"""













