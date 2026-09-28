from flask import Flask, jsonify, request
from datetime import datetime, timedelta
from collections import defaultdict, deque
from threading import Lock
import re, random, time

app = Flask(__name__)

# ============================================================
# CONFIG — canteen-wide settings live here
# ============================================================
CONFIG = {
    "name": "Campus Bites",
    "location": "Main Academic Block, Campus",
    "opening_hour": 8,
    "closing_hour": 20,
    "tax_rate": 0.0,
    "currency": "₹",
    "cancellation_grace_minutes": 2,
    "base_queue_minutes": 2,
    "queue_order_minutes": 3,
    "rate_limit_window": 60,
    "rate_limit_max": 20,
}

MENU = {
    "Monday": [
        {"id":101,"name":"Masala Dosa","price":40,"category":"Breakfast","description":"Crispy dosa with chutney and sambar","image":"https://images.unsplash.com/photo-1668236543090-82eba5ee5976?auto=format&fit=crop&w=900&q=80","popular":True,"veg":True,"spice_level":1,"allergens":["dairy"],"available":True,"prep_time_minutes":6,"sold_count":0},
        {"id":102,"name":"Poha","price":30,"category":"Breakfast","description":"Light flattened rice with peanuts and herbs","image":"https://images.unsplash.com/photo-1601050690597-df0568f70950?auto=format&fit=crop&w=900&q=80","popular":False,"veg":True,"spice_level":1,"allergens":["peanuts"],"available":True,"prep_time_minutes":4,"sold_count":0},
        {"id":103,"name":"Veg Thali","price":90,"category":"Lunch","description":"Dal, two vegetables, rice, roti and salad","image":"https://images.unsplash.com/photo-1546833999-b9f581a1996d?auto=format&fit=crop&w=900&q=80","popular":True,"veg":True,"spice_level":2,"allergens":["dairy"],"available":True,"prep_time_minutes":10,"sold_count":0},
        {"id":104,"name":"Paneer Roll","price":65,"category":"Snacks","description":"Soft roll packed with spicy paneer filling","image":"https://images.unsplash.com/photo-1626700051175-6818013e1d4f?auto=format&fit=crop&w=900&q=80","popular":True,"veg":True,"spice_level":2,"allergens":["dairy","gluten"],"available":True,"prep_time_minutes":7,"sold_count":0},
        {"id":105,"name":"Cold Coffee","price":45,"category":"Beverages","description":"Chilled creamy coffee","image":"https://images.unsplash.com/photo-1461023058943-07fcbe16d735?auto=format&fit=crop&w=900&q=80","popular":True,"veg":True,"spice_level":0,"allergens":["dairy"],"available":True,"prep_time_minutes":3,"sold_count":0},
        {"id":106,"name":"Gulab Jamun","price":25,"category":"Dessert","description":"Soft warm syrup-soaked dumplings","image":"https://images.unsplash.com/photo-1601050690117-94f5f6fa8bd7?auto=format&fit=crop&w=900&q=80","popular":False,"veg":True,"spice_level":0,"allergens":["dairy","gluten"],"available":True,"prep_time_minutes":2,"sold_count":0},
    ],
    "Tuesday": [
        {"id":201,"name":"Idli Sambar","price":35,"category":"Breakfast","description":"Steamed idlis with hot sambar","image":"https://images.unsplash.com/photo-1589301760014-d929f3979dbc?auto=format&fit=crop&w=900&q=80","popular":True,"veg":True,"spice_level":1,"allergens":[],"available":True,"prep_time_minutes":5,"sold_count":0},
        {"id":202,"name":"Aloo Paratha","price":45,"category":"Breakfast","description":"Stuffed paratha with curd and pickle","image":"https://images.unsplash.com/photo-1601050690117-94f5f6fa8bd7?auto=format&fit=crop&w=900&q=80","popular":True,"veg":True,"spice_level":2,"allergens":["dairy","gluten"],"available":True,"prep_time_minutes":7,"sold_count":0},
        {"id":203,"name":"Rajma Rice","price":75,"category":"Lunch","description":"Rajma curry served with steamed rice","image":"https://images.unsplash.com/photo-1601050690597-df0568f70950?auto=format&fit=crop&w=900&q=80","popular":True,"veg":True,"spice_level":2,"allergens":[],"available":True,"prep_time_minutes":9,"sold_count":0},
        {"id":204,"name":"Veg Sandwich","price":50,"category":"Snacks","description":"Toasted sandwich with fresh vegetables","image":"https://images.unsplash.com/photo-1528735602780-2552fd46c7af?auto=format&fit=crop&w=900&q=80","popular":False,"veg":True,"spice_level":1,"allergens":["gluten"],"available":True,"prep_time_minutes":5,"sold_count":0},
        {"id":205,"name":"Masala Chai","price":20,"category":"Beverages","description":"Indian spiced tea","image":"https://images.unsplash.com/photo-1594631252845-29fc4cc8cde9?auto=format&fit=crop&w=900&q=80","popular":True,"veg":True,"spice_level":0,"allergens":["dairy"],"available":True,"prep_time_minutes":2,"sold_count":0},
        {"id":206,"name":"Brownie","price":35,"category":"Dessert","description":"Warm chocolate brownie","image":"https://images.unsplash.com/photo-1606313564200-e75d5e30476c?auto=format&fit=crop&w=900&q=80","popular":False,"veg":True,"spice_level":0,"allergens":["dairy","gluten"],"available":True,"prep_time_minutes":3,"sold_count":0},
    ],
    "Wednesday": [
        {"id":301,"name":"Masala Uttapam","price":45,"category":"Breakfast","description":"Thick uttapam topped with vegetables","image":"https://images.unsplash.com/photo-1630383249896-424e482df921?auto=format&fit=crop&w=900&q=80","popular":True,"veg":True,"spice_level":1,"allergens":[],"available":True,"prep_time_minutes":6,"sold_count":0},
        {"id":302,"name":"Veg Pulao","price":70,"category":"Lunch","description":"Fragrant rice with seasonal vegetables","image":"https://images.unsplash.com/photo-1596797038530-2c107229654b?auto=format&fit=crop&w=900&q=80","popular":True,"veg":True,"spice_level":2,"allergens":[],"available":True,"prep_time_minutes":8,"sold_count":0},
        {"id":303,"name":"Chole Bhature","price":80,"category":"Lunch","description":"Spiced chickpeas with fluffy bhature","image":"https://images.unsplash.com/photo-1626132647523-66f5bf380027?auto=format&fit=crop&w=900&q=80","popular":True,"veg":True,"spice_level":2,"allergens":["gluten"],"available":True,"prep_time_minutes":10,"sold_count":0},
        {"id":304,"name":"Samosa","price":20,"category":"Snacks","description":"Crispy potato-filled samosa","image":"https://images.unsplash.com/photo-1601050690597-df0568f70950?auto=format&fit=crop&w=900&q=80","popular":True,"veg":True,"spice_level":2,"allergens":["gluten"],"available":True,"prep_time_minutes":4,"sold_count":0},
        {"id":305,"name":"Lemon Soda","price":25,"category":"Beverages","description":"Refreshing sweet and salty lemon soda","image":"https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?auto=format&fit=crop&w=900&q=80","popular":False,"veg":True,"spice_level":0,"allergens":[],"available":True,"prep_time_minutes":2,"sold_count":0},
        {"id":306,"name":"Fruit Custard","price":40,"category":"Dessert","description":"Chilled vanilla custard with fruit","image":"https://images.unsplash.com/photo-1488477181946-6428a0291777?auto=format&fit=crop&w=900&q=80","popular":False,"veg":True,"spice_level":0,"allergens":["dairy"],"available":True,"prep_time_minutes":4,"sold_count":0},
    ],
    "Thursday": [
        {"id":401,"name":"Methi Thepla","price":40,"category":"Breakfast","description":"Gujarati-style flatbread with curd","image":"https://images.unsplash.com/photo-1601050690597-df0568f70950?auto=format&fit=crop&w=900&q=80","popular":False,"veg":True,"spice_level":1,"allergens":["dairy","gluten"],"available":True,"prep_time_minutes":5,"sold_count":0},
        {"id":402,"name":"Dal Tadka Rice","price":65,"category":"Lunch","description":"Yellow dal tempered with spices and rice","image":"https://images.unsplash.com/photo-1546833999-b9f581a1996d?auto=format&fit=crop&w=900&q=80","popular":True,"veg":True,"spice_level":1,"allergens":[],"available":True,"prep_time_minutes":8,"sold_count":0},
        {"id":403,"name":"Paneer Butter Masala","price":95,"category":"Lunch","description":"Creamy tomato paneer with roti","image":"https://images.unsplash.com/photo-1631452180519-c014fe946bc7?auto=format&fit=crop&w=900&q=80","popular":True,"veg":True,"spice_level":2,"allergens":["dairy","gluten"],"available":True,"prep_time_minutes":11,"sold_count":0},
        {"id":404,"name":"Vada Pav","price":30,"category":"Snacks","description":"Mumbai-style potato fritter bun","image":"https://images.unsplash.com/photo-1601050690117-94f5f6fa8bd7?auto=format&fit=crop&w=900&q=80","popular":True,"veg":True,"spice_level":2,"allergens":["gluten"],"available":True,"prep_time_minutes":5,"sold_count":0},
        {"id":405,"name":"Cold Coffee","price":45,"category":"Beverages","description":"Chilled creamy coffee","image":"https://images.unsplash.com/photo-1461023058943-07fcbe16d735?auto=format&fit=crop&w=900&q=80","popular":True,"veg":True,"spice_level":0,"allergens":["dairy"],"available":True,"prep_time_minutes":3,"sold_count":0},
        {"id":406,"name":"Ice Cream Cup","price":30,"category":"Dessert","description":"Creamy vanilla ice cream","image":"https://images.unsplash.com/photo-1563805042-7684c019e1cb?auto=format&fit=crop&w=900&q=80","popular":False,"veg":True,"spice_level":0,"allergens":["dairy"],"available":True,"prep_time_minutes":2,"sold_count":0},
    ],
    "Friday": [
        {"id":501,"name":"Misal Pav","price":55,"category":"Breakfast","description":"Spicy sprouted curry with pav","image":"https://images.unsplash.com/photo-1601050690117-94f5f6fa8bd7?auto=format&fit=crop&w=900&q=80","popular":True,"veg":True,"spice_level":3,"allergens":["gluten"],"available":True,"prep_time_minutes":7,"sold_count":0},
        {"id":502,"name":"Veg Biryani","price":85,"category":"Lunch","description":"Aromatic vegetable biryani with raita","image":"https://images.unsplash.com/photo-1563379091339-03246963d51a?auto=format&fit=crop&w=900&q=80","popular":True,"veg":True,"spice_level":2,"allergens":["dairy"],"available":True,"prep_time_minutes":10,"sold_count":0},
        {"id":503,"name":"Chicken Biryani","price":110,"category":"Lunch","description":"Fragrant chicken biryani with raita","image":"https://images.unsplash.com/photo-1563379091339-03246963d51a?auto=format&fit=crop&w=900&q=80","popular":True,"veg":False,"spice_level":2,"allergens":["dairy"],"available":True,"prep_time_minutes":12,"sold_count":0},
        {"id":504,"name":"French Fries","price":45,"category":"Snacks","description":"Crispy salted potato fries","image":"https://images.unsplash.com/photo-1573080496219-bb080dd4f877?auto=format&fit=crop&w=900&q=80","popular":True,"veg":True,"spice_level":1,"allergens":[],"available":True,"prep_time_minutes":5,"sold_count":0},
        {"id":505,"name":"Mango Lassi","price":45,"category":"Beverages","description":"Thick chilled mango lassi","image":"https://images.unsplash.com/photo-1577805947697-89e18249d767?auto=format&fit=crop&w=900&q=80","popular":True,"veg":True,"spice_level":0,"allergens":["dairy"],"available":True,"prep_time_minutes":3,"sold_count":0},
        {"id":506,"name":"Rasmalai","price":45,"category":"Dessert","description":"Soft cottage-cheese dumplings in milk","image":"https://images.unsplash.com/photo-1601050690597-df0568f70950?auto=format&fit=crop&w=900&q=80","popular":False,"veg":True,"spice_level":0,"allergens":["dairy"],"available":True,"prep_time_minutes":3,"sold_count":0},
    ],
    "Saturday": [
        {"id":601,"name":"Chole Kulche","price":60,"category":"Breakfast","description":"Spiced chickpeas with soft kulcha","image":"https://images.unsplash.com/photo-1626132647523-66f5bf380027?auto=format&fit=crop&w=900&q=80","popular":True,"veg":True,"spice_level":2,"allergens":["gluten"],"available":True,"prep_time_minutes":7,"sold_count":0},
        {"id":602,"name":"Veg Fried Rice","price":70,"category":"Lunch","description":"Wok-tossed rice with vegetables","image":"https://images.unsplash.com/photo-1603133872878-684f208fb84b?auto=format&fit=crop&w=900&q=80","popular":True,"veg":True,"spice_level":2,"allergens":["soy"],"available":True,"prep_time_minutes":8,"sold_count":0},
        {"id":603,"name":"Hakka Noodles","price":75,"category":"Lunch","description":"Stir-fried noodles with vegetables","image":"https://images.unsplash.com/photo-1569718212165-3a8278d5f624?auto=format&fit=crop&w=900&q=80","popular":True,"veg":True,"spice_level":2,"allergens":["gluten","soy"],"available":True,"prep_time_minutes":8,"sold_count":0},
        {"id":604,"name":"Pakora Plate","price":40,"category":"Snacks","description":"Assorted crispy vegetable fritters","image":"https://images.unsplash.com/photo-1601050690117-94f5f6fa8bd7?auto=format&fit=crop&w=900&q=80","popular":False,"veg":True,"spice_level":2,"allergens":["gluten"],"available":True,"prep_time_minutes":5,"sold_count":0},
        {"id":605,"name":"Masala Chai","price":20,"category":"Beverages","description":"Indian spiced tea","image":"https://images.unsplash.com/photo-1594631252845-29fc4cc8cde9?auto=format&fit=crop&w=900&q=80","popular":True,"veg":True,"spice_level":0,"allergens":["dairy"],"available":True,"prep_time_minutes":2,"sold_count":0},
        {"id":606,"name":"Gulab Jamun","price":25,"category":"Dessert","description":"Soft warm syrup-soaked dumplings","image":"https://images.unsplash.com/photo-1601050690117-94f5f6fa8bd7?auto=format&fit=crop&w=900&q=80","popular":True,"veg":True,"spice_level":0,"allergens":["dairy","gluten"],"available":True,"prep_time_minutes":2,"sold_count":0},
    ],
}

