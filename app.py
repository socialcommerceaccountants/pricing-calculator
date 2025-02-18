from flask import Flask, request, jsonify

app = Flask(__name__)

# Base pricing per revenue tier
pricing_tiers = {
    "0-90k": 150,
    "90k-300k": 250,
    "300k-1M": 400,
    "1M+": 600
}

# Multipliers
marketplace_multiplier = 0.025  # 2.5% per extra marketplace
software_penalty = 0.05  # 5% increase if no automation software is used
multi_currency_multiplier = 0.03  # 3% if multi-currency is applicable
stock_management_multiplier = 0.04  # 4% for stock/inventory management

# Additional Services
additional_services = {
    "extra_payroll": 20,
    "vat_filings": 50,
    "management_accounts": 100,
    "advisory_calls": 75
}

@app.route('/calculate_price', methods=['POST'])
def calculate_price():
    data = request.json

    revenue_tier = data.get("revenue_tier")
    base_price = pricing_tiers.get(revenue_tier, 0)

    num_marketplaces = max(0, data.get("num_marketplaces", 1) - 1)
    marketplace_fee = base_price * marketplace_multiplier * num_marketplaces

    software_used = data.get("software_used", True)
    software_fee = 0 if software_used else base_price * software_penalty

    multi_currency = data.get("multi_currency", False)
    multi_currency_fee = base_price * multi_currency_multiplier if multi_currency else 0

    stock_management = data.get("stock_management", False)
    stock_fee = base_price * stock_management_multiplier if stock_management else 0

    payroll_count = max(0, data.get("extra_payroll", 0))
    payroll_fee = payroll_count * additional_services["extra_payroll"]

    vat_filings = max(0, data.get("vat_filings", 0))
    vat_fee = vat_filings * additional_services["vat_filings"]

    management_accounts = max(0, data.get("management_accounts", 0))
    management_fee = management_accounts * additional_services["management_accounts"]

    advisory_calls = max(0, data.get("advisory_calls", 0))
    advisory_fee = advisory_calls * additional_services["advisory_calls"]

    total_price = (
        base_price + marketplace_fee + software_fee + multi_currency_fee +
        stock_fee + payroll_fee + vat_fee + management_fee + advisory_fee
    )

    return jsonify({"total_price": total_price})
@app.route('/')
def index():
    return '''
    <!doctype html>
    <html>
      <head>
        <title>Pricing Calculator</title>
      </head>
      <body>
        <h1>Pricing Calculator</h1>
        <form action="/result" method="post">
          <label for="revenue_tier">Revenue Tier:</label>
          <select name="revenue_tier" id="revenue_tier">
            <option value="0-90k">£0-90k</option>
            <option value="90k-300k">£90k-300k</option>
            <option value="300k-1M">£300k-1M</option>
            <option value="1M+">£1M+</option>
          </select>
          <br><br>
          <label for="num_marketplaces">Number of Marketplaces:</label>
          <input type="number" id="num_marketplaces" name="num_marketplaces" value="1">
          <br><br>
          <label for="software_used">Uses Software (true/false):</label>
          <input type="text" id="software_used" name="software_used" value="true">
          <br><br>
          <label for="multi_currency">Multi-currency (true/false):</label>
          <input type="text" id="multi_currency" name="multi_currency" value="false">
          <br><br>
          <label for="stock_management">Stock management (true/false):</label>
          <input type="text" id="stock_management" name="stock_management" value="false">
          <br><br>
          <label for="extra_payroll">Extra payroll employees:</label>
          <input type="number" id="extra_payroll" name="extra_payroll" value="0">
          <br><br>
          <label for="vat_filings">VAT filings:</label>
          <input type="number" id="vat_filings" name="vat_filings" value="0">
          <br><br>
          <label for="management_accounts">Management accounts:</label>
          <input type="number" id="management_accounts" name="management_accounts" value="0">
          <br><br>
          <label for="advisory_calls">Advisory calls:</label>
          <input type="number" id="advisory_calls" name="advisory_calls" value="0">
          <br><br>
          <input type="submit" value="Calculate Price">
        </form>
      </body>
    </html>
    '''

@app.route('/result', methods=['POST'])
def result():
    # Get form data and convert where needed
    revenue_tier = request.form.get("revenue_tier")
@app.route('/result', methods=['POST'])
def result():
    try:
        # Get and process form data
        revenue_tier = request.form.get("revenue_tier")
        base_price = pricing_tiers.get(revenue_tier, 0)

        num_marketplaces = max(0, int(request.form.get("num_marketplaces", 1)) - 1)
        marketplace_fee = base_price * marketplace_multiplier * num_marketplaces

        software_used = request.form.get("software_used", "true").lower() == "true"
        software_fee = 0 if software_used else base_price * software_penalty

        multi_currency = request.form.get("multi_currency", "false").lower() == "true"
        multi_currency_fee = base_price * multi_currency_multiplier if multi_currency else 0

        stock_management = request.form.get("stock_management", "false").lower() == "true"
        stock_fee = base_price * stock_management_multiplier if stock_management else 0

        payroll_count = max(0, int(request.form.get("extra_payroll", 0)))
        payroll_fee = payroll_count * additional_services["extra_payroll"]

        vat_filings = max(0, int(request.form.get("vat_filings", 0)))
        vat_fee = vat_filings * additional_services["vat_filings"]

        management_accounts = max(0, int(request.form.get("management_accounts", 0)))
        management_fee = management_accounts * additional_services["management_accounts"]

        advisory_calls = max(0, int(request.form.get("advisory_calls", 0)))
        advisory_fee = advisory_calls * additional_services["advisory_calls"]

        total_price = (
            base_price + marketplace_fee + software_fee + multi_currency_fee +
            stock_fee + payroll_fee + vat_fee + management_fee + advisory_fee
        )

        # Log the calculated total for debugging
        print("Calculated total_price:", total_price)

        # Build the HTML response as a single string
        response_html = (
            "<!doctype html>"
            "<html><head><title>Pricing Calculator Result</title></head>"
            "<body>"
            f"<h1>Total Price: £{total_price}</h1>"
            "<p><a href='/'>Calculate Again</a></p>"
            "</body></html>"
        )
        return response_html
    except Exception as e:
        print("Error processing request:", e)
        return f"Error processing request: {e}"

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    print("Using port:", port)
    app.run(host='0.0.0.0', port=port, debug=True)
