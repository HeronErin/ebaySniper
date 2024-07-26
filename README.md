# Python Ebay Item Sniper


A simple, bare bones, ebay item sniper. 



## How to use

1. Get a cookies.json file for Ebay.
	* Download the [Get cookies.txt LOCALLY](https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc) chrome extension
	* Navigate to [Ebay.com ](https://www.ebay.com/) while signed in
	* **Switch the output format into JSON**
	* Click the export button and download it into the config folder.
	* It must be named exactally `cookies.json`
2. Create a `config.json` file in the config folder. The following is an example of a `config.json` file. It must include a target, max, and delay. It can optionally include a infoDumpChk, and predelay. 
```json
{
	"infoDumpChk": 900,

	"target": "226260428932",
	"max": 69420,
	"delay": 10,
	"predelay": 90
}
```
	- target: The ebay item id of the auction (from the url bar).
	- max: The max price of the item you will accept.
	- delay: Time before the auction ends to place the bid.
	- predelay: An optional field of how long before the aucion ends to open the webpage and check if you are still signed in.
	- infoDumpChk: An optional field of the interval at which to wait before checking the price again and print it to the screen.
3. Install the dependencies. Use the following command it get the python requirements, you will also need to download the selenium [driver file](https://selenium-python.readthedocs.io/installation.html#drivers) for chrome, put it next to the python files for simplicity. 
```bash
pip install selenium requests pytz
```
4. Run the program
```bash
python main.py
```


## Legal
```plaintext
	Copyright (c) 2024 HeronErin

	Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

	The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```