ORDERS, BILLS = {}, {}
NEXT_BILL_ID = 1001
FEEDBACK = {"up": 0, "down": 0}
RATE_LOG = defaultdict(deque)
BILL_LOCK = Lock()

ADDONS = {
    "extra_cheese": {"name":"Extra cheese", "price":15},
    "no_onion": {"name":"No onion", "price":0},
    "extra_spicy": {"name":"Extra spicy", "price":5},
}

def dish_id(item):
    return re.sub(r"[^a-z0-9]+", "_", item["name"].lower()).strip("_")

def public_item(item):
    x = dict(item)
    x["dish_id"] = dish_id(item)
    x["variants"] = x.get("variants", [{"id":"full","name":"Full","price":item["price"]},{"id":"half","name":"Half","price":max(10, round(item["price"]*0.65))}])
    x["addons"] = x.get("addons", ADDONS)
    return x

def now():
    return datetime.now()

def current_day():
    return now().strftime("%A")

def find_item(item_id, day=None):
    day = day or current_day()
    for item in MENU.get(day, []):
        if item["id"] == item_id:
            return item
    return None

def rate_ok():
    ip = request.remote_addr or "local"
    q = RATE_LOG[ip]
    cutoff = time.time() - CONFIG["rate_limit_window"]
    while q and q[0] < cutoff:
        q.popleft()
    if len(q) >= CONFIG["rate_limit_max"]:
        return False
    q.append(time.time())
    return True

