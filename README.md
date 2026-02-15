StockThresholdMonitor



A small project I made to track a few stocks and get a ping when one drops below a price I care about.

It started as a PowerShell script that could only watch one stock at a time, so I upgraded it to Python with a simple Tkinter GUI and API calls



Features



-Track up to 5 stocks at once



-Set a price threshold and get alerts



-Clean GUI with Tkinter



-Handles API rate limits so you don’t spam Alpha Vantage and get hit the APi limit



How to Run



1\. Install dependencies:

&nbsp;  pip install requests

2\. Get a Alpha Vantage API key its free on their site. Set your Alpha Vantage API key as an environment variable. Or hard code it like API\_KEY = "api key from Alpha Vantage"

3\. Run:

&nbsp;  python stocktracker.py



How to use



-Enter stock symbols (e.g., AAPL) and threshold prices.



-Click ADD TO LIST to track a stock.



-Select a row and click remove selected row to delete it.



-The program checks prices every 60 minutes by default and alerts you with a popup if a stock falls below its threshold.



Why I Built This



A personal project to experiment with using a API and implement some of the Tkinter and GUI development knowledge I leant in university.

