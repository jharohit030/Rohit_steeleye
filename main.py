import requests
from zipfile import ZipFile
import csv
import xml.etree.ElementTree as ET
import logging
import os
import unittest
import pandas as pd


def download_zip(url, zip_filename):
    """
    Downloading the zip file from given link and extracting the contents.

    Args:
        url (str): The URL of the zip file to download.
        zip_filename (str): The filename to save the downloaded zip file.

    Returns:
        None
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raising  an exception for  non-2xx status codes
        logging.info("Downloading successful!")
    except requests.exceptions.RequestException as e:
        logging.error("Error occurred during download: " + str(e))
        return

    try:
        with open(zip_filename, 'wb') as zip_file:
            zip_file.write(response.content)
        with ZipFile(zip_filename, 'r') as zip:
            zip.printdir()
            logging.info("Extracting all the files now...")
            zip.extractall()
            logging.info("Extraction completed!")
    except (IOError, ZipFile.BadZipfile) as e:
        logging.error("Error occurred during extraction: " + str(e))


def xml_to_csv(xml_filename, csv_filename):
    """
    Parses an XML file and writes its data to a CSV file.

    Args:
        xml_filename (str): The filename of the XML file to parse.
        csv_filename (str): The filename to save the parsed data in CSV format.

    Returns:
        None
    """
    try:
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['FinInstrmGnlAttrbts.Id', 'FinInstrmGnlAttrbts.FullNm', 'FinInstrmGnlAttrbts.ClssfctnTp',
                             'FinInstrmGnlAttrbts.CmmdtyDerivInd', 'FinInstrmGnlAttrbts.NtnlCcy', 'Issr'])
            tree = ET.parse(xml_filename)
            root = tree.getroot()
            namespaces = {'a': 'urn:iso:std:iso:20022:tech:xsd:auth.036.001.02'}
            elements = root.findall('.//a:FinInstrmGnlAttrbts', namespaces)
            count = 0
            for element in elements:
                id = element.find('a:Id', namespaces)
                full_nm = element.find('a:FullNm', namespaces)
                Clssfctn_tp = element.find('a:ClssfctnTp', namespaces)
                cmmdty_deriv_ind = element.find('a:CmmdtyDerivInd', namespaces)
                ntnl_ccy = element.find('a:NtnlCcy', namespaces)
                if id is not None and id.text:
                    id_element = id.text.strip()
                if full_nm is not None and full_nm.text:
                    full_nm_element = full_nm.text.strip()
                if Clssfctn_tp is not None and Clssfctn_tp.text:
                    Clssfctn_tp_element = Clssfctn_tp.text.strip()
                if cmmdty_deriv_ind is not None and cmmdty_deriv_ind.text:
                    cmmdty_deriv_ind_element = cmmdty_deriv_ind.text.strip()
                if ntnl_ccy is not None and ntnl_ccy.text:
                    ntnl_ccy_element = ntnl_ccy.text.strip()

            # Find Issr tag outside of FinInstrmGnlAttrbts elements and write its value to csv file
            for issr_elem in root.findall('.//a:Issr', namespaces):
                if issr_elem is not None and issr_elem.text:
                    issr = issr_elem.text.strip()
                writer.writerow([id_element, full_nm_element, Clssfctn_tp_element,
                                 cmmdty_deriv_ind_element, ntnl_ccy_element, issr])
                count += 1
            logging.info("Wrote " + str(count) + " rows to " + csv_filename)
    except (IOError, ET.ParseError) as e:
        logging.error("Error occurred during XML parsing: " + str(e))


class Test(unittest.TestCase):
    """
    Unit tests for XML parsing and CSV writing.
    """

    def test_download(self):
        # Check if the file exists
        self.assertTrue(os.path.exists('DLTINS_20210117_01of01.zip'))
        logging.info("File is download successfully..")

    def test_extraction(self):
        # Check if the extracted files exist
        self.assertTrue(os.path.exists('DLTINS_20210117_01of01.xml'))
        logging.info("File extraction is done successfully..")

    def test_csv_creation(self):
        # Check if the CSV file has been created
        self.assertTrue(os.path.exists('output.csv'))
        logging.info("Output file is created successfully..")

    def test_null_values(self):
        # Test for null values in each column of the CSV output
        df = pd.read_csv('output.csv')
        self.assertFalse(df.isnull().values.any())
        logging.info("Checking for the null value in output file")

    def test_csv_formatting(self):
        # Test that the extracted data is written to a CSV file in the correct format
        expected_header = ['FinInstrmGnlAttrbts.Id', 'FinInstrmGnlAttrbts.FullNm', 'FinInstrmGnlAttrbts.ClssfctnTp',
                           'FinInstrmGnlAttrbts.CmmdtyDerivInd', 'FinInstrmGnlAttrbts.NtnlCcy', 'Issr']
        with open('output.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)
            self.assertEqual(header, expected_header)
        logging.info("Data stored in the respective columns..")


if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(filename='steeleye.log', level=logging.INFO)

    # Download and extract the zip file
    url = 'http://firds.esma.europa.eu/firds/DLTINS_20210117_01of01.zip'
    zip_filename = 'DLTINS_20210117_01of01.zip'
    download_zip(url, zip_filename)

    # Parse XML to CSV
    xml_filename = 'DLTINS_20210117_01of01.xml'
    csv_filename = 'output.csv'
    xml_to_csv(xml_filename, csv_filename)

    # Run the unit tests
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