def eta_for(items):
    slowest = max((find_item(x["item_id"])["prep_time_minutes"] for x in items if find_item(x["item_id"])), default=0)
    queue = sum(1 for b in BILLS.values() if b["status"] in ("received", "preparing"))
    return CONFIG["base_queue_minutes"] + slowest + queue * CONFIG["queue_order_minutes"]

def calculate_bill(items):
    subtotal = sum(i["price"] * i["quantity"] for i in items)
    tax = round(subtotal * CONFIG["tax_rate"], 2)
    return subtotal, tax, round(subtotal + tax, 2)

def update_lifecycle(bill):
    if bill["status"] in ("cancelled", "completed"):
        return
    elapsed = (now() - datetime.fromisoformat(bill["placed_at"])).total_seconds()
    prep = max(4, bill["ready_eta_minutes"] * 60)
    if elapsed >= prep + 30 * 60:
        bill["status"] = "ready"
    elif elapsed >= prep:
        bill["status"] = "ready"
    elif elapsed >= min(30, max(20, prep * 0.35)):
        bill["status"] = "preparing"

def combos(menu, budget, category_hint=None):
    available = [x for x in menu if x["available"]]
    if category_hint:
        hinted = [x for x in available if x["category"].lower() == category_hint.lower()]
        others = [x for x in available if x not in hinted]
        available = hinted + others
    available = sorted(available, key=lambda x: (not x["popular"], x["price"]))
    results = []
    # Simple pair/triple generator, bounded for predictable V1 behavior.
    for a in available:
        if a["price"] <= budget:
            results.append([a])
        for b in available:
            if b["id"] <= a["id"]:
                continue
            total = a["price"] + b["price"]
            if total <= budget:
                if category_hint and not (a["category"].lower() == category_hint.lower() or b["category"].lower() == category_hint.lower()):
                    continue
                results.append([a,b])
                for c in available:
                    if c["id"] <= b["id"]:
                        continue
                    t = total + c["price"]
                    if t <= budget:
                        results.append([a,b,c])
                    if len(results) >= 40:
                        break
            if len(results) >= 40:
                break
        if len(results) >= 40:
            break
    # Prefer fuller combos without exceeding budget, then lower total.
    results = sorted(results, key=lambda r: (-len(r), sum(x["price"] for x in r)))
    unique = []
    seen = set()
    for r in results:
        key = tuple(x["id"] for x in r)
        if key not in seen:
            seen.add(key)
            unique.append(r)
        if len(unique) >= 10:
            break
    return [{"items":[{"item_id":x["id"],"name":x["name"],"price":x["price"]} for x in r],
             "total":sum(x["price"] for x in r)} for r in unique]

