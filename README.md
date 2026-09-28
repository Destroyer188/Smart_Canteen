# Campus Bites — AI Smart Canteen

A modern campus canteen ordering system built with **Python, Flask, SQLite, HTML, CSS, and vanilla JavaScript**.

Campus Bites separates the application into a backend API and a frontend web server. The backend is the source of truth for menus, prices, cart quotes, orders, bills, inventory, payments, recommendations, and order lifecycle state.

## Features

### 🍽️ Menu & Food Discovery
- Today's menu with weekday-based menus.
- Browse menus for other days without accidentally ordering from a past/future day.
- Search and category filtering.
- Veg / non-veg information.
- Spice-level indicators.
- Allergen information on food cards.
- Nutrition/calorie information.
- Healthy-pick filtering.
- Sold-out state driven by inventory.
- Item-specific food images with fallback handling.
- Popular/recommended dishes based on sales, ratings, and menu metadata.

### 🛒 Smart Cart
- Add, remove, and update quantities.
- Portion variants such as half/full where supported.
- Paid and free add-ons/customizations.
- Multiple lines for the same dish when the variant/add-ons differ.
- Server-side `/cart/quote` endpoint.
- The browser never decides the final price.
- Coupon/discount support.
- Tax calculation performed by the backend.
- Order notes with server-side sanitization.
- Cart validation and quantity limits.

### 📦 Ordering & Pickup
- Server-authoritative order validation.
- Canteen opening-hours enforcement.
- Time-slot pre-ordering.
- Per-slot capacity limits.
- Unique order/token number such as `Token A-27`.
- Pickup PIN to prevent incorrect collection.
- Cancellation grace period.
- Order completion/pickup flow.
- Automatic lifecycle: `Received → Preparing → Ready → Completed`.
- Uncollected ready orders can automatically expire.

### ⚡ Live Order Tracking
- Server-Sent Events (SSE) for live bill/order updates.
- Automatic polling fallback if SSE is unavailable.
- Live queue position.
- Estimated preparation time.
- Customer UI reflects kitchen status changes without manually refreshing.

### 👨‍🍳 Kitchen Dashboard
Open `http://localhost:8000/kitchen`.

- Token-protected kitchen access.
- Live order queue.
- Change order status.
- Mark items sold out / back in stock.
- Adjust preparation times.
- Live queue updates.
- Inventory-aware ordering.

### 🧾 Bills & Payments
- Persistent SQLite bills.
- Direct bill URLs: `http://localhost:8000/bill/<bill-id>`.
- Printable bill/receipt.
- QR code for bill access.
- UPI deep-link/QR generation.
- Pay-at-counter option.
- Paid/unpaid payment state.
- Demo wallet/prepaid balance.
- Coupon discounts.
- Loyalty points.

> UPI/payment functionality is intentionally a local/demo abstraction. It does not connect to a real bank or payment provider.

### ❤️ Favorites, History & Reorder
- Favorites saved to the user's account/profile.
- Order history.
- Reorder previous purchases.
- Stable dish identifiers across weekday menus.

### 👤 User Identity
- Campus ID / phone-style login flow.
- Mock OTP for local development.
- User profile.
- Dietary preferences.
- Allergen exclusions.
- Favorites and order history synced through the backend.

### 🥗 Dietary & Nutrition
Supported dietary filtering/profile options include:
- Vegetarian
- Vegan
- Jain

Users can also configure allergen exclusions. Dish cards can display nutrition/calorie information and support a healthy-pick filter.

### ⭐ Ratings & Reviews
- Quick order feedback.
- Per-dish ratings and short reviews.
- Duplicate feedback is rejected.
- Review data is persisted in SQLite.

### 🤖 AI Canteen Assistant
The built-in rule-based assistant can handle:
- Menu questions.
- Dish prices.
- Canteen timings.
- Canteen location.
- Order/bill status.
- Budget-based food recommendations.
- Combo recommendations.
- Surprise-me recommendations.
- Dietary/allergen-aware recommendations.

It also supports Hindi responses for supported UI/chat flows and voice input through the browser Speech Recognition API.

The chatbot is deliberately implemented without paid AI APIs.

