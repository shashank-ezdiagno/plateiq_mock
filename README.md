# PLATEIQ DIGITIZATION MOCK PROJECT
## INTRODUCTION
This projects tries to mock the functioning of what plateiq does.
### APIs Implemented

- To allow a customer to provide a PDF document to process(endpoint="/invoice")
- To allow a customer to track a document’s digitization status(endpoint="/invoice/progress")
- To allow a customer to retrieve the structured invoice information for a specified(endpoint="/invoice/show/{id}")
- To allow a staff member (or another microservice) to manually add digitized / parsed(endpoint="invoice/api/v1/invoice/{id}/" method=POST)
  - The same endpoint can also be used to update the status of a document as “digitized”
- To allow a staff member (or another microservice) to see the digital invoice(endpoint="invoice/api/v1/invoice/{id}/" method=GET)

### Tech Stack
- Web Framework - Django
- Database - SQLite(the database is also saved with project for sample data)
- Front-End - Django Templates with basic HTML
- S3 - to store files

### Data Models
- File - to save file attributes(name, s3 ID, etc)
- Vendor - vendor data(can be created dynamically while digitizing invoice)
- Buyer - buyer data(can be created dynamically while digitizing invoice)
- VendorItem - item sold by a vendor- PK reference to Vendor(can be created dynamically while digitizing invoice)
- Invoice - actual invoice data
- InvoiceItem - items purchased within an invoice(PK reference to VendorItem)

### Data Flow
- access /invoice/ to upload file
- access /invoice/progress to see progress