def parse_budget(text):
    m = re.search(r"(?:₹|rs\.?|inr)?\s*(\d{2,4})", text.lower())
    return int(m.group(1)) if m else None

def chatbot(message):
    text = message.lower().strip()
    day = current_day()
    menu = MENU[day]
    if "where" in text and ("order" in text or "bill" in text):
        ids = re.findall(r"\b10\d{2,4}\b", text)
        if ids:
            bid = int(ids[-1])
            bill = BILLS.get(bid)
            if not bill: return {"type":"text","message":f"I couldn't find bill #{bid}."}
            update_lifecycle(bill)
            return {"type":"status","bill_id":bid,"status":bill["status"],"ready_eta_minutes":max(0, bill["ready_eta_minutes"] - int((now()-datetime.fromisoformat(bill["placed_at"])).total_seconds()/60)),
                    "message":f"Bill #{bid} is {bill['status'].replace('_',' ')}."}
        return {"type":"text","message":"Sure — tell me your bill number, like “where is order 1004?”"}
    if any(k in text for k in ["surprise", "recommend", "what's good", "whats good"]):
        candidates = [x for x in menu if x["available"]]
        if not candidates:
            return {"type":"text","message":"Looks like everything is sold out right now — check back soon!"}
        item = sorted(candidates, key=lambda x:(-x["sold_count"], not x["popular"]))[0]
        return {"type":"recommendation","item":{"item_id":item["id"],"name":item["name"],"price":item["price"]},
                "message":f"Try the {item['name']} — ₹{item['price']}. Want me to add it?"}
    if any(k in text for k in ["time", "open", "close", "timing", "hours"]):
        return {"type":"text","message":f"{CONFIG['name']} is open from {CONFIG['opening_hour']}:00 to {CONFIG['closing_hour']}:00."}
    if any(k in text for k in ["location", "where is canteen", "where's canteen"]):
        return {"type":"text","message":f"We're at {CONFIG['location']}."}
    if "menu" in text or "today" in text:
        names = ", ".join(x["name"] for x in menu[:6])
        return {"type":"text","message":f"Today's menu: {names}."}
    if any(k in text for k in ["price", "cost", "how much"]):
        item_match = next((x for x in menu if x["name"].lower() in text or any(w in text for w in x["name"].lower().split() if len(w)>3)), None)
        if item_match:
            return {"type":"text","message":f"{item_match['name']} is ₹{item_match['price']} today."}
        return {"type":"text","message":"Tell me the item name and I’ll check its live menu price."}
    budget = parse_budget(text)
    if budget and any(k in text for k in ["budget","have","under","spend","₹","rs","inr"]):
        hint = next((c for c in ["breakfast","lunch","snacks","snack"] if c in text), None)
        data = combos(menu, budget, hint)
        return {"type":"combos","budget":budget,"combos":data,
                "message":f"I found {len(data)} combo option(s) under ₹{budget}."}
    return {"type":"text","message":"I can help with today's menu, prices, timings, location, budget combos, recommendations, or order status. Try “I have ₹100” or “surprise me”."}

