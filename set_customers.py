import pandas as pd
from datetime import datetime, timedelta
import re
import os

#Make sure you have installed the wheel and pandas packages in order to run this script
#Using ubuntu on WSL
#sudo python3 -m pip install wheel
#sudo python3 -m pip install pandas

#-----------------------------------------
# The purpose of this script is to identify contacts in MAUTIC that are already customers. 
#
# This script updates the mautic list to include the "CUSTOMERS", "CONVERTED" and "ACCOUNT_NAME".
# It also updates the "CUSTOMERS" column to "YES", for emails entries in the mautic list
# that also exits on the customers.csv file. 
#
# STEPS
# STEP 1: Read the customers list
# STEP 2: Read the mautic existing list
# STEP 3: Add the columns CUSTOMERS, ACCOUT and
# STEP 3: Identify the customers on the mautic list and set the CUSTOMERS tab to YES
#
# How to run: 
# python set_customers.py
#-----------------------------------------

# Read the CSV file into a DataFrame
df1 = pd.read_csv('customers.csv')
df2 = pd.read_csv('mautic.csv')

# Add the require columns: CONVERTED, CUSTOMER, ACCOUNT_NAME to df2
# Add the require columns: CONVERTED, CUSTOMER, ACCOUNT_NAME to mautic
df2['CONVERTED']='NO'
df2['CUSTOMERS']='NO'
df2['ACCOUNT_NAME']='FASTSIGNS69501'

# Write the DataFrame back to the CSV file
df2.to_csv('mautic_with_customers_set.csv', index=False )

#REMOVE OLD EMAILS FROM THE NEW OTAY LIST
# Identify rows in df1 that are already present in df2
# Identify rows in customers.csv that are already present in mautic.csv
df1_duplicates = df1[df1['ContactEmail'].isin(df2['email'])]
df2_duplicates = df2[df2['email'].isin(df1['ContactEmail'])]

print ("Here are the duplicates in the new list: df2_duplicates")
print (df2_duplicates)

df2.to_csv('mautic_with_customers_set.csv', index=False )


# Find all columns where CUSTOMERS = NO and change them to Customers = MAYBE
#df2.loc[df2['CUSTOMERS'] == 'NO', 'CUSTOMERS'] = "MAYBE"

# Find all columns where CUSTOMERS = Match Email List and change them to Customers = YES
# If Condition, then set "column" to "Value
# if loc[if-Condition, Set-Column] = 'NewValue'
df2.loc[df2['email'].isin(df1['ContactEmail']), 'CUSTOMERS'] = 'YES'


# Write the DataFrame back to the CSV file
df2.to_csv('mautic_with_customers_set.csv', index=False )

# Copy the files to the S3 bucket
os.system('aws s3 cp ./mautic_with_customers_set.csv s3://00fastsignsreports')
