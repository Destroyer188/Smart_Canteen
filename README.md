# Campus Bites — Smart Canteen

Campus Bites is a web-based smart campus canteen ordering application built with **Python Flask, HTML, CSS, and JavaScript**.

The project uses two Python files:

- `canteen_server.py` — backend API, menu data, ordering logic, chatbot, combos, bills, and order status.
- `website.py` — frontend web application served through Flask.

> This README describes only the functionality present in these two project files.

---

## Features

### 🍽️ Menu

The application provides a weekday-based canteen menu for:

- Monday
- Tuesday
- Wednesday
- Thursday
- Friday
- Saturday

Each food item contains information such as:

- Name
- Price
- Category
- Description
- Food image
- Vegetarian/non-vegetarian status
- Spice level
- Allergens
- Preparation time
- Popularity
- Availability

The menu can be filtered by:

- Category
- Vegetarian items
- Favorites

There is also a search box for searching dishes, categories, and descriptions.

---

## 🛒 Shopping Cart

Users can add food items to a cart and modify quantities.

The cart supports:

- Full/Half portion selection
- Add-ons
- Quantity controls
- Order notes
- Cart item count
- Cart total
- Removing items
- Adding multiple favorite items
- Reordering items from previous bills

Available add-ons include:

- Extra cheese
- No onion
- Extra spicy

The backend validates:

- Item IDs
- Quantities
- Availability
- Portion variants
- Add-ons

---

## 📦 Ordering

Users can place an order directly from the cart.

When an order is placed, the backend creates a bill containing:

- Bill ID
- Ordered items
- Quantity
- Selected variant
- Add-ons
- Subtotal
- Tax
- Total
- Order status
- Estimated preparation time
- Queue position
- Optional customer note

The default order flow is:

```text
Received → Preparing → Ready → Completed
```

Orders can also be cancelled during the configured cancellation grace period.

---

## 🧾 Bill & Order Tracking

Every order receives a bill number.

The frontend provides a bill view containing:

- Bill number
- Order status
- Progress tracker
- Estimated waiting time
- Queue position
- Ordered items
- Subtotal
- Tax
- Total
- Customer note
- QR code
- Bill splitting calculation
- Print option
- Reorder option
- Cancel option
- Pickup completion option

Bills can also be opened directly using:

```text
http://localhost:8000/bill/<bill_id>
```

The QR code generated on the bill points to the corresponding bill page.

---

## ⏱️ Order Status & Queue

The backend calculates an estimated waiting time based on:

- Food preparation time
- Current queue
- Queue configuration

Orders move through their lifecycle automatically based on elapsed time.

The customer interface periodically checks the bill so that the displayed order status can update.

A ready-order indicator is also displayed on the main page while an active order is being tracked.

---

## 💰 Combo Builder

Users can build food combinations based on a budget.

The combo builder allows users to:

- Choose a budget from ₹50 to ₹200
- Select a meal/category hint
- Find combinations within the selected budget

Supported hints include:

- Any meal
- Breakfast
- Lunch
- Snack

The backend generates combinations using available menu items and returns their prices.

The user can add a generated combo to the cart.

---

## 🤖 Canteen Assistant

Campus Bites includes a built-in rule-based chatbot.

The assistant can answer questions about:

- Today's menu
- Food prices
- Canteen timings
- Canteen location
- Budget-based combos
- Food recommendations
- Order/bill status

Example queries:

```text
What is on today?
```

```text
How much is the Masala Chai?
```

```text
I have ₹100
```

```text
What are the timings?
```

```text
Where is the canteen?
```

```text
Where is order 1004?
```

```text
Surprise me
```

The chatbot uses the current day's menu when providing menu-related information.

---

## 🎤 Voice Input

The chatbot supports browser speech recognition when the browser provides:

```text
SpeechRecognition
```

or:

```text
webkitSpeechRecognition
```

The recognition language changes between:

- English (`en-IN`)
- Hindi (`hi-IN`)

based on the selected interface language.

---

## ❤️ Favorites

Users can mark dishes as favorites.

Favorites are stored in the browser's `localStorage`.

Features include:

- Favorite/unfavorite dishes
- Favorites filter
- Add all available favorites to the cart

---

## 🔄 Reorder

Previous orders are stored locally in the browser.

The history section shows previous bill IDs and dates.

Users can select:

```text
View / Reorder
```

to open a previous bill and add its available items back to the current cart.

---

## 🌱 Vegetarian Filter

The menu provides a vegetarian-only filter.

Food cards also indicate:

```text
🌱 Veg
```

or:

```text
🍗 Non-veg
```

The current menu data contains one non-vegetarian item:

