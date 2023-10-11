import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = "https://www.drsaina.com/hospital?pageIndex="
num_pages = 99 


all_hospital_data = []


for page_number in range(1, num_pages + 1):
 
    page_url = base_url + str(page_number)

   
    response = requests.get(page_url)

  
    if response.status_code != 200:
        print(f"Failed  {page_number}")
        continue

    
    soup = BeautifulSoup(response.content, "html.parser")

    
    hospital_elements = soup.find_all("div", class_="hospitalDetails")

   
    for hospital in hospital_elements:
        hospital_name = hospital.find("h2").text
        
        hospital_city=hospital.find("label").text

     
        hospital_link = hospital.find("a")["href"]
        
        
        hospital_url = "https://www.drsaina.com" + hospital_link

       
        response_hospital = requests.get(hospital_url)

        if response_hospital.status_code == 200:
            soup_hospital = BeautifulSoup(response_hospital.content, "html.parser")
            hospital_phone = soup_hospital.find("div", class_="newmedicine-name").text
            hospital_image=soup_hospital.find("div",class_="newmedicine-icon col-lg-3").text
            hospital_descripe=soup_hospital.find("div",class_="newsecoundContent").text
        else:
            hospital_phone = "Phone number not found"
            hospital_imag="image url not found"
            hospital_descripe="descripe not found"

        all_hospital_data.append({"Name": hospital_name , "Phone and address": hospital_phone,"City":hospital_city,"image url":hospital_image,"Descripe":hospital_descripe})


df = pd.DataFrame(all_hospital_data)


excel_writer = pd.ExcelWriter("D:\project\Darmankade\hospital_data18.xlsx", engine="openpyxl")
df.to_excel(excel_writer, sheet_name="Hospitals", index=False)
excel_writer._save()

print(f"اطلاعات از {num_pages}صفحه جمع اوری شد")
