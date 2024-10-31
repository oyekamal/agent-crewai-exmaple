import os
import fitz  # PyMuPDF
import csv
from datetime import datetime


def get_all_pdfs(folder_path):
    """Recursively find all PDFs in a folder and its subfolders."""
    pdf_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(".pdf"):
                pdf_files.append(os.path.join(root, file))
    return pdf_files


def read_pdf_content(pdf_path):
    """Extract text content from a PDF file."""
    try:
        with fitz.open(pdf_path) as pdf:
            text = "".join(pdf.load_page(i).get_text() for i in range(pdf.page_count))
            return text
    except Exception as e:
        print(f"Failed to read {pdf_path}: {e}")
        return None


def get_file_details(file_path):
    """Get details of the file such as size, creation time, and modification time."""
    try:
        size = os.path.getsize(file_path)  # File size in bytes
        created = datetime.fromtimestamp(os.path.getctime(file_path)).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        modified = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        return size, created, modified
    except Exception as e:
        print(f"Error fetching details for {file_path}: {e}")
        return None, None, None


def save_to_csv(data, csv_filename="pdf_data.csv"):
    """Save PDF data along with file details to a CSV."""
    with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        # Write header row
        writer.writerow(["PDF Path", "Size (Bytes)", "Created", "Modified", "Content"])

        for path, details in data.items():
            size, created, modified, content = details
            writer.writerow([path, size, created, modified, content])

    print(f"Data saved to {csv_filename}")


def main():
    folder_path = "pdf"
    all_pdfs = get_all_pdfs(folder_path)

    pdf_data = {}
    for pdf_path in all_pdfs:
        content = read_pdf_content(pdf_path)
        size, created, modified = get_file_details(pdf_path)

        if content:
            print(pdf_path)
            pdf_data[pdf_path] = (size, created, modified, content)
        else:
            print(f"Skipping {pdf_path} due to read error.")

    print(f"Total PDFs found: {len(pdf_data)}")
    save_to_csv(pdf_data)


if __name__ == "__main__":
    main()
