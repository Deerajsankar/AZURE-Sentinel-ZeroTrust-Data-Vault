import logging
import csv
import io
import azure.functions as func

# 1. Initialize the Function App (The Engine)
app = func.FunctionApp()

# 2. The Trigger (Listen to the 'inboundlogs' vault)
@app.blob_trigger(arg_name="myblob", 
                  path="inboundlogs/{name}", 
                  connection="AzureWebJobsStorage")

# 3. The Output Binding (Send clean data to a new 'outboundclean' folder)
@app.blob_output(arg_name="cleanblob", 
                 path="outboundclean/CLEAN-{name}", 
                 connection="AzureWebJobsStorage")

def process_transactions(myblob: func.InputStream, cleanblob: func.Out[bytes]):
    logging.info(f"🚨 New file detected! Processing: {myblob.name} (Size: {myblob.length} bytes)")

    # --- EXTRACT ---
    # Read the raw CSV data into memory
    raw_data = myblob.read().decode('utf-8')
    csv_reader = csv.DictReader(io.StringIO(raw_data))
    
    # Prepare the output buffer
    output_buffer = io.StringIO()
    csv_writer = csv.DictWriter(output_buffer, fieldnames=csv_reader.fieldnames)
    csv_writer.writeheader()
    
    # --- TRANSFORM ---
    # Filter out 'Failed' and 'Pending' transactions
    clean_count = 0
    total_count = 0
    
    for row in csv_reader:
        total_count += 1
        if row.get('Status') == 'Cleared':
            csv_writer.writerow(row)
            clean_count += 1
            
    logging.info(f"✅ Data Transformation Complete: Kept {clean_count} out of {total_count} rows.")

    # --- LOAD ---
    # Write the pristine data to the output binding
    cleanblob.set(output_buffer.getvalue().encode('utf-8'))
    logging.info(f"🚀 Successfully routed clean data to the outboundclean folder!")