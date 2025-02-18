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
software_penalty = 0.05         # 5% increase if no automation software is used
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

    payroll_count = max(0, data.ge
