from flask import Flask
from flask import jsonify
from bs4 import BeautifulSoup
import requests


def get_currency(input_currency, output_currency, amount):
    url = f"https://www.x-rates.com/calculator/?from={input_currency}&to={output_currency}&amount={amount}"
    content = requests.get(url).text
    soup = BeautifulSoup(content, 'html.parser')
    currency = soup.find("span", class_="ccOutputRslt").get_text()

    return get_float_currency(currency.replace(",", ""))


def get_float_currency(text):                   # It's important to return the correct data type.
    result = float(text.split(" ")[0])          # Best practice is to use print functions outside your custom functions.
    return result


app = Flask(__name__)


@app.route('/')
def home():  # put application's code here
    return '<h1>Currency Rate API - by Christian Perez</h1> <p>Example URL: /api/v1/usd-eur-1</p>' \
           '' \
           '<body><small>Thanks to X-Rates for Data!</small></body>'


@app.route('/api/v1/<in_cur>-<out_cur>-<amount>')
def api(in_cur, out_cur, amount):
    rate = get_currency(in_cur, out_cur, amount)
    result_dict = {'Input_Currency': in_cur, 'Output_Currency': out_cur, 'Initial Amount': amount, 'Final Amount': rate}
    return jsonify(result_dict)


if __name__ == '__main__':
    app.run()

# Flask is best for creating smaller web apps.