```text
Chicken Biryani
```

on Friday.

---

## 🌶️ Spice Level

Each food item has a spice-level indicator.

The interface displays:

- No spice
- Mild
- Medium
- Spicy

This information comes from the menu data in the backend.

---

## ⚠️ Allergen Information

Menu items contain allergen information such as:

- Dairy
- Gluten
- Peanuts
- Soy

The current frontend data model includes these allergens, although the current card UI primarily displays the item's dietary/spice/preparation information rather than rendering a separate allergen badge.

---

## 🌙 Dark Mode

The frontend includes a dark theme.

Users can switch between the normal and dark appearance using the theme button.

The selected dark-mode state is saved in:

```text
localStorage
```

so it can be restored when the page is loaded again.

---

## 🌐 Language Toggle

The interface contains an English/Hindi toggle.

Currently, the implemented translations cover the main:

- Menu heading
- Combo builder heading

and the voice-recognition language changes accordingly.

The full interface is not translated.

---

## 📱 Responsive Design

The frontend is designed to adapt to different screen sizes.

It includes responsive layouts for:

- Desktop
- Tablet
- Mobile

Food cards change from three columns to two and eventually one column on smaller screens.

---

## 🔔 Sold-Out Notifications

When an item is unavailable, the interface provides:

```text
🔔 Notify me
```

Users can request a notification for that dish.

The notification preference is stored in:

```text
localStorage
```

under:

```text
soldoutNotify
```

---

## 💬 Toast Notifications

The frontend uses temporary toast messages for actions such as:

- Adding items
- Cancelling orders
- Placing orders
- Changing language
- Adding favorites
- Setting sold-out notifications
- Feedback

---

## 👍 / 👎 Order Feedback

Once an order reaches:

```text
Ready
```

or:

```text
Completed
```

the customer can submit:

- 👍
- 👎

feedback.

The backend prevents the same bill from being rated more than once.

---

## 📊 Admin Summary API

The backend exposes:

```text
GET /admin/summary
```

The endpoint returns information including:

- Current date
- Number of active/non-cancelled orders
- Revenue
- Top-selling items
- Feedback totals

The current implementation does not include authentication for this endpoint.

---

## 🔐 Rate Limiting

The backend includes a basic IP-based rate limiter.

It limits repeated requests to protect endpoints such as:

- Orders
- Cancellation
- Feedback
- Chatbot

The rate-limit configuration is defined in `CONFIG`.

---

## 🌐 CORS

The backend adds CORS headers for the two local frontend origins:

```text
http://localhost:8000
http://127.0.0.1:8000
```

This allows the frontend running on port `8000` to communicate with the backend running on port `5000`.

---

# Project Structure

The project consists of two Python files:

```text
canteen_final/
│
├── canteen_server.py
└── website.py
```

---

# How the Application Works

The project runs two Flask servers.

```text
                Browser
                   │
                   ▼
          website.py :8000
                   │
                   │ HTTP requests
                   ▼
        canteen_server.py :5000
                   │
                   ▼
             Menu / Orders
             Bills / Chatbot
             Combos / Status
```

### `website.py`

Responsible for:

- Frontend HTML
- CSS
- JavaScript
- Menu display
- Search/filter UI
- Cart UI
- Bill UI
- Chat interface
- Theme switching
- Language toggle
- Local browser storage
- QR-code display
- Frontend Flask routes

### `canteen_server.py`

Responsible for:

- Menu data
- Menu API
- Canteen status
- Order validation
- Bill creation
- Pricing
- Variants
- Add-ons
- Queue calculations
- Order lifecycle
- Cancellation
- Feedback
- Combo generation
- Chatbot
- Rate limiting
- Admin summary

---

# Requirements

You need:

- Python 3.x
- VS Code or another Python IDE
- A modern web browser
- Internet access for the external food images and QRCode JavaScript library used by the frontend

The application does not require a separate database server.

The current backend stores its application state in Python memory.

---

# Setup in VS Code

## 1. Open the project

Open the folder containing:

```text
canteen_server.py
website.py
```

in VS Code.

---

## 2. Open the VS Code terminal

Use:

