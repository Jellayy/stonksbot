import datetime as dt
import requests, zipfile, csv, os  # , pdfplumber


def get_disclosures(date):
    # Download financial disclosures ZIP
    response = requests.get(f'https://disclosures-clerk.house.gov/public_disc/financial-pdfs/{date.strftime("%Y")}FD.ZIP')
    with open('disclosures.zip', 'wb') as file:
        file.write(response.content)

    # Extract txt file
    with zipfile.ZipFile('disclosures.zip') as file:
        file.extract(f'{date.strftime("%Y")}FD.txt', '.')

    # Parse txt file for disclosure ids
    disclosures = []
    with open(f'{date.strftime("%Y")}FD.txt') as file:
        for line in csv.reader(file, delimiter='\t'):
            if line[7] == '{dt.month}/{dt.day}/{dt.year}'.format(dt = date):
                if line[4] == 'P':
                    disclosures.append({'name': f'{line[2]} {line[1]}',
                                        'state': line[5],
                                        'filing_date': line[7],
                                        'doc_link': f'https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/{date.strftime("%Y")}/{line[8]}.pdf'})

    # Clean up files
    os.remove(f'{date.strftime("%Y")}FD.txt')
    os.remove('disclosures.zip')

    # Return
    return disclosures


# # This was a WIP method for parsing the data in PDFs, but PDFs were too unpredictable, unfinished and doesn't always work
# def get_pdf_data(date, pdf_id):
#     # Download disclosure PDF
#     response = requests.get(f'https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/{date.strftime("%Y")}/{pdf_id}.pdf')
#     with open(f'{pdf_id}.pdf', 'wb') as file:
#         file.write(response.content)
#
#     # Read raw PDF data
#     raw = ""
#     with pdfplumber.open(f'{pdf_id}.pdf') as pdf:
#         for page in pdf.pages:
#             raw += page.extract_text()
#
#     # Clean up files
#     os.remove(f'{pdf_id}.pdf')
#
#     # Very roughly parse PDF data (this is a lil yikes)
#     footer_split = raw.split('*')[0]
#     header_split = footer_split.split('tranSactionS\n')[1].replace('iD owner asset transaction Date notification amount cap.\ntype Date gains >\n$200?', '')
#
#     print(header_split)


if __name__ == '__main__':
    print(get_disclosures(dt.datetime(2022, 2, 2)))
