import pandas as pd
import csv
#Shriners uses APC codes, but they include something about Package/Line_Level idk what that is yet
def main():
    finaldf = pd.DataFrame(columns = ['Hospital', 'ProcedureCode','HCPCS', 'Code Code', 'Procedure Name', 'Affiliation', 'Cost'])
    with open("Shriners_Children's_Portland_standardcharges.csv",'r') as csvfile:
        next(csvfile)
        reader = csv.DictReader(csvfile)
        for row in reader:
            #For some reason the rows are processed as a dict with the same key and item value, the below just saves some space
            temprow = list(row.keys())
             #Finds commanilities here, idk if HCPCS should even be in its own section at this point
            #Columns five through nine are mandatory reported info, past that should be insurer specific information
            temp = ["Shriners Children's Hospital Portland", "N/A", temprow[0], "N/A" , temprow[1]]
            
            for i in range(10, len(temprow))
main()
    
