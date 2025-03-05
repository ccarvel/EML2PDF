import email
from email import policy
from email.parser import BytesParser
from email.utils import parsedate_to_datetime
import re
import pdfkit
import os
import argparse

def sanitize_subject(subject):
    """Remove unsafe characters from subject to create a safe file name."""
    subject = subject.strip().replace(' ', '_')
    return re.sub(r'[^a-zA-Z0-9\-_]', '', subject)

def eml_to_pdf(eml_path, output_dir="."):
    """Convert a single .eml file to a PDF using date and sanitized subject for naming."""
    with open(eml_path, 'rb') as f:
        msg = BytesParser(policy=policy.default).parse(f)
    
    # Build HTML header with email fields
    header_html = f"""
    <h2>{msg['subject'] or 'No Subject'}</h2>
    <p>
      <strong>From:</strong> {msg['from'] or 'Unknown'}<br>
      <strong>To:</strong> {msg['to'] or 'Unknown'}<br>
      <strong>Date:</strong> {msg['date'] or 'Unknown'}
    </p>
    """

    # Extract the email body
    body_html = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == 'text/html':
                body_html = part.get_content()
                break
            elif content_type == 'text/plain' and not body_html:
                body_html = f"<pre>{part.get_content()}</pre>"
    else:
        content_type = msg.get_content_type()
        if content_type == 'text/html':
            body_html = msg.get_content()
        else:
            body_html = f"<pre>{msg.get_content()}</pre>"

    # Combine header and body into a complete HTML document
    html_content = f"""
    <html>
      <head>
        <meta charset="utf-8">
        <title>{msg['subject'] or 'Email PDF'}</title>
      </head>
      <body>
        {header_html}
        <hr>
        {body_html}
      </body>
    </html>
    """

    # Parse the email date and format it as YYYY-MM-DD
    email_date_str = msg['date']
    if email_date_str:
        try:
            email_date = parsedate_to_datetime(email_date_str)
            formatted_date = email_date.strftime("%Y-%m-%d")
        except Exception:
            formatted_date = "unknown-date"
    else:
        formatted_date = "unknown-date"
    
    # Sanitize the subject for safe file naming
    subject = msg['subject'] or "no-subject"
    subject_sanitized = sanitize_subject(subject)

    # Create output file name: YYYY-MM-DD_subject.pdf
    pdf_filename = f"{formatted_date}_{subject_sanitized}.pdf"
    pdf_path = os.path.join(output_dir, pdf_filename)

    # Convert HTML content to PDF
    pdfkit.from_string(html_content, pdf_path)
    print(f"Converted '{eml_path}' to '{pdf_path}'")

def process_directory(input_dir, output_dir="."):
    """Process every .eml file in the input directory."""
    os.makedirs(output_dir, exist_ok=True)
    
    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.eml'):
            eml_path = os.path.join(input_dir, filename)
            eml_to_pdf(eml_path, output_dir)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Convert all .eml files in a directory to PDFs")
    parser.add_argument("input_directory", help="Directory containing .eml files")
    parser.add_argument("output_directory", nargs="?", default=".", help="Directory to save PDF files (default: current directory)")
    args = parser.parse_args()

    process_directory(args.input_directory, args.output_directory)
