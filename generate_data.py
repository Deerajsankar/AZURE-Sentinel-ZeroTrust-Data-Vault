import csv
import random
import uuid
from datetime import datetime, timedelta

# The target volume for our Big Data test
rows = 100000 

merchants = ['Starbucks', 'Apple Store', 'Uber', 'Amazon', 'Target', 'KPMG']
statuses = ['Cleared', 'Pending', 'Failed']

print(f"Generating {rows} fake transactions...")

# Using newline='' to prevent blank rows in Windows
with open('massive_transactions.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    # Write the header
    writer.writerow(['TransactionID', 'AccountNumber', 'Amount', 'Merchant', 'Timestamp', 'Status'])
    
    # Generate the synthetic data
    for i in range(rows):
        t_id = f"TXN-{uuid.uuid4().hex[:8].upper()}"
        account = f"****{random.randint(1000, 9999)}"
        amount = round(random.uniform(5.00, 1500.00), 2)
        merchant = random.choice(merchants)
        timestamp = (datetime.utcnow() - timedelta(days=random.randint(0, 30))).isoformat() + "Z"
        status = random.choice(statuses)
        
        writer.writerow([t_id, account, amount, merchant, timestamp, status])
        
        # Print a progress update every 20,000 rows
        if i % 20000 == 0 and i > 0:
            print(f"{i} rows generated...")

print("Success! massive_transactions.csv is ready for the vault.")