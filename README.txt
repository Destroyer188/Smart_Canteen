SMART CANTEEN — UPDATED V1

Requirements:
- Python 3.10+
- Flask (`pip install flask`)
- Modern browser

Run:
1. Terminal A: `python canteen_server.py`
2. Terminal B: `python website.py`
3. Open `http://localhost:8000`

Implemented from the bug/feature master prompt:
- Fixed localhost/127.0.0.1 CORS mismatch.
- Real direct `/bill/<id>` receipt URL with live tracking.
- Bill poller cleanup and modal safety.
- Sold-out-safe chatbot recommendation.
- Stable dish IDs for cross-day favorites and reorder.
- Correct item-price chatbot answers and safer budget intent.
- Escaped bill notes to prevent receipt XSS.
- Removed dead keyboard handlers.
- Real `ready` -> `completed` pickup flow.
- Repeat feedback returns a clear 409 response.
- Cross-midnight menu refresh.
- Persistent backend-offline menu state/retry behavior is handled by the UI.
- ETA queue position.
- Rate limits on cancellation, feedback and order/chat endpoints.
- Thread lock around bill IDs.
- QR code on receipts.
- Sold-out “Notify me” reminder using localStorage.
- Admin-lite `/admin/summary`.
- Split-bill calculator.
- Add all favorites.
- Arrow-key budget nudging.
- Chat clear button.
- Portion size variants and server-validated add-ons.
- Persistent active-order ready pill.
- English/Hindi UI toggle.
- PWA manifest + service worker registration.
- Browser voice input for chatbot where supported.

V1 persistence note:
Orders and bills remain in memory and disappear when `canteen_server.py` restarts. SQLite/accounts/payments/push notifications/WebSockets remain V2-style upgrades.

The QR library is loaded from CDN, so internet access is needed for QR rendering and the remote food photos.
