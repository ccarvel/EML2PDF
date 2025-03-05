# EML2PDF
A Python script to convert email files (.eml) into PDFs; you can process a single .eml file or a directory in bulk.  

For each email, the script extracts key information (date, subject, sender, etc.), builds a simple HTML representation, and then uses a PDF conversion tool to generate a PDF. The resulting PDF file is named using the email’s date in YYYY-MM-DD format followed by a sanitized version of the email subject (e.g., 2025-03-05_My_Email_Subject.pdf).   

## Features   
•	Batch Processing: Converts all .eml files in a specified directory.   
•	Custom Naming: Generates PDF filenames based on the email’s date and subject.   
•	HTML Conversion: Uses a simple HTML template to format the email content.   
•	Command Line Interface: Specify input and output directories via command-line arguments.   

## Dependencies   
This script relies on the following Python libraries and external tools:   

**Python Libraries:**   
**pdfkit**: Python wrapper for wkhtmltopdf.   

**External Tool:**   
**wkhtmltopdf**: A command-line tool to render HTML into PDF.

**Installation**   
1.	Install Python Dependencies   

```
pip install pdfkit   
```
   
2.	Install wkhtmltopdf
Download wkhtmltopdf from [wkhtmltopdf](https://wkhtmltopdf.org/downloads.html)

**Usage**   
Run the script from the command line and provide the input directory containing your .eml files and an optional output directory for the generated PDFs. 
If no output directory is provided, PDFs are saved to the current directory.

**Command Line Example**

```
python eml2pdf_converter.py /path/to/eml/files /path/to/output/pdfs
```
   
```
/path/to/eml/files: Replace with the directory containing your .eml files.

/path/to/output/pdfs: Replace with the directory where you want the PDF files saved (optional).   
```

*If you want to see a help message with usage details, run:*   

```
python eml2pdf_converter.py -h
```   

**How It Works**   
  1.	Email Parsing:   
The script uses Python’s email module to parse each .eml file and extract relevant header fields (subject, sender, recipient, date) along with the email body (preferably HTML; falls back to plain text).   

  2.	HTML Generation:   
A simple HTML document is created that embeds the extracted information. This HTML serves as the template for the PDF.   
	
  3.	PDF Conversion:   
The HTML content is converted to a PDF file using pdfkit, which requires wkhtmltopdf.   
	
  4.	File Naming:   
The email date is parsed and formatted as YYYY-MM-DD, and the email subject is sanitized (to remove unsafe filename characters). These are combined to form the PDF filename.   


---   
**License**

*This project is provided as-is under the MIT License. Feel free to modify and use it according to your needs.*