@app.after_request
def cors(resp):
    origin = request.headers.get("Origin", "")
    if origin in {"http://localhost:8000", "http://127.0.0.1:8000"}:
        resp.headers["Access-Control-Allow-Origin"] = origin
    resp.headers["Vary"] = "Origin"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    resp.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return resp

@app.get("/health")
def health():
    return jsonify(status="ok")

@app.get("/status")
def status():
    hour = now().hour
    return jsonify(open=(CONFIG["opening_hour"] <= hour < CONFIG["closing_hour"]),
                   opening_hour=CONFIG["opening_hour"], closing_hour=CONFIG["closing_hour"],
                   location=CONFIG["location"], name=CONFIG["name"])

@app.get("/menu")
def menu():
    day = request.args.get("day", current_day())
    if day not in MENU: return jsonify(error="Invalid day"), 400
    return jsonify(day=day, items=[public_item(x) for x in MENU[day]])

@app.get("/menu/<day>")
def menu_day(day):
    if day not in MENU: return jsonify(error="Invalid day"), 404
    return jsonify(day=day, items=[public_item(x) for x in MENU[day]])

@app.post("/order")
def order():
    global NEXT_BILL_ID
    if not rate_ok(): return jsonify(error="Too many requests. Please wait a moment."), 429
    data = request.get_json(silent=True) or {}
    raw = data.get("items")
    if not isinstance(raw, list) or not raw:
        return jsonify(error="Your cart is empty."), 400
    normalized, seen = [], set()
    for row in raw:
        try:
            item_id, qty = int(row["item_id"]), int(row["quantity"])
        except Exception:
            return jsonify(error="Invalid cart item."), 400
        if qty <= 0 or qty > 20: return jsonify(error="Quantity must be between 1 and 20."), 400
        if item_id in seen: return jsonify(error="Duplicate item in cart."), 400
        seen.add(item_id)
        item = find_item(item_id)
        if not item: return jsonify(error=f"Item #{item_id} is not on today's menu."), 400
        if not item["available"]: return jsonify(error=f"{item['name']} is sold out today."), 400
        variant = str(row.get("variant", "full"))
        variants = {v["id"]: v for v in public_item(item)["variants"]}
        if variant not in variants: return jsonify(error="Invalid portion size."), 400
        addon_rows = row.get("addons", []) or []
        addon_total = 0; addon_out=[]
        for aid in addon_rows:
            if aid not in ADDONS: return jsonify(error="Invalid add-on."), 400
            addon_out.append(aid); addon_total += ADDONS[aid]["price"]
        unit_price = variants[variant]["price"] + addon_total
        normalized.append({"item_id":item["id"],"dish_id":dish_id(item),"name":item["name"],"quantity":qty,"price":unit_price,"variant":variant,"addons":addon_out})
    subtotal, tax, total = calculate_bill(normalized)
    with BILL_LOCK:
        bid = NEXT_BILL_ID; NEXT_BILL_ID += 1
    placed = now().isoformat(timespec="seconds")
    eta = eta_for(normalized)
    queue_position = 1 + sum(1 for b in BILLS.values() if b["status"] in ("received", "preparing"))
    bill = {"bill_id":bid,"items":normalized,"subtotal":subtotal,"tax":tax,"total":total,
            "status":"received","placed_at":placed,"ready_eta_minutes":eta,"queue_position":queue_position,
            "note":str(data.get("note","")).strip()[:300],"feedback":None}
    BILLS[bid] = bill; ORDERS[bid] = bill
    for row in normalized:
        item = find_item(row["item_id"])
        item["sold_count"] += row["quantity"]
    return jsonify(bill=bill), 201

