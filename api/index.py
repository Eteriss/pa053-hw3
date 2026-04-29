from flask import Flask, request, jsonify
import requests
import ast
import operator
import yfinance as yf

app = Flask(__name__)

# Airport temperature
def get_airport_temp(iata):
    r = requests.get(f"https://airport-data.com/api/ap_info.json?iata={iata}", timeout=10)
    r.raise_for_status()
    data = r.json()
    lat = data["latitude"]
    lon = data["longitude"]

    w = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={"latitude": lat, "longitude": lon, "current_weather": True},
        timeout=10
    )
    w.raise_for_status()
    return w.json()["current_weather"]["temperature"]

# Stock price
def get_stock_price(symbol):
    ticker = yf.Ticker(symbol)
    price = ticker.fast_info.last_price
    return float(price)

# Arithemtic eval
OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,
}

def safe_eval(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    elif isinstance(node, ast.BinOp) and type(node.op) in OPS:
        return OPS[type(node.op)](safe_eval(node.left), safe_eval(node.right))
    elif isinstance(node, ast.UnaryOp) and type(node.op) in OPS:
        return OPS[type(node.op)](safe_eval(node.operand))
    else:
        raise ValueError(f"Unsupported operation: {ast.dump(node)}")

@app.route("/")
def index():
    airport = request.args.get("queryAirportTemp")
    stock   = request.args.get("queryStockPrice")
    expr    = request.args.get("queryEval")

    try:
        if airport:
            return jsonify(get_airport_temp(airport.upper()))
        elif stock:
            return jsonify(get_stock_price(stock.upper()))
        elif expr:
            tree = ast.parse(expr, mode="eval")
            return jsonify(safe_eval(tree.body))
        else:
            return jsonify({"error": "Provide one query param: queryAirportTemp, queryStockPrice, or queryEval"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500