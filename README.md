# supercalifragilisticexpialidocious

Hasif Ahmed, Shin Bamba, Tania Cao, Soojin Choi(PM)

## Stock Overflow

### Project Overview

### Launch Instructions
#### Running Flask App
1. Go to [root repository](https://github.com/Soojin-C/supercalifragilisticexpialidocious) and click "Clone or Download"
2. Copy the ssh/https link and run `$ git clone <link>`
3. Have the latest version of Python installed, which is currently Python 3.7.1. If not, download it [here](https://www.python.org/downloads/).
4. Install virtualenv by running `$ pip install virtualenv`
   * Make a venv by running `$ python3 -m venv VENV_NAME`
   * Activate it by running `$ . ~/path_to_venv/VENV_NAME/bin/activate`
   * Deactivate it by running `$ deactivate`
5. Install Flask and wheel with `$ pip3 install flask` and `$ pip3 install wheel` (this is a Flask application)
6. In the root of the directory, run `$ python app.py`. Make sure your virtual enviornment is actvated
7. Launch the root route (http://127.0.0.1:5000/) in your browser.

#### API information
Two APIs are used in this project:
###### IEX Trading
* Provides stock information given the company name
* This API doesn't require an API key. The documentation on how to use the api is [here](https://iextrading.com/developer/docs/#getting-started)
* Data provided for free by IEX. View IEX’s Terms of Use.
###### The New York Times
* Some interesting info
* Obtain an New York Times API key [here](some link)
