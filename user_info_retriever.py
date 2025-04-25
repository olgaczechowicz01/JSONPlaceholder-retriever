
"""
DOKUMENTACJA APLIKACJI
Olga Czechowicz - Zadanie dodatkowe (Dział Danych i Analityki - Python API + CSV)

NAZWA APLIKACJI
Pozyskiwanie danych o użytkownikach z API JSONPlaceholder.

OPIS APLIKACJI
Niniejsza aplikacja służy do pobierania danych o użytkownikach
z zewnętrznego REST API – JSONPlaceholder (umieszczone są na nim fikcyjne dane testowe), a
następnie przetwarzeniu danych w celu wybrania najważniejszych informacji oraz optymalizacji ich czytelności,
kończąc na zapisie przetworzonych danych w pliku CSV.

SPOSÓB POBRANIA DANYCH
Dane użyte w aplikacji pochodzą z witryny "https://jsonplaceholder.typicode.com/users/", gdzie umieszczone
są dane o użytkownikach w API JSONPlaceholder. Dane zostały pobrane za pomocą modułów requests, retry-requests
oraz requests-cache.

W celu ominięcia możliwych błędów w pobraniu danych, zamiast wysłania jednej prośby do API (za pomocą requests.get()),
zastosowano mechanizm automatycznych prób połączenia z wykorzystaniem pamięci podręcznej cache.
Bardziej dokładnie, w wypadku nieudanej próby, kod automatycznie próbuje ponownie wysłać prośbę (do 5 razy),
po czym użytkownik jest powiadomiony o zaistniałym błędzie w wypadku nieudanej próby.

Cache został wykorzystany do stworzenia sesji cache z pamięcią podręczną (wygasającej po 3600 s.),
która zachowuje pamięć o wykonanych wysłanych prośbach do API (za pomocą funkcji CachedSession()),
tj. sesja cache posłużyła jako baza dla sesji automatycznych prób połączenia z API za pomocą funkcji retry().
Faktyczne połączenie z API oraz pobranie danych, wykonano za pomocą metody get() zaaplikowanej
do uprzednio opisanej sesji, gdzie jako argument zastosowano URL, na którym umieszczone były dane zainteresowania.

PRZETWARZANIE DANYCH
Wpierw po uzyskaniu danych za pomocą get(), zastosowano metodę json(), aby przekształcić uzyskany string,
w dane formatu dziennika JSON (aby móc dalej przekształcić dane oraz poddać je bibliotece pandas).

Każdy użytkownik został opisany przez dziennik,
zawierający następujące klucze:
- id: id użytkownika,
- name: imię użytkownika,
- username: pseudonim użytkownika,
- address: adres użytkownika, zawierający dziennik o 4 kluczach opisujących adres (street, suite, city i zipcode)
  oraz 1 opisującym szerokość geograficzną adresu,
- phone: numer telefonu użytkownika,
- website: adres strony internetowej użytkownika,
- company: informacje o firmie użytkownika, dziennik o 3 kluczach (name, catchPhrase i bs).

Ze względu na to, iż powyższa struktura jest mniej złożona, zachowano wszystkie główne klucze,
gdyż posiadają ważne informacje na temat użytkowników. Natomiast, wartości przypisane do niektórych
kluczy zostały zmodyfikowane w celu usunięcia możliwych „zbędnych" informacji, tj.
- informacji o szerokości geograficznej adresu
- informacji o firmie użytkownika poza nazwą firmy - dotyczyły sloganu oraz opisu działalności firmy.
Powyższe informacje, są nadmiernie szczegółowe (w przypadku adresu) albo nie są bezpośrednio związane
z użytkownikiem (informacje o firmie), w wyniku czego są postrzegane jako mniej istotne w porównaniu do innych pól.

Ponadto, w celu optymalizacji czytelności danych, zdecydowano się na:
- połączenie 4 oddzielnych wartości opisujących adres w jeden f-string zawierający pełen adres,
- ujednoliceniu sformatowania numerów telefonu użytkowników za pomocą modułu phonenumbers,
- ustawieniu wyłącznie nazwy firmy użytkownika jako wartość klucza „company".

Następnie zmodyfikowany obiekt JSON posłużył jako źródło dla stworzenia ramki danych,
za pomocą metody from_records(), gdzie klucze dziennika każdego użytkownika posłużyły jako nagłówki kolumny,
a każdy wiersz reprezentował pojedynczego użytkownika/rekord.

ZAPIS DANYCH DO PLIKU CSV
Utworzona ramka danych posłużyła jako źródło dla stworzenia pliku CSV za pomocą metody .to_csv()
pochodzącej z biblioteki pandas.

OBSŁUGA BŁĘDÓW
Wszystkie etapy kodu zostały ujęte w ramach blokach try, gdzie zostały opisane możliwe wyjątki,
w celu obsługi potencjalnych błędów.

Na poziomie dostępu do API:
- Zastosowano obsługę błędów/wyjątków pochodzących z biblioteki requests, aby zlokalizować możliwe różne rodzaje niepowodzeń podczas próby połączenia z API.
- Uwzględniono kilka scenariuszy, aby zwrócić spersonalizowaną wiadomość dla użytkownika skryptu, w celu większego poinformowania na temat możliwych błędów.
- Wyróżnione przypadki to:
  - HTTPError – informuje o zwróceniu kodu odpowiedzi HTTP oznaczającego błąd (np. 404, 500).
  - ConnectionError – informuje o problemach z nawiązaniem połączenia, np. błędnym URL lub braku internetu.
  - ReadTimeout – wiadomość o przekroczeniu limitu czasowego oczekiwania na odpowiedź z API.
  - RequestException – ogólny wyjątek na inne rodzaje błędów zapytań nieopisanych powyżej.

W ramach niepoprawnego formatu danych:
- Konwersja obiektu response do formatu JSON:
  - Po otrzymaniu odpowiedzi z API, przed przetworzeniem danych zastosowano metodę .json(),
    której błędne działanie (np. brak poprawnego formatu JSON) przechwytywane jest jako wyjątek ValueError.
    Użytkownik zostaje poinformowany, że odpowiedź nie miała poprawnego formatu JSON,
    a dalsze przetwarzanie zostaje zatrzymane.
- Przekształcanie dziennika JSON:
  - W przypadku niewystępnia przekształcanego klucza, czy wartości, może wystąpić wyjątek KeyError.
  - W przypadku błędów w związku z formatowaniem numerów telefonu, występuje wyjątek NumberParseException z modułu phonenumbers.

W ramach zapisu pliku CSV:
- Przy wykorzystaniu metody .to_csv(), zostały obsłużone poniższe wyjątki:
  - PermissionError – informuje użytkownika o braku uprawnień do zapisania pliku.
  - UnicodeEncodeError – informuje o problemie zapisania pliku w związku z kodowaniem znaków. Informacja o potrzebie zastosownia kodowania utf-8 lub utf-8-sig.
  - FileNotFoundError – błąd, gdy ścieżka do zapisu pliku nie istnieje.
  - Exception – ogólny wyjątek na inne rodzaje błędów zapytań nieopisanych powyżej.

WYMAGANE BIBLIOTEKI
- requests
- pandas
- retry-requests
- requests-cache
- phonenumbers

"""

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