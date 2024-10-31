import os
import fitz  # PyMuPDF
import csv
import logging
from datetime import datetime
from typing import Dict, Tuple, Optional, List

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class PDFProcessor:
    """Class to handle PDF extraction and file details retrieval."""

    def __init__(self, folder_path: str = "pdf"):
        """
        Initialize with the path to the folder containing PDFs.

        Args:
            folder_path (str): Path to the folder containing PDFs.
        """
        self.folder_path = folder_path

    def get_all_pdfs(self) -> List[str]:
        """Recursively find all PDFs in the folder and subfolders."""
        return [
            os.path.join(root, file)
            for root, _, files in os.walk(self.folder_path)
            for file in files
            if file.lower().endswith(".pdf")
        ]

    def read_pdf_content(self, pdf_path: str) -> Optional[str]:
        """Extract text content from a PDF file."""
        try:
            with fitz.open(pdf_path) as pdf:
                return "".join(
                    pdf.load_page(i).get_text() for i in range(pdf.page_count)
                )
        except (fitz.FileDataError, fitz.DocumentError) as e:
            logging.error(f"Failed to read {pdf_path}: {e}")
            return None

    def get_file_details(
        self, file_path: str
    ) -> Tuple[Optional[int], Optional[str], Optional[str]]:
        """Get file size, creation time, and modification time."""
        try:
            size = os.path.getsize(file_path)
            created = datetime.fromtimestamp(os.path.getctime(file_path)).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            modified = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            return size, created, modified
        except OSError as e:
            logging.error(f"Error fetching details for {file_path}: {e}")
            return None, None, None

    def process_pdfs(self) -> Dict[str, Tuple[int, str, str, str]]:
        """Process all PDFs and return their details and content."""
        pdf_data = {}
        for pdf_path in self.get_all_pdfs():
            content = self.read_pdf_content(pdf_path)
            size, created, modified = self.get_file_details(pdf_path)

            if content:
                logging.info(f"Processed: {pdf_path}")
                pdf_data[pdf_path] = (size, created, modified, content)
            else:
                logging.warning(f"Skipping {pdf_path} due to read error.")

        return pdf_data

    @staticmethod
    def save_to_csv(
        data: Dict[str, Tuple[int, str, str, str]], csv_filename: str = "pdf_data.csv"
    ) -> None:
        """Save the PDF data to a CSV file."""
        try:
            with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(
                    ["PDF Path", "Size (Bytes)", "Created", "Modified", "Content"]
                )
                for path, details in data.items():
                    writer.writerow([path, *details])
            logging.info(f"Data saved to {csv_filename}")
        except OSError as e:
            logging.error(f"Failed to save data to CSV: {e}")


def main():
    """Main function to run the PDF processing."""
    processor = PDFProcessor(folder_path="pdf")
    pdf_data = processor.process_pdfs()

    if pdf_data:
        logging.info(f"Total PDFs processed: {len(pdf_data)}")
        PDFProcessor.save_to_csv(pdf_data)
    else:
        logging.warning("No valid PDFs were found or processed.")


if __name__ == "__main__":
    main()