### 🎁 Combos & Recommendations
- Budget-based combo generation.
- Category hints.
- Pair/triple combinations.
- Server-side price validation.
- Recommendation ranking based on availability, popularity, ratings, dietary constraints, and time of day.

### 👥 Group Ordering
- Create a shared group order.
- Share a group link.
- Multiple people can add items to the shared cart.
- Server validates the resulting order.

### 🔔 Notifications & PWA
- Browser notification when an active order becomes ready, when permission is granted.
- Sold-out notification hooks for inventory changes.
- Installable PWA shell.
- 192×192 and 512×512 icons.
- Offline app-shell cache.

> The offline cache covers the application shell only. Ordering, account, inventory, payments, and other API operations still require the backend.

### 📊 Admin & Analytics
Admin endpoints provide:
- Order/revenue summaries.
- Peak-hour analytics.
- Best-selling dishes.
- Prep-time information.
- Inventory information.
- CSV analytics export.

Admin/kitchen APIs are protected using `X-Admin-Token`.

### 🔐 Reliability & Security Basics
- Server-authoritative pricing.
- Server-side cart validation.
- Endpoint-specific rate limiting.
- Rate-limit memory cleanup.
- Configurable CORS origins.
- Sanitized order notes.
- Escaped customer-visible receipt content.
- Admin token authentication.
- SQLite persistence.
- Automatic database schema initialization/migrations.
- Graceful backend-offline UI.
- Responsive/mobile-friendly interface.
- Keyboard navigation and visible focus states.
- Reduced-motion support.

## Project Architecture

```text
                  Browser
                     │
                     ▼
             website.py :8000
          Frontend / presentation
                     │
              HTTP API + SSE
                     │
                     ▼
          canteen_server.py :5000
              Backend / business logic
                     │
                     ▼
                SQLite DB
```

### `canteen_server.py`
Responsible for menu data, inventory, pricing, cart quotes, order validation, bills, discounts, payments, user/profile data, favorites, reviews, lifecycle state, queue calculations, chatbot logic, combos, SSE, kitchen/admin APIs, and SQLite persistence.

### `website.py`
Responsible for serving the frontend, main application shell, direct bill URLs, group URLs, kitchen dashboard page, and PWA manifest. Frontend JavaScript communicates with the backend API; it does not become the source of truth for prices or order validation.

## Requirements

- Windows, macOS, or Linux
- Python 3.10+
- VS Code recommended
- Modern browser such as Chrome, Edge, or Firefox
- No paid services required

## Installation — VS Code

### 1. Open the project

Extract the project and open the folder in VS Code. It should contain:

```text
canteen_final/
├── canteen_server.py
├── website.py
├── requirements.txt
├── README.md
├── templates/
│   ├── index.html
│   └── kitchen.html
├── static/
│   ├── app.js
│   ├── style.css
│   ├── sw.js
│   ├── manifest.webmanifest
│   └── icons/
│       ├── icon-192.png
│       ├── icon-512.png
│       └── icon.svg
└── tests/
    ├── test_canteen.py
    └── test_playwright.py
```

### 2. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate again.

### 3. Select the VS Code interpreter

`Ctrl + Shift + P` → `Python: Select Interpreter` → choose `.venv\Scripts\python.exe`.

### 4. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

**Flask-CORS is not required.** CORS is implemented directly in `canteen_server.py`.

## Running the Application

Use two terminals.

### Terminal 1 — Backend

```powershell
.\.venv\Scripts\Activate.ps1
$env:ADMIN_TOKEN="admin123"
$env:ALLOWED_ORIGINS="http://localhost:8000,http://127.0.0.1:8000"
$env:DB_PATH="canteen.db"
$env:FRONTEND_BASE_URL="http://localhost:8000"
$env:MOCK_OTP="1"
python canteen_server.py
```

Backend: `http://localhost:5000`

### Terminal 2 — Frontend

```powershell
.\.venv\Scripts\Activate.ps1
$env:ADMIN_TOKEN="admin123"
$env:ALLOWED_ORIGINS="http://localhost:8000,http://127.0.0.1:8000"
$env:DB_PATH="canteen.db"
$env:FRONTEND_BASE_URL="http://localhost:8000"
$env:MOCK_OTP="1"
python website.py
```

