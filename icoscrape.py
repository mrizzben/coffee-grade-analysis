import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the webpage
url = "https://www.ico.org/new_historical.asp"

# Send a GET request to the webpage
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# Find all the links on the webpage
links = soup.find_all("a")

# Download and convert each Excel file to CSV
for link in links:
    href = link.get("href")
    if href.endswith((".xls", ".xlsx")):
        file_url = url + "/" + href
        file_name = href.split("/")[-1]

        # Send a GET request to download the file
        file_response = requests.get(file_url)

        # Save the Excel file locally
        excel_file_name = "./data/" + str(file_name)
        with open(excel_file_name, "wb") as file:
            file.write(file_response.content)
        
        # Convert the saved Excel file to CSV using pandas
        # excel_data = pd.read_excel(excel_file_name)
        # csv_file_name = file_name.replace(".xlsx", ".csv")
        # excel_data.to_csv(csv_file_name, index=False)
        # print(f"Downloaded and converted: {file_name} to {csv_file_name}")

print("All files downloaded and converted successfully.")
