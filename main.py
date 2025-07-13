import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
import time
import os
from datetime import datetime

def clear_console():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def fetch_dividend_data():
    """
    Fetches and parses dividend data from Moneycontrol's updated card-based layout.

    Returns:
        A tuple containing a list of headers and a list of lists with row data.
        Returns (None, None) if fetching or parsing fails.
    """
    url = "https://www.moneycontrol.com/markets/corporate-action/dividends_declared/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return None, None

    soup = BeautifulSoup(response.text, 'html.parser')

    # UPDATED LOGIC (July 2025): Find the main container using the new class name.
    card_container = soup.find('div', class_='lhsGrayCard_web_grayBoxMain__3uS2_')

    if not card_container:
        print("Could not find the main dividend data container (div.lhsGrayCard_web_grayBoxMain__3uS2_). The website structure may have changed.")
        return None, None

    # UPDATED LOGIC: Find all individual company data blocks using the new class name.
    dividend_cards = card_container.find_all('div', class_='lhsGrayCard_web_lhsGrayCard__RSkQw')

    if not dividend_cards:
        print("Could not find any dividend cards (div.lhsGrayCard_web_lhsGrayCard__RSkQw) on the page.")
        return None, None

    # --- Define Headers and Prepare Data Rows ---
    # Headers will be dynamically updated based on user input for investment amount
    data_rows = []

    # Iterate over each card to extract information
    for card in dividend_cards:
        try:
            # UPDATED: Company Name is in an 'a' tag with a specific class
            company_tag = card.find('a', class_='lhsGrayCard_web_title__B2NJA')
            company_name = company_tag.get_text(strip=True) if company_tag else 'N/A'

            # UPDATED: Find all data points. They are in 'span's with class 'lhsGrayCard_web_values__DQOxi'
            values = card.find_all('span', class_='lhsGrayCard_web_values__DQOxi')

            # The LTP also has a percentage change next to it, which we'll combine.
            ltp_section = card.find('div', class_='lhsGrayCard_web_secondRow__BulOS').find('div', class_='lhsGrayCard_web_lhs__Bh6QQ')
            ltp_value_str = ltp_section.find('span', class_='lhsGrayCard_web_values__DQOxi').get_text(strip=True)
            try:
                ltp_value = float(ltp_value_str.replace(',', '')) # Convert to float, remove comma if present
            except ValueError:
                ltp_value = 0.0 # Default if conversion fails

            # The change can be in a red or green class
            change_red = ltp_section.find('span', class_='lhsGrayCard_web_redtext__dd7oX')
            change_green = ltp_section.find('span', class_='lhsGrayCard_web_greentext__zbrAw')
            change_gray = ltp_section.find('span', class_='lhsGrayCard_web_graytext__Qgy9W')

            if change_red:
                ltp_full = f"{ltp_value_str} {change_red.get_text(strip=True)}"
            elif change_green:
                ltp_full = f"{ltp_value_str} {change_green.get_text(strip=True)}"
            elif change_gray:
                ltp_full = f"{ltp_value_str} {change_gray.get_text(strip=True)}"
            else:
                ltp_full = ltp_value_str

            # Extract other values based on their order
            dividend_str = values[1].get_text(strip=True) if len(values) > 1 else '0.0'
            try:
                dividend = float(dividend_str)
            except ValueError:
                dividend = 0.0

            ann_date_str = values[2].get_text(strip=True) if len(values) > 2 else 'N/A'
            ex_date_str = values[3].get_text(strip=True) if len(values) > 3 else 'N/A'

            data_rows.append({
                'Company': company_name,
                'LTP & Change': ltp_full,
                'LTP': ltp_value, # Store raw LTP for calculations
                'Dividend (Rs)': dividend, # Store raw dividend for calculations
                'Ann. Date': ann_date_str,
                'Ex-Date': ex_date_str
            })

        except (AttributeError, IndexError) as e:
            # This handles cases where a card might be structured unexpectedly (e.g., an ad)
            # print(f"Skipping a card due to parsing error: {e}")
            continue

    return data_rows

if __name__ == "__main__":
    try:
        clear_console()
        print("Fetching latest dividend data from Moneycontrol...")
        print("-" * 50)

        raw_data = fetch_dividend_data()

        if raw_data:
            while True:
                try:
                    investment_amount = float(input("Enter the amount you wish to invest (e.g., 10000): "))
                    if investment_amount <= 0:
                        print("Please enter a positive investment amount.")
                        continue
                    break
                except ValueError:
                    print("Invalid input. Please enter a numerical value for the investment amount.")

            processed_data = []
            today = datetime.now().date()

            for row in raw_data:
                company_name = row['Company']
                ltp_full = row['LTP & Change']
                ltp = row['LTP']
                dividend_per_share = row['Dividend (Rs)']
                ann_date_str = row['Ann. Date']
                ex_date_str = row['Ex-Date']

                quantity = 0
                total_invested = 0.0
                total_dividend = 0.0
                status = "N/A"

                if ltp > 0:
                    quantity = int(investment_amount // ltp) # Round down to whole shares
                    total_invested = round(quantity * ltp, 2)
                    total_dividend = round(quantity * dividend_per_share, 2)

                # Determine status based on Ex-Date
                try:
                    # Assuming Ex-Date format is DD/MM/YYYY
                    ex_date_dt = datetime.strptime(ex_date_str, '%d/%m/%Y').date()
                    # A stock is 'Active' if its ex-date is strictly after today.
                    # If ex-date is today or in the past, it's 'Inactive' for dividend eligibility.
                    if ex_date_dt > today:
                        status = "Active"
                    else:
                        status = "Inactive"
                except ValueError:
                    status = "Unknown Date" # If date parsing fails

                processed_data.append([
                    company_name,
                    ltp_full,
                    f"{dividend_per_share:.2f}", # Format dividend to 2 decimal places
                    quantity,
                    f"{total_invested:.2f}", # Format total invested to 2 decimal places
                    f"{total_dividend:.2f}", # Format total dividend to 2 decimal places
                    status,
                    ex_date_str,
                    ann_date_str
                ])

            output_headers = [
                'Company',
                'LTP & Change',
                'Dividend (Rs)',
                'Quantity',
                'Total Amt Invested',
                'Potential Dividend',
                'Status',
                'Ex-Date',
                'Ann. Date'
            ]

            # Use the tabulate library to print a formatted table
            print(tabulate(processed_data, headers=output_headers, tablefmt="grid"))
            print(f"\nData retrieved on: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print("Failed to retrieve or parse data. The website layout may have changed again.")

    except KeyboardInterrupt:
        print("\nProcess interrupted by user. Exiting.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")