Frontend: `http://localhost:8000`

Open `http://localhost:8000` in the browser.

## Useful URLs

| Page | URL |
|---|---|
| Main application | `http://localhost:8000` |
| Kitchen dashboard | `http://localhost:8000/kitchen` |
| Direct bill | `http://localhost:8000/bill/<bill-id>` |
| Group order | `http://localhost:8000/group/<group-id>` |
| Backend health | `http://localhost:5000/health` |
| Backend menu | `http://localhost:5000/menu` |
| Backend status | `http://localhost:5000/status` |

## Environment Variables

| Variable | Default | Purpose |
|---|---|---|
| `ADMIN_TOKEN` | empty | Token required for kitchen/admin endpoints |
| `ALLOWED_ORIGINS` | `http://localhost:8000,http://127.0.0.1:8000` | Allowed frontend origins |
| `DB_PATH` | `canteen.db` | SQLite database path |
| `FRONTEND_BASE_URL` | `http://localhost:8000` | Base URL used in bill QR codes |
| `MOCK_OTP` | `1` | Enables the local/mock OTP flow |

## Database

SQLite stores users, orders, bills, order items, feedback, dish reviews, favorites, inventory, daily sales, payments, wallet balances, groups, and coupons. The schema is initialized/migrated automatically when the backend starts.

To reset local data, stop the backend and delete `canteen.db`, then start the backend again.

## Testing

API tests:

```powershell
pytest -q tests/test_canteen.py
```

Optional Playwright browser smoke test:

```powershell
python -m pip install playwright
python -m playwright install chromium
$env:RUN_PLAYWRIGHT="1"
pytest -q tests/test_playwright.py
```

The browser smoke test expects both servers to already be running.

## Troubleshooting

### `ModuleNotFoundError`

Make sure `(.venv)` appears in the terminal, then run:

```powershell
python -m pip install -r requirements.txt
```

### Backend offline

Check that both servers are running and test:

```text
http://localhost:5000/health
```

### CORS errors

Start the backend with:

```powershell
$env:ALLOWED_ORIGINS="http://localhost:8000,http://127.0.0.1:8000"
```

Then restart it.

### Port already in use

```powershell
netstat -ano | findstr :5000
netstat -ano | findstr :8000
```

Then stop the relevant PID with:

```powershell
taskkill /PID <PID> /F
```

## Current Limitations

1. OTP is mocked when `MOCK_OTP=1`; no real SMS provider is connected.
2. UPI/payment confirmation is a local demo abstraction, not a real payment gateway.
3. Browser-ready notifications use the Notification API rather than a VAPID/Web Push service.
4. Pre-order slots are for the current operating day.
5. Kitchen prep-time overrides are process-local rather than persisted as permanent configuration.
6. The chatbot is rule-based and does not use an external LLM or paid AI API.

## Future / P3 Architecture

Possible future extensions include multi-canteen support, role-based staff permissions, refunds and cancellation reasons, allergen-safe kitchen tickets/printer output, full Hindi/Marathi localization, an LLM-backed chatbot with strict tool calling, dark-mode-aware analytics charts, and Docker/Gunicorn single-origin deployment.

These are future design directions, not claims that they are production-ready in this version.

## GitHub

### Suggested repository name

`ai-smart-canteen`

### GitHub repository description

> AI-powered smart campus canteen system built with Flask, SQLite and vanilla JavaScript, featuring server-authoritative ordering, live order tracking, kitchen dashboard, inventory, time-slot pre-orders, chatbot recommendations, payments, favorites, group ordering and analytics.

### Short description

> Smart campus canteen ordering system with Flask, SQLite, live order tracking, inventory, kitchen dashboard, chatbot, payments and analytics.

### Suggested GitHub topics

```text
python
flask
sqlite
javascript
html
css
canteen-management
food-ordering
campus-app
smart-canteen
restaurant-management
sse
pwa
web-development
```

## License

Add the license that matches the project's intended distribution before publishing publicly.
