import pandas as pd
import numpy as np

COL_CARE = ["loan_amnt", "loan_status", "zip_code", "annual_inc", "term", "int_rate",
            "grade", "purpose", "issue_d", "addr_state"]

def lookup(ts):
    dates = {date: pd.to_datetime(date) for date in ts.unique()}
    return ts.map(dates)

# def process_geo(data):
#     import zipcodes

#     loan_amnt_zip = data.groupby(['addr_state','zip_code']).agg({'loan_amnt': np.mean, 'annual_inc': np.mean}).reset_index()
#     loan_amnt_zip.head()

#     def convertzip_county(zip):
#         zip = zip[0:3]
#         county = zipcodes.similar_to(zip)
#         if county:
#             county = county[0]['state']
#         else: 
#             county = ""
#             return county


#     loan_amnt_zip['county'] = loan_amnt_zip['zip_code'].apply(convertzip_county)
#     loan_amnt_zip_new = loan_amnt_zip.loc[loan_amnt_zip.addr_state == loan_amnt_zip.county]

#     data["addr_state"] = "US." + data["addr_state"]
#     data = data.groupby(["issue_d", "addr_state"])[["loan_amnt"]].agg(np.sum).reset_index() 
#     data.to_csv("geo_date.csv", index=False)

def process_stats(data):
    data = data.groupby(data['issue_d'].dt.to_period('Q'))[["loan_amnt"]].agg(np.sum).reset_index() 
    data.to_csv("stats_data.csv", index=False)

def process_time(data):
    data["date"] = data.issue_d.map(lambda x: x.strftime('%Y-%m'))
    data = data.groupby(["date", "addr_state"])[["loan_amnt"]].agg(np.sum).reset_index() 
    data["value"] = data["loan_amnt"]
    data.colunms = ["date", "state", "loan_amnt"]
    data.to_csv("time_data.csv", index=False)

def run():
    raw_data = pd.read_csv("loan.csv", usecols=COL_CARE)
    raw_data['issue_d'] = lookup(raw_data['issue_d'])

    process_time(raw_data) 
    #process_geo(raw_data)
    #process_stats(raw_data)
    
    

if  __name__ == "__main__":
    run()