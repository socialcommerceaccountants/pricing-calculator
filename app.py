from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load pricing data from the spreadsheet
file_path = "SCA - Pricing Master.xlsx"
xls = pd.ExcelFile(file_path)
df = pd.read_excel(xls, sheet_name='Sheet1')

# Identify the rows where services and their prices start
services_start_row = 7  # Where "Bookkeeping" starts
services_end_row = 18   # Ends at "Cashflow Forecast"
revenue_columns = df.iloc[2, 3:9]  # Extract revenue tiers

# Extract services and pricing into a structured format
pricing_data = df.iloc[services_start_row:services_end_row+1, [0] + list(range(3, 9))]
pricing_data.columns = ["Service"] + list(revenue_columns)
pricing_data = pricing_data.dropna(subset=["Service"]).reset_index(drop=True)

@app.route('/')
def index():
    # Dynamically generate checkboxes from pricing data
    services_html = ""
    for service in pricing_data["Service"]:
        safe_service_name = service.replace(" ", "_").lower()  # Make it form-friendly
        services_html += f'<input type="checkbox" name="services" value="{safe_service_name}"> {service}<br>'

    return f'''
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
            <option value="90k-300k">£90k-£300k</option>
            <option value="300k-1M">£300k-£1m</option>
            <option value="1M-3M">£1m-£3m</option>
            <option value="3M-5M">£3m-£5m</option>
            <option value="5M-9M">£5m-£9m</option>
          </select>
          <br><br>

          <h3>Select Services:</h3>
          {services_html}

          <br><br>
          <input type="submit" value="Calculate Price">
        </form>
      </body>
    </html>
    '''

@app.route('/result', methods=['POST'])
def result():
    try:
        revenue_tier = request.form.get("revenue_tier")
        selected_services = request.form.getlist("services")

        total_price = 0
        for service in selected_services:
            service_name = service.replace("_", " ").title()
            service_price = pricing_data.loc[pricing_data["Service"].str.contains(service_name, case=False, na=False), revenue_tier].values
            if len(service_price) > 0:
                total_price += float(service_price[0])

        response_html = f'''
        <!doctype html>
        <html>
          <head>
            <title>Pricing Calculator Result</title>
          </head>
          <body>
            <h1>Total Price: £{total_price:.2f}</h1>
            <p><a href='/'>Calculate Again</a></p>
          </body>
        </html>
        '''
        return response_html
    except Exception as e:
        return f"Error processing request: {e}"

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    print("Using port:", port)
    app.run(host='0.0.0.0', port=port, debug=True)
