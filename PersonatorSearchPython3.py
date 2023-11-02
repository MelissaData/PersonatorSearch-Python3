
import json
import requests
import argparse
import urllib.parse

def main():
  base_service_url = "https://personatorsearch.melissadata.net/"
  service_endpoint = "WEB/doPersonatorSearch"; #please see https://www.melissa.com/developer/personator for more endpoints
  
  # Create an ArgumentParser object
  parser = argparse.ArgumentParser(description='Personator Search command line arguments parser')

  # Define the command line arguments
  parser.add_argument('--license', '-l', type=str, help='License key')
  parser.add_argument('--fullname', type=str, help='Full Name')
  parser.add_argument('--addressline1', type=str, help='Address Line 1')
  parser.add_argument('--city', type=str, help='City')
  parser.add_argument('--state', type=str, help='State')
  parser.add_argument('--postal', type=str, help='Postal Code')

  # Parse the command line arguments
  args = parser.parse_args()

  # Access the values of the command line arguments
  license = args.license
  fullname = args.fullname
  addressline1 = args.addressline1
  city = args.city
  state = args.state
  postal = args.postal

  call_api(base_service_url, service_endpoint, license, fullname, addressline1, city, state, postal)

def get_contents(base_service_url, request_query):
    url = urllib.parse.urljoin(base_service_url, request_query)
    response = requests.get(url)
    obj = json.loads(response.text)
    pretty_response = json.dumps(obj, indent=4)

    print("\n==================================== OUTPUT ====================================\n")

    print("API Call: ")
    for i in range(0, len(url), 70):
        if i + 70 < len(url):
            print(url[i:i+70])
        else:
            print(url[i:len(url)])
    print("\nAPI Response:")
    print(pretty_response)

def call_api(base_service_url, service_endpoint, license, fullname, addressline1, city, state, postal):
    print("\n================ WELCOME TO MELISSA PERSONATOR SEARCH CLOUD API ================\n")

    should_continue_running = True
    while should_continue_running:
        input_fullname = ""
        input_addressline1 = ""
        input_city = ""
        input_state = ""
        input_postal = ""
        if not fullname and not addressline1 and not city and not state and not postal:
            print("\nFill in each value to see results")
            input_fullname = input("Full Name: ")
            input_addressline1 = input("Addressline1: ")
            input_city = input("City: ")
            input_state = input("State: ")
            input_postal = input("Postal: ")
        else:
            input_fullname = fullname
            input_addressline1 = addressline1
            input_city = city
            input_state = state
            input_postal = postal

        while not input_fullname or not input_addressline1 or not input_city or not input_state or not input_postal:
            print("\nFill in each value to see results")
            if not input_fullname:
                input_fullname = input("\nFulll Name: ")
            if not input_addressline1:
                input_addressline1 = input("\nAddressline1: ")
            if not input_city:
                input_city = input("\nCity: ")
            if not input_state:
                input_state = input("\nState: ")
            if not input_postal:
                input_postal = input("\nPostal: ")

        inputs = {
            "format": "json",
            "full": input_fullname,
            "a1": input_addressline1,
            "city": input_city,
            "state": input_state,
            "postal": input_postal
        }

        print("\n==================================== INPUTS ====================================\n")
        print(f"\t   Base Service Url: {base_service_url}")
        print(f"\t  Service End Point: {service_endpoint}")
        print(f"\t          Full Name: {input_fullname}")
        print(f"\t       Addressline1: {input_addressline1}")
        print(f"\t               City: {input_city}")
        print(f"\t              State: {input_state}")
        print(f"\t        Postal Code: {input_postal}")

       # Create Service Call
        # Set the License String in the Request
        rest_request = f"&id={urllib.parse.quote_plus(license)}"

        # Set the Input Parameters
        for k, v in inputs.items():
            rest_request += f"&{k}={urllib.parse.quote_plus(v)}"

        # Build the final REST String Query
        rest_request = service_endpoint + f"?{rest_request}"

        # Submit to the Web Service.
        success = False
        retry_counter = 0

        while not success and retry_counter < 5:
            try: #retry just in case of network failure
                get_contents(base_service_url, rest_request)
                print()
                success = True
            except Exception as ex:
                retry_counter += 1
                print(ex)
                return

        is_valid = False;

        if (fullname is not None) and (addressline1 is not None) and (city is not None) and (state is not None) and (postal is not None):
            concat = fullname + addressline1 + city + state + postal
        else:
            concat = None

        if concat is not None and concat != "":
            is_valid = True
            should_continue_running = False

        while not is_valid:
            test_another_response = input("\nTest another record? (Y/N)")
            if test_another_response != '':
                test_another_response = test_another_response.lower()
                if test_another_response == 'y':
                    is_valid = True
                elif test_another_response == 'n':
                    is_valid = True
                    should_continue_running = False
                else:
                    print("Invalid Response, please respond 'Y' or 'N'")

    print("\n===================== THANK YOU FOR USING MELISSA CLOUD API ====================\n")

main()