from bs4 import BeautifulSoup
import requests
import pdfplumber



home_url = "https://www.crcna.com.au"

base_url = "https://www.crcna.com.au/resources/publications"



def extract_information_pdf(pdf_path):
    page_text =''
    pdf_text = ''
    with pdfplumber.open(pdf_path) as pdf:
        num_pages = len(pdf.pages)

        for page_num in range(num_pages):
            page = pdf.pages[page_num]
            try:
                page_text = page.extract_text()
                if '\uf0b7' in page.extract_text():
                    raise UnicodeEncodeError
            except UnicodeEncodeError:
                continue
            pdf_text = pdf_text + page_text
    return pdf_text
        

def main():
    page = 0
    file_name = 0
    while page != 12:
        url = f"{base_url}?page={page}"
        response = requests.get(url)
        html_content = response.content
        soup = BeautifulSoup(html_content, 'html.parser')
        section = soup.find("table", class_="cols-4")
        links = section.find_all("a")
        
        for link in links:
            url = f"{home_url}{link['href']}"  # Get the correct URL from the link
            print(url)
            response = requests.get(url)
            document_page = response.content
            soup = BeautifulSoup(document_page, 'html.parser')
            document_div = soup.find("div", class_="field field--name-field-media-file field--type-file field--label-hidden field__item")
            
            try:
                document_link = document_div.find("a")
                if document_link is None:
                    raise AttributeError("Document div not found")
            except AttributeError as e:
                print("There's no research paper in pdf: ", e)
                continue
            document_link = home_url + document_link['href']
            print(document_link)
            response = requests.get(document_link)
            if response.status_code == 200:
                extracted_text = ''
                print("Downloadable")
                with open(f"{file_name}.pdf", 'wb') as pdf:
                    pdf.write(response.content)
                    pdf_path = 'C:/Users/Thuan/Documents/GovHack/'+ str(file_name) + '.pdf'
                    extracted_text = extract_information_pdf(pdf_path)
                with open("data.txt", "a") as file:
                    file.write(extracted_text)
    
            file_name += 1
        page += 1



if __name__ == "__main__":
    main()