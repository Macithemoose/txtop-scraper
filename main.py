import requests
from datetime import datetime, timedelta
from urllib.parse import quote
import helpers
import sys

class Search:
    def __init__(self, user_input = None, years = None):
        self.user_input = user_input
        self.years = years

    def __repr__(self):
        return (f"Search(user_input={self.user_input}, years={self.years})")
    

def main(): # search_to_plane(user_input, years):
    last_update_time = helpers.load_last_update_time()

    headers_flag = True

    # Update headers again if it's been too long
    if ((last_update_time is None) or (datetime.now() - last_update_time > timedelta(hours=3)) or (headers_flag == True)): 
        try:
            print("Updating headers...")
            helpers.update_headers()
            new_time = datetime.now()
            helpers.save_last_update_time(new_time)
        except Exception as e:
            print(f"Error loading headers: {e}")
            sys.exit(1)


    headers = helpers.convert_headers_to_dict('headers_input.txt')
    listings = []

    user_input_manufacturer = input("What is the manufacturer of the aircraft you'd like to search for?: ")
    encoded_string_manufacturer = quote(user_input_manufacturer.strip())

    user_input_model = input("What is the model of the aircraft you'd like to search for?: ")
    encoded_string_model = quote(user_input_model.strip())

    user_input_first = user_input_manufacturer + "_" + user_input_model
    add_more_planes = ""

    while add_more_planes != "No":
        years = []
        listings = []
        year_input = input("Would you like to specify a year? If yes, type the first year you'd like to specify. If not, type 'No'. ")
        while year_input != "No":
            years.append(year_input)
            year_input = input("What's the next year you'd like to add? Type 'No' if finished. ")

        page_num = 1
        print(f"Querying the following URL: https://www.controller.com/ajax/listings/ajaxsearch?Manufacturer={encoded_string_manufacturer}&ModelGroup={encoded_string_model}")
        # print(f"Querying the following URL: https://www.controller.com/ajax/listings/ajaxsearch?Model={encoded_string_model}&Manufacturer={encoded_string_manufacturer}")
        # print(f"Querying the following URL: ", f"https://www.controller.com/ajax/listings/ajaxsearch?keywords={encoded_string}")

        while True:
            url = f"https://www.controller.com/ajax/listings/ajaxsearch?Manufacturer={encoded_string_manufacturer}&ModelGroup={encoded_string_model}&page={page_num}" 
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                try:
                    print(f"On page {page_num}...")
                    data = response.json()
                    listings.extend(data["Listings"])
                    if len(data["Listings"]) == 0:
                        break 
                    page_num += 1
                except ValueError:
                    print("Response is not valid JSON")
                    break
            else:
                print(f"Request failed with status code {response.status_code}")
                break
        planes = helpers.extract_planes_from_listings(listings)

        if len(years) > 0:
            planes = helpers.filter_year(planes, years)

        helpers.extract_avionics(planes)

        # Asking if you want to add any other planes:
        add_more_planes = input("Would you like to add another aircraft to this file? Type 'Yes' if yes, type 'No' if you're finished. ")
        if add_more_planes != "No":
            # Redo headers 
            helpers.update_headers()
            new_time = datetime.now()
            helpers.save_last_update_time(new_time)
            headers = helpers.convert_headers_to_dict('headers_input.txt')
            user_input_manufacturer = input("What is the manufacturer of the aircraft you'd like to search for?: ")
            encoded_string_manufacturer = quote(user_input_manufacturer.strip())

            user_input_model = input("What is the model of the aircraft you'd like to search for?: ")
            encoded_string_model = quote(user_input_model.strip())
    
    timestamp = datetime.now().strftime("%m-%d-%Y")
    safe_filename = user_input_first.replace("/", "-") # Some planes have a '/' character, which we wanna remove in the file name
    helpers.export_planes_to_xlsx(planes, f"data/{safe_filename}_{timestamp}.xlsx")

if __name__ == "__main__":
    main()