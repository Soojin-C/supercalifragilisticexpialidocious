# supercalifragilisticexpialidocious

Hasif Ahmed, Shin Bamba, Tania Cao, Soojin Choi(PM)

## Stock Overflow

### Project Overview
Stock Overflow is a website focusing on investment and financing education. Users will be able to read articles revelvant to the financial world and view information on a wide range of stocks. Users can take part in a simulation game where they have an initial buying power of $100, 000. With that money, they will be able to purchase or sell stocks. If the user is interested in certain stocks, they may add them to the watchlist to keep track of them. 

### Launch Instructions
#### Running Flask App
1. Go to [root repository](https://github.com/Soojin-C/supercalifragilisticexpialidocious) and click "Clone or Download"
2. Copy the ssh/https link and run `$ git clone <link>`
3. Have the latest version of Python installed, which is currently Python 3.7.1. If not, download it [here](https://www.python.org/downloads/).
4. Install virtualenv by running `$ pip install virtualenv`
   * Make a venv by running `$ python3 -m venv VENV_NAME`
   * Activate it by running `$ . ~/path_to_venv/VENV_NAME/bin/activate`
   * Deactivate it by running `$ deactivate`
5. Activate your virtual environment. 
6. In the root of the directory, run `$ pip install -r requirements.txt`
  * This will instal flask and wheel for you. Manually, you can run `$ pip install flask` and `$ pip install wheel`
7. To obtain API keys, look below for the instructions. Insert the obtained New York Times key into the file keys.json. 
8. Now you are ready to run the flask app. Run the command `$ python app.py`. (Make sure your virtual enviornment is actvated)
9. Launch the root route (http://127.0.0.1:5000/) in your browser.

#### API information
Two APIs are used in this project:
###### IEX Trading
* Provides stock information given the company name
* This API doesn't require an API key. The documentation on how to use the api is [here](https://iextrading.com/developer/docs/#getting-started)
* Data provided for free by IEX. View IEX’s Terms of Use.
###### The New York Times
* Provides the articles for the article search
* First make an account, then create a new app in order to obtain your API key
* Obtain an New York Times API key [here](https://developer.nytimes.com/get-started) Please select the API to Article Search API.
* Place the key to replace the "nyt key here" in the keys.json file,, which is in the keys directory.

