from config import *

def get_sport_name(span_elements: list) -> tuple:
    if len(span_elements) >= 2:
        # Check if the first span contains a country code (typically in parentheses)
        first_span_text = span_elements[0].text.strip()
        if first_span_text.startswith('(') and first_span_text.endswith(')'):
            # This is a country code, so the second span is likely the sport
            sport = span_elements[1].text.strip()
            league = span_elements[2].text.strip()
        else:
            # No country code, so the first span is the sport
            sport = span_elements[0].text.strip()
            league = span_elements[1].text.strip()
    elif len(span_elements) == 1:
        # Only one span, assume it's the sport
        sport = span_elements[0].text.strip()
        league = span_elements[1].text.strip()
    return (sport, league)

def merge_dataframes(bets_df: pd.DataFrame, new_bets_df: pd.DataFrame, bet_id: int) -> pd.DataFrame:
    new_bets_df['Bet id'] = None

    id_mapping = {}

    # Create mapping of existing keys to bet IDs
    for _, row in bets_df.iterrows():
        id_mapping[row['match_key']] = row['Bet id']

    # Assign IDs to new results
    for idx, row in new_bets_df.iterrows():
        match_key = row['match_key']
        if match_key in id_mapping:
            # This is an existing bet, use its ID
            new_bets_df.at[idx, 'Bet id'] = id_mapping[match_key]
        else:
            # This is a new bet, assign new ID and update mapping
            new_bets_df.at[idx, 'Bet id'] = bet_id
            id_mapping[match_key] = bet_id
            bet_id += 1

    new_bets_df = new_bets_df.drop('match_key', axis=1)
    bets_df = bets_df.drop('match_key', axis=1)

    combined_df = pd.concat([bets_df, new_bets_df], ignore_index=True)
    return combined_df

def main():
    try:
        bets_df = pd.read_csv('valuebets.csv')
        bet_id = bets_df['Bet id'].max() + 1 if not bets_df.empty else 1
    except Exception as e:
        bet_id = 1

    html_bytes = urlopen(surebets_req).read()
    html = html_bytes.decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")

    tbody_elements = soup.find_all('tbody', class_='valuebet_record')

    results = []

    for tbody in tbody_elements:
        overvalue = tbody.get("data-overvalue").strip()
        probability = tbody.get("data-probability").strip()
        odds = tbody.get("data-value").strip()
        date_of_event = datetime.fromtimestamp(int(tbody.get("data-start-at")))
        bet = tbody.find('td', class_="coeff").find("abbr").text.strip()
        bookmaker = tbody.find(target="_blank").text.strip()

        minor_spans = tbody.find_all('span', class_="minor")
        sport, league = get_sport_name(minor_spans)

        event = tbody.find('td', class_="event").find(target="_blank").text.strip()

        bet = {
            'Bookmaker': bookmaker,
            'Sport': sport,
            'League': league,
            'Date': date_of_event,
            'Event': event,
            'Bet': bet,
            'Odds': odds,
            'Probability': probability,
            'Overvalue': overvalue,
            'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M") # Current timestamp
        }
            
        results.append(bet)    
    
    new_bets_df = pd.DataFrame(results)

    bets_df['match_key'] = bets_df['Event'] + '|' + bets_df['Bet']
    new_bets_df['match_key'] = new_bets_df['Event'] + '|' + new_bets_df['Bet']

    # Combine datasets
    combined_df = merge_dataframes(bets_df, new_bets_df, bet_id)

    # Write back to CSV
    combined_df.to_csv('valuebets.csv', index=False)

if __name__=="__main__":
    main()