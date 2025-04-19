from config import *

def main():
    path_to_browser = "C:/Program Files/Mozilla Firefox/firefox.exe"
    html_bytes = urlopen(results_req).read()
    html = html_bytes.decode("utf-8")
    data_dir = WindowsPath('D:/prog/gits/Gamblor/data')


    ws = sd.WhoScored(leagues="ENG-Premier League", seasons=2025, headless=False, path_to_browser=path_to_browser, data_dir=data_dir) 
    missing_players = ws.read_missing_players(match_id=1485184)
    missing_players.head()
    

if __name__=="__main__":
    main()