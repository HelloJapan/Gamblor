from config import *

def get_sport_name(span_elements):
    if len(span_elements) >= 2:
        # Check if the first span contains a country code (typically in parentheses)
        first_span_text = span_elements[0].text.strip()
        if first_span_text.startswith('(') and first_span_text.endswith(')'):
            # This is a country code, so the second span is likely the sport
            sport = span_elements[1].text.strip()
        else:
            # No country code, so the first span is the sport
            sport = first_span_text
    elif len(span_elements) == 1:
        # Only one span, assume it's the sport
        sport = span_elements[0].text.strip()
    return sport

def main():
    html_bytes = urlopen(req).read()
    html = html_bytes.decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")

    tbody_elements = soup.find_all('tbody', class_='valuebet_record')

    results = []

    for tbody in tbody_elements:
        # time_element = tbody.find('td', class_='time').find('abbr').get('data-utc')
        # date_of_event = datetime.fromtimestamp(int(time_element )/1000) # Convert milliseconds to datetime
        
        for td in tbody.find_all('td', class_='text-center'):
            if td.find('span', class_='overvalue'):
                overvalue_td = td
                break

        overvalue = tbody.get("data-overvalue").strip()
        probability = tbody.get("data-probability").strip()
        odds = tbody.get("data-value").strip()
        date_of_event = datetime.fromtimestamp(int(tbody.get("data-start-at")))
        bet = tbody.find('td', class_="coeff").find("abbr").text.strip()
        bookmaker = tbody.find(target="_blank").text.strip()

        minor_spans = tbody.find_all('span', class_="minor")
        sport = get_sport_name(minor_spans)

        event = tbody.find('td', class_="event").find(target="_blank").text.strip()

        data = Bet (
            bookmaker=bookmaker,
            sport=sport,
            date=date_of_event,
            event=event,
            odds=odds,
            probability=probability,
            overvalue=overvalue,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M") # Current timestamp
        )
            
        results.append(data)

    # Print the results
    for result in results:
        print(f"{"_"*100}\nBookmaker: {result.bookmaker}, \nSport: {result.sport}, \nDate of event: {result.date}, \nEvent: {result.event}, \nOdds: {result.odds}, \nProbability: {result.probability}, \nOvervalue: {result.overvalue}, \nTimestamp: {result.timestamp}\n{"_"*100}")

    with open('valuebets.csv', 'w', newline='', encoding="utf-8") as csvfile:
        bet_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        bet_writer.writerow(['bookmaker', 'sport', 'date', 'event', 'odds', 'probability', 'overvalue', 'timestamp'])
        
        # Count rows written for debugging
        rows_written = 0
        
        for result in results:
            bet_writer.writerow([
                result.bookmaker, 
                result.sport, 
                result.date, 
                result.event, 
                result.odds, 
                result.probability, 
                result.overvalue, 
                result.timestamp
            ])
            rows_written += 1
            
        print(f"Rows written: {rows_written}")

if __name__=="__main__":
    main()