import requests as rq
import pandas as pd
import phonenumbers
from retry_requests import retry
import requests_cache

# Ustawienie właściwego adresu URL.
URL = 'https://jsonplaceholder.typicode.com/users/'

# Inicjalizacja sesji HTTP z wykorzystaniem lokalnej pamięci podręcznej.
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
session = retry(cache_session, retries = 5, backoff_factor = 0.5)

# Wysyłanie żądania do REST API.

response = None
data = []

try:
    response = session.get(URL, timeout = 10)
    response.raise_for_status()

# Obsługa błędów/wyjątków związanych z żądaniem.
except rq.exceptions.HTTPError as errh:
    print(f"An HTTP error occured: {errh}")
except rq.exceptions.ConnectionError:
    print("A connection error occured. Check your internet connection or API URL format.")
except rq.exceptions.ReadTimeout:
    print("Your request timed out.")
except rq.exceptions.RequestException as err:
    print(f"An unknown error occured during your request: {err}.")

# Parsowanie danych odpowiedzi w formacie JSON.
if response:
    try:
        data = response.json()

    # Obsługa błędów związanych z niepoprawnym formatem danych JSON w odpowiedzi.
    except ValueError:
        print("An error occured. Response was not in proper JSON format.")


# Przekształcenie danych.
for user in data:
    try:
        # Spłaszczenie słownika adresu do jednego łańcucha tekstowego.
        address_info = user['address']
        address = f"{address_info['street']}, {address_info['suite']}, {address_info['city']}, {address_info['zipcode']}"
        user['address'] = address

        # Formatowanie numeru telefonu w celu ujednolicenia formatu.
        try:
            parsed_phone = phonenumbers.parse(user['phone'], "US")
            format_phone = phonenumbers.format_number(parsed_phone, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
            user['phone'] = format_phone

        # Obsługa błędów związanych z nieprawidłowym formatem numeru telefonu.
        except phonenumbers.phonenumberutil.NumberParseException as err:
            print(f"Invalid phone number format for user {user.get('id', 'unknown')}.")
            user['phone'] = "Unknown"

        # Ustawienie klucza „company” tak, aby zawierał wyłącznie nazwę firmy.
        user['company'] = user['company']['name']

    # Handling error of missing key.
    except KeyError as err:
        print(f"Key {err} not found for user {user.get('id', 'unknown')}.")


# Tworzenie ramki danych (dataframe) i zapis do pliku CSV.
if data:
    df = pd.DataFrame.from_records(data)

    if df.empty:
        print("Dataframe is empty.")
    else:
        print(df.head())

    # Zapis ramki danych do pliku CSV.
    try:
        df.to_csv('O. Czechowicz - zadanie dodatkowe.csv', index = False)
        print("CSV file created successfully.")

    # Obsługa błędów/wyjątków związanych z zapisem pliku CSV.
    except PermissionError:
        print("You don't have permission to write the file.")

    except UnicodeEncodeError:
        print("Encoding error. Save with utf-8 or utf-8-sig encoding.")

    except FileNotFoundError:
        print("Targeted folder not found.")

    except Exception as err:
        print(f"An unexpected error occured while saving data to CSV: {err}")

else:
    print("No data found to write to CSV.")
