import os
import pdfplumber
import pandas as pd

def pdf_to_dataframe(pdf_path):
    """
    Reads a PDF file and converts its tabular content into a pandas DataFrame.

    Parameters:
        pdf_path (str): Path to the PDF file.

    Returns:
        pd.DataFrame: A DataFrame containing the extracted table data, or None if no tables are found.
    """
    try:
        with pdfplumber.open(pdf_path) as pdf:
            tables = []
            for page_number, page in enumerate(pdf.pages, start=1):
                page_tables = page.extract_tables()
                for table_index, table in enumerate(page_tables, start=1):
                    print(f"Extracting table {table_index} from page {page_number}...")
                    tables.append(pd.DataFrame(table))

            if tables:
                combined_df = pd.concat(tables, ignore_index=True)
                return combined_df
            else:
                print("No tables found in the PDF.")
                return None
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return None

def save_to_csv(dataframe, output_path):
    """
    Saves the DataFrame to a CSV file.

    Parameters:
        dataframe (pd.DataFrame): The DataFrame to save.
        output_path (str): Path to save the CSV file.
    """
    try:
        dataframe.to_csv(output_path, index=False)
        print(f"DataFrame saved to {output_path}")
    except Exception as e:
        print(f"Error saving DataFrame to CSV: {e}")

def main():
    """
    Main function to execute the script.
    """
    # Specify input and output paths
   
    input_pdf = "sample_data/sample_table.pdf"  # Change to the path of your PDF file
    output_csv = "output/extracted_data.csv"  # Change to your desired output file path
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)

    print(f"Processing PDF file: {input_pdf}")
    dataframe = pdf_to_dataframe(input_pdf)

    if dataframe is not None:
        print(f"Extracted data:\n{dataframe.head()}")
        save_to_csv(dataframe, output_csv)
    else:
        print("No data extracted from the PDF.")

if __name__ == "__main__":
    main()
