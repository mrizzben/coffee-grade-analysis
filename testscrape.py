import requests
import json
import time

reqUrl = "https://www.archdaily.com/search/api/v1/us/projects"
headersList = {
    "Accept": "*/*"
}

# Initialize an empty list to store the data from all pages
all_data = []

# Send requests for each page and retrieve the data
page = 1
while True:
    response = requests.get(reqUrl+f"?page={page}", headers=headersList)

    if response.status_code == 200:
        json_data = response.json()
        data = json_data['results']

        # Break the loop if there are no more pages
        if not data:
            break

        # Append the data from the current page to the list
        all_data.extend(data)
        print(f"Page {page} done.")
        page += 1
        time.sleep(5)
    else:
        print("Request failed with status code:", response.status_code)
        break

# Save the collected data as a JSON file
with open("response.json", "w") as json_file:
    json.dump(all_data, json_file)

print("Response data saved as response.json")
