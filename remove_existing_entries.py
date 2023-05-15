import pandas as pd
from datetime import datetime, timedelta
import re
import os

#Make sure you have installed the wheel and pandas packages in order to run this script
#Using ubuntu on WSL
#sudo python3 -m pip install wheel
#sudo python3 -m pip install pandas

#-----------------------------------------
# The purpose of this script is to generate a list of email that do not include existing contacts in the
# Mautic or the customers list. In other words, a new list to add as new contacts to Mautic, where
# otay.csv is the full list of contacts downloaded from the chamber. 
# STEPS
# STEP 1: Read the otay new list
# STEP 2: Read the mautic existing list
# STEP 3: Read the customers file
# STEP 4: Remove existing emails in mautic from the new list 
# STEP 5: Remove customers from the new otay list, so we can get a list otay emails that do not include existing customers
# STEP 6: Write the final list without customers and without existing emails to a new csv file: NewContacts_NONC.csv
#-----------------------------------------

# Read the CSV file into a DataFrame
df1 = pd.read_csv('otay.csv')
df2 = pd.read_csv('mautic.csv')
df3 = pd.read_csv('customers.csv')


#REMOVE OLD EMAILS FROM THE NEW OTAY LIST
# Identify rows in df1 that are already present in df2
# Identify rows in otay.csv that are already present in mautic.csv
df1_duplicates = df1[df1['email'].isin(df2['email'])]

print ("Here are the duplicates in the new list: df1_duplicates")
print (df1_duplicates)

# Remove the identified rows from df1
df1 = df1[~df1['email'].isin(df1_duplicates['email'])]

# Write the DataFrame back to the CSV file
df1.to_csv('otay_no_mautic.csv', index=False, header=False)



#REMOVE CUSTOMERS FROM THIS LIST 
df4 = pd.read_csv('otay_no_mautic.csv')
df4.columns = ["email", "Name", "Phone"]
df4.to_csv('otay_no_mautic.csv', index=False)

print ("Done adding the columns")

# Identify rows in df4 that are already present in df3
# Identify rows in otay_no_mautic.csv that are already present in customers.csv
df4_duplicates = df4[df4['email'].isin(df3['ContactEmail'])]

print ("Here are the customers in the new list: df4_duplicates")
print (df4_duplicates)

# Remove the identified rows from df4
df4 = df4[~df4['email'].isin(df4_duplicates['email'])]

print ("Here are the list of otay no mautic without customers")
print (df4)

# Write the DataFrame back to the CSV file
df4.to_csv('NewContacts_NMNC.csv', index=False)
print(df4)

# Split the "Name" column into two.
# Make it so that it only looks at the first space. 
df4[['lastname', 'firstname']] = df4.Name.str.split(' ', n=1, expand = True)


# Drop column 1 an 2 on the 
# Where 1 is the axis number (0 for rows and 1 for columns.)
df4 = df4.drop(df4.columns[[1, 2]], axis=1)

# Add the require columns: CONVERTED, CUSTOMER, ACCOUNT_NAME
df4['CONVERTED']='NO'
df4['CUSTOMERS']='NO'
df4['ACCOUNT_NAME']='FASTSIGNS69501'

# Write the DataFrame back to the CSV file
df4.to_csv('NewContacts_NMNC.csv', index=False)


# Copy the files to the S3 bucket
#os.system('aws s3 cp s3://00fastsignsreports ./ --recursive')
os.system('aws s3 cp ./NewContacts_NMNC.csv s3://00fastsignsreports')
