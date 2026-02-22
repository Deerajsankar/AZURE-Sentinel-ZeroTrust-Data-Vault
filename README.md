# Project Sentinel: Zero-Trust Serverless Data Pipeline 🛡️

## 🎯 Project Objective
The goal of Project Sentinel was to architect a high-security, automated data ingestion system for a financial services scenario. The primary challenge was to process large-scale transaction logs (**100,000+ rows**) while adhering to strict **Zero-Trust** security protocols. This meant:
- Eliminating all hardcoded passwords and connection strings.
- Automating infrastructure deployment via **Terraform**.
- Ensuring data integrity by separating raw and processed data (Medallion Architecture).
- Minimizing operational costs through **Serverless, Event-Driven** compute.

## 🏗️ Architecture & Design Patterns

### 1. Medallion Architecture
- **Bronze Layer (`inboundlogs`):** Stores raw, immutable CSV transaction logs exactly as they arrive from the source.
- **Silver Layer (`outboundclean`):** Stores filtered and validated "Cleared" transactions, ready for downstream analytics or ML models.

### 2. Zero-Trust Security (AuthN & AuthZ)
- **Identity:** Utilizes **System-Assigned Managed Identity** for the compute engine. Azure dynamically issues a "badge" (Object ID) to the VM, removing the need for secrets.
- **Role-Based Access Control (RBAC):** Implemented via Terraform to grant the **Storage Blob Data Contributor** role to only the necessary identities (The Developer and the Function App).

### 3. Serverless Compute
- **Azure Functions (Python 3.11):** An event-driven engine that sits idle ($0 cost) until a file is detected, then scales instantly to process data.

## 🐍 The App Code (ETL Logic)
The heart of the pipeline is a Python-based Azure Function located in the `app_code/` directory. 

### Key Features of the Python Engine:
- **v2 Programming Model:** Uses modern Python decorators (`@app.blob_trigger` and `@app.blob_output`) to handle data bindings, keeping the code clean and focused on logic.
- **Stream Processing:** Reads the incoming blob as a stream to handle large files efficiently without crashing the server's memory.
- **Automated Transformation:**
    - **Extraction:** Parses the CSV using the `csv.DictReader` library.
    - **Filtration:** Drops any rows marked as "Failed" or "Pending," ensuring only "Cleared" transactions reach the Silver layer.
    - **Header Preservation:** Dynamically writes the clean CSV while maintaining the original schema.

## 🚀 How It Works
1. **Trigger:** A `massive_transactions.csv` file is uploaded to the `inboundlogs` container.
2. **Event:** The Azure Blob Trigger detects the `PutBlob` event and wakes up the Python Function.
3. **Execution:** The script extracts the data, applies transformation logic, and loads it into the `outboundclean` container with a `CLEAN-` prefix.
4. **Completion:** The serverless engine shuts down automatically.

## 🛠️ Tech Stack
- **IaC:** Terraform
- **Cloud:** Microsoft Azure
- **Language:** Python 3.11
- **Identity:** Microsoft Entra ID
- **Networking:** VNet & NSG

## 📦 Deployment Instructions

### 1. Deploy Infrastructure
Initialize and build the cloud environment:
```powershell
terraform init
terraform apply -auto-approve
