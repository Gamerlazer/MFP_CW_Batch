import csv
import os
import datetime

print datetime.date.today()

# save files as Window Comma Separated (.csv)

sfdc_report_name = raw_input("What is the name of the SFDC report? (Don't include '.csv)")
recon_report_name = raw_input("What is the name of the recon report from last month? (Don't include '.csv)")
cc_trans_name = raw_input("What is the name of the cc transaction report you just pulled? (Don't include '.csv)")

### ----

cl_oppts = {}
with open(sfdc_report_name+'.csv', 'rU') as f1:
	report = csv.DictReader(f1)
	for row in report:
		cl_oppts[row['Opportunity ID']] = row
	# print cl_oppts['0063300000hty43'] # Testing

recon_report = {} 
with open(recon_report_name+'.csv', 'rU') as f2:
	report = f2.readlines()
	for row in range(2,len(report)):
		recon_report[report[row].split(",")[0]] = report[row].split(",")[1].strip()
	# print recon_report # Testing

# Add payment_id to each oppt's dictionary
for key in cl_oppts:
	yelp_biz_id = cl_oppts[key]['Yelp Business ID']
	if yelp_biz_id in recon_report:
		cl_oppts[key]['Payment Account ID'] = recon_report[yelp_biz_id]

cc_trans = [] # List of all payment ID's that cleared
with open(cc_trans_name+'.csv', 'rU') as f3:
	report = csv.DictReader(f3)
	for row in report:
		adv_id = row['advertiser_id']
		if row['status'] == 'Cleared':
			cc_trans.append(adv_id)
	# print cc_trans # Testing

cw_oppts = {}

for key in cl_oppts:
	if cl_oppts[key].has_key('Payment Account ID'):
		# print cl_oppts[key]['Payment Account ID']
		if cl_oppts[key]['Payment Account ID'] in cc_trans:
			cw_oppts[key] = cl_oppts[key]
print cw_oppts



### Below works
## Create a file for the batches

os.chdir("/Users/jtruong/Desktop/M1M Closed Lost Batches/Uploads") # Move uploads to uploads folder
cw_oppts_report = 'MFP_Closed Won Oppts_'+str(datetime.date.today())+'.csv'
mfp_batch1 = 'MFP_Closed Won Batch 1_'+str(datetime.date.today())+'.csv'
mfp_batch2 = 'MFP_Closed Won Batch 2_'+str(datetime.date.today())+'.csv'

with open(cw_oppts_report, 'w') as csvfile:
    fieldnames = ['Opportunity Record Type', 'Close Date', 'Yelp Business ID', 'Payment Account ID', 'Payment cycle', 'Commitment Period', 'Split Oppty: Total Comp Pts/New Revenue', 'Comp Points Currency', 'Is Split', 'Business Name', 'Reason Closed Lost - Local', 'Yelp Admin Page', 'Opportunity ID', 'Comp Points', 'Split Oppty: Total Comp Pts/New Revenue Currency', 'Ops Error Notes', 'Stage'] # header row
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for key in cw_oppts:
    	writer.writerow(cw_oppts[key])

with open(mfp_batch1, 'w') as csvfile:
    fieldnames = ['Opportunity ID','Stage'] # header row
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames,extrasaction='ignore')
    writer.writeheader()
    for key in cw_oppts:
    	cw_oppts[key]['Stage'] = 'Closed Won'
    	writer.writerow(cw_oppts[key])


with open(mfp_batch2, 'w') as csvfile:
	w = csv.writer(csvfile)
	w.writerow(['Opportunity ID','COMP_POINTS__C'])
	fieldnames = ['Opportunity ID','Comp Points']
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames,extrasaction='ignore')
	for key in cw_oppts:
		if cw_oppts[key]['Is Split'] == '1':
			writer.writerow(cw_oppts[key])


    




