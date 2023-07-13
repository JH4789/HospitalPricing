import pandas as pd
import json
def specific_provider(in_out, num, df, data,rowid):
    for i in range(1, num):
        for j in data[in_out + "patient Payer Specific Charge " + str(i)]:
            try:
                temp = [38007, rowid, "DRG",j["Description"], None, None, None, j["MS-DRG"], None, None, None, None, None, None, None, None, None, None, None, None, "facility", in_out+"patient", "payer", j["Payer"], None, j["Payer Specific Negotiated Charge"], None, "Capitation", None,None]
            except:
                temp = [38007, rowid, "APC",j["Description"], None, None, None, None, None, None, None, None, None, j["APC"], None, None, None, None, None, None, "facility", in_out+"patient", "payer", j["Payer"], None, j["Payer Specific Negotiated Charge"], None, "Capitation", None,None]
            rowid+=1
            df.loc[len(df)] = temp
    return df, rowid
def min_max(minmax, in_out, df,data,rowid):
    for i in data[in_out+"patient De-identified " +minmax +"imum Negotiated Charge"]:
        try:
            temp = [38007, rowid, "DRG",i["Description"], None, None, None, i["MS-DRG"], None, None, None, None, None, None, None, None, None, None, None, None, "facility", in_out+"patient", minmax.lower(), None, None, i["De-Identified " + minmax + "imum Negotiated Charge"], None, "Capitation", None,None]

        except:
            temp = [38007, rowid, "APC",i["Description"], None, None, None, None, None, None, None, None, None, i["APC"], None, None, None, None, None, None, "facility", in_out+"patient", minmax.lower(), None, None, i["De-Identified " + minmax + "imum Negotiated Charge"], None, "Capitation", None,None]
        df.loc[len(df)] = temp
        rowid +=1
    return df, rowid
def gross(data, df, affil, addendum, rowid):
    for i in data["Gross Charges"]:
        if rowid >= 300:
            return df, rowid
        try:
            temp = [38007, rowid, "CDM",i["Description"], i["CDM Revenue Code"], i["Itemcode"], None, None, None, None, i["CDM Hcpcs"], None, None, None, None, None, None, None, None, None, "facility", "both", "gross", None, None, i["LEGACY EMANUEL MEDICAL CENTER"], None, "Capitation", None,None]
            temp1 = [38007, rowid+1, "CDM",i["Description"], i["CDM Revenue Code"], i["Itemcode"], None, None, None, None, i["CDM Hcpcs"], None, None, None, None, None, None, None, None, None, "facility", "both", "cash", None, None,  i["LEGACY EMANUEL MEDICAL CENTER Discount Cash Price"], None, "Capitation", None,None]
        except:
            temp = [38007, rowid, "CDM",i["Description"], i["CDM Revenue Code"], i["Itemcode"], None, None, None, None, None, None, None, None, None, None, None, None, None, None, "facility", "both", "gross", None, None, i["LEGACY EMANUEL MEDICAL CENTER"], None, "Capitation", None,None]
            temp1 = [38007, rowid+1, "CDM",i["Description"], i["CDM Revenue Code"], i["Itemcode"], None, None, None, None, None, None, None, None, None, None, None, None, None, None, "facility", "both", "cash", None, None,  i["LEGACY EMANUEL MEDICAL CENTER Discount Cash Price"], None, "Capitation", None,None]
        rowid +=2
        df.loc[len(df)] = temp
        df.loc[len(df)] = temp1
    return df, rowid
def main():
    with open('Raw/legacy_emanuel_medical_center_standardcharges.json','r') as file:
        data = json.load(file)
        df = pd.DataFrame(columns = ["hospital_id","row_id","line_type","description","rev_code","local_code","code","ms_drg","apr_drg","eapg","hcpcs_cpt","modifiers","thru","apc","icd","ndc","drug_hcpcs_multiplier","drug_quantity","drug_unit_of_measurement","drug_type_of_measurement","billing_class","setting","payer_category","payer_name","plan_name","standard_charge","standard_charge_percent", "contracting_method","additional_generic_notes","additional_payer_specific_notes"])
    rowid = 1
    df ,rowid =  gross(data, df, "Normal ", "", rowid)
    df, rowid =  min_max("Min","In", df, data, rowid)
    df, rowid =  min_max("Max","In", df, data,rowid)
    df, rowid =  min_max("Min", "Out", df, data,rowid)
    df, rowid =  min_max("Max", "Out", df, data,rowid)
    df, rowid =  specific_provider("In" , 41, df, data,rowid)
    df ,rowid =  specific_provider("Out", 44,df,data,rowid)
    #print(df)
    df.to_csv("/home/jayden/Code/HospitalsPortlandMetro/LegacyMedicalCenters/Complete/legacy_emanuel_medical_center_final.csv")
main()