```text
Ctrl + `
```

---

## 3. Create a virtual environment

```powershell
python -m venv .venv
```

---

## 4. Activate the virtual environment

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

If activation is blocked by PowerShell:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate again:

```powershell
.\.venv\Scripts\Activate.ps1
```

You should see:

```text
(.venv)
```

in the terminal.

---

## 5. Install Flask

The two provided files directly require Flask.

Install it with:

```powershell
python -m pip install flask
```

The frontend also loads QRCode.js from a CDN in the browser.

---

# Running the Application

The application uses two servers.

## Terminal 1 — Backend

Run:

```powershell
python canteen_server.py
```

The backend runs on:

```text
http://127.0.0.1:5000
```

Keep this terminal open.

---

## Terminal 2 — Website

Open a second VS Code terminal.

Activate the environment again if required:

```powershell
.\.venv\Scripts\Activate.ps1
```

Then run:

```powershell
python website.py
```

The website runs on:

```text
http://127.0.0.1:8000
```

Open:

```text
http://localhost:8000
```

in your browser.

---

# Important URLs

| Purpose | URL |
|---|---|
| Main website | `http://localhost:8000` |
| Bill page | `http://localhost:8000/bill/<bill_id>` |
| Backend health | `http://localhost:5000/health` |
| Canteen status | `http://localhost:5000/status` |
| Menu | `http://localhost:5000/menu` |
| Specific day's menu | `http://localhost:5000/menu/<day>` |
| Bill API | `http://localhost:5000/bill/<bill_id>` |
| Order status | `http://localhost:5000/order/<bill_id>/status` |
| Admin summary | `http://localhost:5000/admin/summary` |

---

# Main API Endpoints

### Menu

```http
GET /menu
GET /menu/<day>
```

### Canteen status

```http
GET /status
```

### Health check

```http
GET /health
```

### Create order

```http
POST /order
```

### View bill

```http
GET /bill/<bill_id>
```

### Order status

```http
GET /order/<bill_id>/status
```

### Cancel order

```http
POST /order/<bill_id>/cancel
```

### Complete pickup

```http
POST /order/<bill_id>/complete
```

### Feedback

```http
POST /order/<bill_id>/feedback
```

### Chatbot

```http
POST /chat
```

### Combos

```http
POST /combos
```

### Admin summary

```http
GET /admin/summary
```

---

# Configuration

The main backend configuration is stored in the `CONFIG` dictionary inside `canteen_server.py`.

Current settings include:

```text
Name: Campus Bites
Location: Main Academic Block, Campus
Opening hour: 08:00
Closing hour: 20:00
Tax rate: 0%
Currency: ₹
Cancellation grace period: 2 minutes
Base queue time: 2 minutes
Queue time per order: 3 minutes
Rate limit window: 60 seconds
Rate limit maximum: 20 requests
```

These values can be changed directly in `canteen_server.py`.

---

# Browser Storage

The frontend uses `localStorage` for client-side information including:

```text
canteenCart
favorites
dark
lang
soldoutNotify
activeBill
lastBill
pastOrders
```

This means cart, favorites, language/theme preferences, and order history are stored in the browser rather than in a database.

---

# PWA Support

The frontend includes:

```text
/manifest.webmanifest
```

and:

```text
/sw.js
```

The service worker currently provides basic installation/activation hooks, while the manifest contains the application metadata.

The current manifest does not define application icons and the service worker does not implement an offline cache.

---

# Limitations of the Current Version

The following are characteristics of the provided implementation:

- Application data is stored in memory and is lost when the backend process restarts.
- `flask-cors` is not required; CORS headers are implemented directly.
- The admin summary endpoint currently has no authentication.
- The language toggle only translates selected headings rather than the entire interface.
- The frontend uses periodic bill polling rather than Server-Sent Events.
- There is no separate kitchen/staff dashboard.
- There is no SQLite persistence.
- There is no real payment integration.
- There is no user account/login system.
- There is no persistent inventory system.
- The PWA service worker does not provide an offline cache.
- The manifest currently contains no icons.
- Food images are loaded from external Unsplash URLs.
- The chatbot is rule-based rather than powered by an external LLM.
- The current frontend directly uses the backend's menu item IDs when constructing cart entries.

These limitations reflect the functionality present in the two provided Python files.

---

# Technologies Used

- **Python**
- **Flask**
- **HTML5**
- **CSS3**
- **JavaScript**
- **Browser Local Storage**
- **QRCode.js**
- **Unsplash image URLs**

---

# GitHub Repository Description

### Recommended description

> Smart campus canteen web application built with Python Flask and JavaScript, featuring weekday menus, smart cart, food variants and add-ons, combo recommendations, chatbot assistance, order tracking, bills, favorites, feedback, and responsive dark-mode UI.

### Short description

> Smart campus canteen ordering app built with Flask and JavaScript, featuring menus, cart, combos, chatbot, order tracking, bills, favorites and feedback.

---

# Suggested GitHub Topics

```text
python
flask
javascript
html
css
canteen
food-ordering
campus-app
smart-canteen
chatbot
web-app
```