@app.get("/bill/<int:bill_id>")
def bill(bill_id):
    b = BILLS.get(bill_id)
    if not b: return jsonify(error="Bill not found."), 404
    update_lifecycle(b)
    return jsonify(bill=b)

@app.get("/order/<int:bill_id>/status")
def order_status(bill_id):
    b = BILLS.get(bill_id)
    if not b: return jsonify(error="Bill not found."), 404
    update_lifecycle(b)
    elapsed = int((now()-datetime.fromisoformat(b["placed_at"])).total_seconds()/60)
    return jsonify(status=b["status"], ready_eta_minutes=max(0, b["ready_eta_minutes"]-elapsed))

@app.post("/order/<int:bill_id>/cancel")
def cancel(bill_id):
    if not rate_ok(): return jsonify(error="Too many requests. Please wait a moment."), 429
    b = BILLS.get(bill_id)
    if not b: return jsonify(error="Bill not found."), 404
    update_lifecycle(b)
    elapsed = (now()-datetime.fromisoformat(b["placed_at"])).total_seconds()/60
    if b["status"] != "received" or elapsed > CONFIG["cancellation_grace_minutes"]:
        return jsonify(error="Order is already being prepared and can no longer be cancelled."), 409
    b["status"] = "cancelled"
    for row in b["items"]:
        item = find_item(row["item_id"])
        if item: item["sold_count"] = max(0, item["sold_count"] - row["quantity"])
    return jsonify(bill=b)

