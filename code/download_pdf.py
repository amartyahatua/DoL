import os
import pandas as pd
import urllib.request
from schema import DoLExtraction
from tqdm import tqdm


def download_pdf_files(df_ack, pdf_dest):
    """
    Downloads pdf files to a temporary local directory

    :param ack: String ACK_ID of the plan
    :param pdf_dest: String path to the create a temporary folder to save the pdf
    :return: None
    """
    # columns of interest from EFAST CSV export
    try:
        if not os.path.exists(pdf_dest):
            os.makedirs(pdf_dest)
    except BaseException:
        print('Error in directory creation')
    for ack in tqdm(df_ack):
        try:
            year = ack[0:4]
            month = ack[4:6]
            day = ack[6:8]
            s3_url = f'https://efast2-filings-public.s3.amazonaws.com/prd/{str(year)}/{str(month)}/{str(day)}/{str(ack)}.pdf'
            fname = os.path.basename(s3_url)
            pdf_file = urllib.request.urlopen(s3_url)
            pdf_path = os.path.join(pdf_dest, fname)

            # Save the file
            with open(pdf_path, 'wb') as fpdf:
                fpdf.write(pdf_file.read())
        except:
            continue


# Read csv file which has ACK IDs, and ground truth values
df = pd.read_csv('../data/data_balanced_unique_ack.csv')
df_ack = df[DoLExtraction.ACK_ID.value]
download_pdf_files(df_ack, DoLExtraction.PDF_PATH.value)
