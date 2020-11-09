initiate master list

pdf_data_to_xml_function(file, query)
    initiate query list
    open file
    break by line
    for each line containing query
        split line by space
        add index of desired value to query list
    add query list to master list

openpyxl_spreadsheet_insert_func(index_in_sublists, start_position_in_sheet)
    for each sublist in masterlist:
        take index_in_sublists value
        insert at start_position_in_sheet
        start_position_in_sheet = start_position_in_sheet + 1

make an accuracy check- possibly turn query list into tuples with paycode to check
spreadsheet row for paycode to be correct before inserting value into spreadsheet
if incorrect, throw an error and return what the incorrect paycode was so I can see
how to change it.


open in lines before searching for terms

with open("/home/seth/PycharmProjects/SettlementReview/CurrentSettlements/settlement1.txt", "r") as f:
...     for line in f:
...             print(line)