@app.post("/order/<int:bill_id>/feedback")
def feedback(bill_id):
    if not rate_ok(): return jsonify(error="Too many requests. Please wait a moment."), 429
    b = BILLS.get(bill_id)
    if not b: return jsonify(error="Bill not found."), 404
    update_lifecycle(b)
    data = request.get_json(silent=True) or {}
    rating = data.get("rating")
    if rating not in ("up","down"): return jsonify(error="Rating must be up or down."), 400
    if b["status"] not in ("ready","completed"): return jsonify(error="Feedback is available after the order is ready."), 409
    if b["feedback"] is not None:
        return jsonify(error="You already rated this order."), 409
    b["feedback"] = rating; FEEDBACK[rating] += 1
    return jsonify(feedback=b["feedback"])


@app.post("/order/<int:bill_id>/complete")
def complete_order(bill_id):
    if not rate_ok(): return jsonify(error="Too many requests. Please wait a moment."), 429
    b = BILLS.get(bill_id)
    if not b: return jsonify(error="Bill not found."), 404
    update_lifecycle(b)
    if b["status"] != "ready": return jsonify(error="Order must be ready before pickup."), 409
    b["status"] = "completed"
    return jsonify(bill=b)

@app.get("/admin/summary")
def admin_summary():
    for b in BILLS.values(): update_lifecycle(b)
    active = [b for b in BILLS.values() if b["status"] != "cancelled"]
    top = sorted(((x["name"], x["sold_count"]) for x in MENU[current_day()]), key=lambda z:-z[1])[:5]
    return jsonify(date=now().date().isoformat(), orders=len(active), revenue=round(sum(b["total"] for b in active),2), top_selling=[{"name":n,"sold":q} for n,q in top], feedback=FEEDBACK)

@app.post("/chat")
def chat():
    if not rate_ok(): return jsonify(error="Too many messages. Please wait a moment."), 429
    data = request.get_json(silent=True) or {}
    return jsonify(chatbot(str(data.get("message",""))))

@app.post("/combos")
def combo_api():
    data = request.get_json(silent=True) or {}
    try: budget = int(data.get("budget", 0))
    except Exception: budget = 0
    if budget < 1: return jsonify(error="Enter a valid budget."), 400
    hint = str(data.get("category_hint","")).strip() or None
    return jsonify(budget=budget, combos=combos(MENU[current_day()], budget, hint))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
