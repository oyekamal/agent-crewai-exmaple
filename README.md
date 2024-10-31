# agent-crewai-exmaple

# PDF Processing and Summarization Tools

This repository contains two scripts: `pdf_to_db.py` for processing PDF files into a CSV database and `pdf_to_summary_blog.py` for generating summaries and blog posts from PDF content.

## 1. PDF to DB

This script scans a specified folder for PDF files, extracts text and metadata (size, creation date, modification date), and saves the information into a CSV file.

### Usage
1. Ensure you have `PyMuPDF` installed (`pip install pymupdf`).
2. Run the script with `python pdf_to_db.py`.
3. A `pdf_data.csv` file will be created with extracted PDF data.

## 2. PDF to Summary and Blog

This script uses CrewAI tools to analyze PDF content, summarize it, and generate a blog post.

### Usage
1. Ensure `crewAI` and `crewAI_tools` are installed and set your OpenAI API key in the environment variable.
2. Run `pdf_to_summary_blog.py` to analyze a PDF, summarize it, and create a JSON-formatted blog post in `blog-posts/sample.json`.
