import pandas as pd
import numpy as np
import csv
#Shriners uses APC codes, but they include something about Package/Line_Level idk what that is yet
#^ Not true
def main():
    finaldf = pd.DataFrame(columns = ["hospital_id", "row_id","line_type","description","rev_code","local_code", "code","ms_drg","apr_drg","eapg","hcpcs_cpt","modifiers","thru","apc","icd","ndc","drug_hcpcs_multiplier","drug_quantity","drug_units_of_measurement","drug_type_of_measurement","billing_class","setting","payer_category","payer_name","plan_name","standard_charge","standard_charge_percent","contracting_method","additional_generic_notes","additional_payer_specific_notes"])
    exclusionlist = ["Code", "Description", "Type","Package/Line_Level"]
    rowid = 1
    with open("Raw/Shriners_Children's_Portland_standardcharges.csv",'r') as csvfile:
        
        reader = csv.DictReader(csvfile)
        next(reader)
        for row in reader:
            #For some reason the rows are processed as a dict with the same key and item value, the below just saves some space
            temprow = list(row.keys())
             #Finds commanilities here, idk if HCPCS should even be in its own section at this point
            #Columns five through nine are mandatory reported info, past that should be insurer specific information
            filtered = {k: v for k, v in row.items() if v != "N/A"}
            charges  = [i for i in list(filtered.keys()) if i not in exclusionlist]
            #print(charges)
            #This CSV includes a reference to a "Derived Contract Rate" that is neither the minimum or maximum
            charges = charges[:-1]
            for i in charges:
                
                temp = [383300, rowid, "CPT", filtered["Description"], None, None, None, None, None, None, filtered["Code"], None, None,None,None,None,None,None,None,None,"facility",filtered["Type"].lower(),i,i, None, row[i],None, "Capitation",filtered["Package/Line_Level"], None ]
                finaldf.loc[len(finaldf)] = temp
        #        print(temp)
                rowid +=1
        #Cleaning everything up
        finaldf["payer_category"].replace(["Discounted cash price","Gross charge","De-identified max contracted rate", "De-identified min contracted rate"],["cash","gross","max","min"], inplace = True)
        allowedlist = ["cash","gross","max","min"]
        finaldf = finaldf[finaldf.payer_category != "Derived contracted rate"]
        finaldf.loc[~finaldf["payer_category"].isin(allowedlist), "payer_category"] = "payer"
        finaldf["payer_name"].replace(["Discounted cash price","Gross charge","De-identified max contracted rate", "De-identified min contracted rate"],[None,None,None,None], inplace = True)
        #Not sure if the data being dropped above is valuable
        print(finaldf)
        finaldf.to_csv("Complete/shriners_childrens_hospital_portland_final.csv")
main()
    
