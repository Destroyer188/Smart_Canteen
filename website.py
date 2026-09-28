from flask import Flask, render_template_string

app = Flask(__name__)

HTML = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{{ name }} — Smart Canteen</title><link rel="manifest" href="/manifest.webmanifest"><meta name="theme-color" content="#174d36"><script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>
<style>
:root{--bg:#f8f5ed;--card:#fff;--text:#17251d;--muted:#6c776f;--green:#174d36;--green2:#286b4c;--orange:#e98a2b;--line:#e6e2d8;--shadow:0 18px 45px rgba(23,37,29,.09)}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;font-family:Inter,ui-sans-serif,system-ui,-apple-system,Segoe UI,sans-serif;background:var(--bg);color:var(--text)}button,input,textarea{font:inherit}button{cursor:pointer;border:0}.container{width:min(1180px,92%);margin:auto}
header{position:sticky;top:0;z-index:20;background:rgba(248,245,237,.88);backdrop-filter:blur(16px);border-bottom:1px solid var(--line)}
.nav{height:72px;display:flex;align-items:center;justify-content:space-between}.brand{font-weight:900;font-size:21px;display:flex;gap:10px;align-items:center}.logo{width:38px;height:38px;border-radius:12px;background:var(--green);color:white;display:grid;place-items:center}
.navlinks{display:flex;gap:8px}.navlinks button,.iconbtn{background:transparent;padding:10px 13px;border-radius:12px;color:var(--text)}.navlinks button:hover,.iconbtn:hover{background:#ece9df}
.hero{padding:62px 0 35px;display:grid;grid-template-columns:1.15fr .85fr;gap:40px;align-items:center}.eyebrow{color:var(--orange);font-weight:800;letter-spacing:.08em;text-transform:uppercase;font-size:12px}.hero h1{font-size:clamp(42px,6vw,76px);line-height:.95;margin:12px 0 20px;letter-spacing:-.055em}.hero p{font-size:18px;color:var(--muted);max-width:620px;line-height:1.7}.actions{display:flex;gap:12px;flex-wrap:wrap;margin-top:25px}.primary,.secondary{padding:13px 18px;border-radius:14px;font-weight:800}.primary{background:var(--green);color:white}.primary:hover{background:var(--green2);transform:translateY(-1px)}.secondary{background:#fff;border:1px solid var(--line)}
.hero-card{background:linear-gradient(145deg,#214e3b,#102d20);color:#fff;border-radius:30px;padding:28px;min-height:330px;box-shadow:var(--shadow);position:relative;overflow:hidden}.hero-card:after{content:"";position:absolute;width:230px;height:230px;border-radius:50%;right:-60px;bottom:-70px;background:rgba(233,138,43,.28)}.hero-card h3{font-size:28px;margin:10px 0}.status{display:inline-flex;align-items:center;gap:8px;background:rgba(255,255,255,.1);padding:9px 12px;border-radius:99px}.dot{width:9px;height:9px;border-radius:50%;background:#6ee7a3}.section{padding:28px 0 55px}.section-head{display:flex;align-items:end;justify-content:space-between;gap:15px;margin-bottom:18px}.section h2{font-size:32px;margin:0;letter-spacing:-.03em}.muted{color:var(--muted)}
.tabs,.filters{display:flex;gap:8px;overflow:auto;padding:5px 0 14px}.pill{white-space:nowrap;padding:10px 14px;border-radius:999px;background:#fff;border:1px solid var(--line);font-weight:700}.pill.active{background:var(--green);color:white;border-color:var(--green)}
.search{display:flex;gap:10px;margin:8px 0 20px}.search input,.chatinput input,.note{width:100%;border:1px solid var(--line);background:#fff;border-radius:14px;padding:13px 15px;outline:none}.search input:focus,.chatinput input:focus,.note:focus{border-color:var(--green)}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}.card{background:var(--card);border:1px solid var(--line);border-radius:22px;overflow:hidden;box-shadow:0 5px 20px rgba(23,37,29,.04);transition:.22s}.card:hover{transform:translateY(-4px);box-shadow:var(--shadow)}.foodimg{height:190px;background-size:cover;background-position:center;position:relative}.badge{position:absolute;left:12px;top:12px;background:#fff;padding:7px 9px;border-radius:10px;font-size:11px;font-weight:900}.fav{position:absolute;right:12px;top:12px;width:38px;height:38px;border-radius:50%;background:rgba(255,255,255,.9);font-size:18px}.fav.on{color:#df4b57}.cardbody{padding:17px}.cardtop{display:flex;justify-content:space-between;gap:12px}.card h3{margin:0;font-size:18px}.price{font-weight:900}.desc{font-size:13px;line-height:1.5;color:var(--muted);margin:8px 0 12px}.meta{display:flex;gap:7px;flex-wrap:wrap;margin-bottom:14px}.tag{font-size:11px;padding:5px 8px;border-radius:8px;background:#f1f2ec}.add{width:100%;padding:11px;border-radius:12px;background:var(--green);color:#fff;font-weight:850}.add:disabled{background:#bbb;cursor:not-allowed}
.builder{background:#173e2d;color:#fff;border-radius:26px;padding:25px;margin-top:15px}.builderrow{display:flex;gap:15px;align-items:center;flex-wrap:wrap}.range{flex:1;min-width:220px}.range input{width:100%}.budget{font-size:34px;font-weight:900;min-width:100px}
.floating{position:fixed;right:22px;bottom:22px;z-index:30;display:flex;gap:10px}.floatbtn{height:58px;padding:0 18px;border-radius:18px;background:var(--green);color:#fff;box-shadow:0 15px 35px rgba(23,77,54,.28);font-weight:900}.cartcount{background:var(--orange);padding:2px 7px;border-radius:99px;margin-left:5px}
.drawer{position:fixed;inset:0;z-index:50;pointer-events:none}.drawer.open{pointer-events:auto}.shade{position:absolute;inset:0;background:rgba(0,0,0,.4);opacity:0;transition:.2s}.drawer.open .shade{opacity:1}.panel{position:absolute;right:0;top:0;height:100%;width:min(460px,94%);background:#fff;padding:24px;transform:translateX(100%);transition:.25s;overflow:auto}.drawer.open .panel{transform:translateX(0)}.panelhead{display:flex;justify-content:space-between;align-items:center}.cartrow{display:flex;justify-content:space-between;gap:12px;padding:14px 0;border-bottom:1px solid var(--line)}.qty{display:flex;gap:8px;align-items:center}.qty button{width:30px;height:30px;border-radius:9px;background:#eee}.total{display:flex;justify-content:space-between;font-size:22px;font-weight:900;padding:18px 0}
.modal{position:fixed;inset:0;z-index:70;background:rgba(0,0,0,.45);display:none;place-items:center;padding:20px}.modal.show{display:grid}.modalbox{background:#fff;border-radius:24px;padding:25px;width:min(650px,100%);max-height:85vh;overflow:auto}.combo{border:1px solid var(--line);border-radius:16px;padding:15px;margin:10px 0;display:flex;justify-content:space-between;gap:12px}
.chat{position:fixed;right:22px;bottom:92px;width:min(390px,calc(100% - 30px));background:#fff;border:1px solid var(--line);border-radius:22px;box-shadow:var(--shadow);z-index:45;display:none;overflow:hidden}.chat.show{display:block}.chathead{background:var(--green);color:white;padding:16px;font-weight:900}.messages{height:330px;overflow:auto;padding:14px}.msg{padding:10px 12px;border-radius:14px;background:#f0f2ed;margin:7px 0;max-width:88%;font-size:14px}.msg.user{margin-left:auto;background:var(--green);color:white}.quick{display:flex;gap:6px;overflow:auto;padding:8px 12px}.quick button{white-space:nowrap;background:#f0f2ed;border-radius:99px;padding:7px 10px;font-size:12px}.chatinput{display:flex;gap:7px;padding:12px;border-top:1px solid var(--line)}
.billwrap{padding:45px 0}.receipt{background:#fff;border:1px solid var(--line);border-radius:24px;padding:28px;max-width:760px;margin:auto;box-shadow:var(--shadow)}.receipt h1{margin-top:0}.receiptrow{display:flex;justify-content:space-between;padding:10px 0;border-bottom:1px dashed #ddd}.tracker{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:22px 0}.step{padding:13px;border-radius:13px;background:#eee;text-align:center;font-weight:800;font-size:12px}.step.active{background:#d9f0e1;color:#145a3a}.toast{position:fixed;left:50%;bottom:22px;transform:translate(-50%,20px);background:#17251d;color:#fff;padding:12px 16px;border-radius:13px;opacity:0;z-index:100;transition:.25s}.toast.show{opacity:1;transform:translate(-50%,0)}
footer{padding:35px 0;border-top:1px solid var(--line);color:var(--muted)}
.readypill{position:fixed;right:22px;bottom:92px;z-index:29;background:#fff;border:1px solid var(--line);padding:10px 14px;border-radius:14px;box-shadow:var(--shadow);font-weight:800;display:none}.ready-pill-show{display:block}.notify{background:#fff3dd;color:#754b00;padding:9px 12px;border-radius:11px;font-size:12px;margin-top:8px}.dark{--bg:#101612;--card:#172019;--text:#f4f5ef;--muted:#a7b1aa;--line:#29332d}.dark header{background:rgba(16,22,18,.88)}.dark .secondary,.dark .pill,.dark .search input,.dark .chat,.dark .panel,.dark .modalbox,.dark .receipt,.dark .card,.dark .chatinput input{background:#172019;color:var(--text)}.dark .tag,.dark .quick button,.dark .step{background:#253029;color:#ddd}
@media(max-width:850px){.hero{grid-template-columns:1fr}.grid{grid-template-columns:repeat(2,1fr)}}@media(max-width:560px){.navlinks{display:none}.hero{padding-top:38px}.grid{grid-template-columns:1fr}.hero h1{font-size:50px}.tracker{grid-template-columns:1fr}.floating{right:12px;bottom:12px}.floatbtn{height:52px}}
@media(prefers-reduced-motion:reduce){*{scroll-behavior:auto!important;transition:none!important}}
@media print{header,.floating,.chat,.actions,.section:not(#billSection),footer{display:none!important}.receipt{box-shadow:none;border:0}}
</style>
</head>
<body>
<header><div class="container nav">
<div class="brand"><span class="logo">🍴</span>{{ name }}</div>
<div class="navlinks"><button onclick="scrollToId('menu')">Menu</button><button onclick="scrollToId('builder')">Combos</button><button onclick="toggleChat()">Assistant</button><button class="iconbtn" onclick="toggleLang()">हि/EN</button><button class="iconbtn" onclick="toggleTheme()">◐</button></div>
</div></header>

<main>
<section class="container hero">
<div><div class="eyebrow">Smart campus food ordering</div><h1>Good food.<br><span style="color:var(--orange)">Zero queue.</span></h1>
<p>Browse today's canteen menu, build a budget meal, order in seconds, and track your food until it's ready.</p>
<div class="actions"><button class="primary" onclick="scrollToId('menu')">Explore today's menu →</button><button class="secondary" onclick="toggleChat()">Ask the assistant</button></div></div>
<div class="hero-card"><div class="status"><span class="dot" id="statusDot"></span><span id="canteenStatus">Checking...</span></div><h3>What are you craving?</h3><p style="opacity:.75;line-height:1.6">Search the live menu or let the assistant surprise you with something good.</p><div style="margin-top:55px;font-size:12px;opacity:.65" id="location"></div></div>
</section>

<section class="container section" id="menu">
<div class="section-head"><div><div class="eyebrow">Fresh today</div><h2>Today's menu</h2></div><div class="muted" id="dayLabel"></div></div>
<div class="tabs" id="days"></div>
<div class="search"><input id="search" placeholder="Search dishes, categories or descriptions…"><button class="secondary" onclick="clearSearch()">Clear</button></div>
<div class="filters" id="filters"></div>
<div class="grid" id="menuGrid"></div>
</section>

<section class="container section" id="builder">
<div class="section-head"><div><div class="eyebrow">Eat smart</div><h2>Build a meal on your budget</h2></div></div>
<div class="builder"><div class="builderrow"><div class="budget" id="budgetText">₹100</div><div class="range"><input id="budget" type="range" min="50" max="200" step="5" value="100"></div><button class="secondary" onclick="findCombos()">Find my combos</button></div><div class="tabs" style="margin-top:16px"><button class="pill active mealhint" data-hint="">Any meal</button><button class="pill mealhint" data-hint="Breakfast">Breakfast</button><button class="pill mealhint" data-hint="Lunch">Lunch</button><button class="pill mealhint" data-hint="Snacks">Snack</button></div></div>
</section>

<section class="container section">
<div class="section-head"><div><div class="eyebrow">Your shortcuts</div><h2>Favorites & past orders</h2></div></div>
<div class="card" style="padding:20px"><button class="pill" onclick="addAllFavorites()">♥ Add all favorites</button><div id="history">No past orders yet. Your completed bill IDs will appear here.</div></div>
</section>
</main>

<footer><div class="container">Built as a two-server campus canteen app · Server owns prices and business logic.</div></footer>

<div class="readypill" id="readyPill" onclick="showBill(activeBill)">⏱ <span id="readyPillText"></span></div>
<div class="floating"><button class="floatbtn" onclick="toggleCart()">🛒 Cart <span class="cartcount" id="cartCount">0</span></button><button class="floatbtn" onclick="toggleChat()">🤖</button></div>

<div class="drawer" id="cartDrawer"><div class="shade" onclick="toggleCart()"></div><aside class="panel"><div class="panelhead"><h2>Your cart</h2><button class="iconbtn" onclick="toggleCart()">✕</button></div><div id="cartItems"></div><textarea id="note" class="note" rows="3" placeholder="Optional note: less spicy, extra napkins…"></textarea><div class="total"><span>Total</span><span id="cartTotal">₹0</span></div><button class="primary" style="width:100%" onclick="placeOrder()">Place order</button></aside></div>

<div class="modal" id="modal"><div class="modalbox"><div class="panelhead"><h2 id="modalTitle">Meal ideas</h2><button class="iconbtn" onclick="closeModal()">✕</button></div><div id="modalBody"></div></div></div>

<div class="chat" id="chat"><div class="chathead">🤖 Campus Bites Assistant <button style="float:right;background:transparent;color:white" onclick="clearChat()">Clear</button></div><div class="messages" id="messages"><div class="msg">Hey! Ask me about today's menu, a budget combo, timings, or say “surprise me”.</div></div><div class="quick"><button onclick="quick('What is on today?')">Today's menu</button><button onclick="quick('I have ₹100')">₹100 combo</button><button onclick="quick('What are the timings?')">Timings</button><button onclick="quick('surprise me')">Surprise me</button></div><div class="chatinput"><button class="secondary" onclick="voiceInput()">🎙</button><input id="chatInput" placeholder="Ask anything…"><button class="primary" onclick="sendChat()">Send</button></div></div>
<div class="toast" id="toast"></div>

<script>
const API="http://localhost:5000";
let day="", menu=[], cart=JSON.parse(localStorage.getItem("canteenCart")||"{}"), favorites=JSON.parse(localStorage.getItem("favorites")||"[]"), selectedCategory="", selectedHint="";
const days=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"];
const categories=["All","Breakfast","Lunch","Snacks","Beverages","Dessert"];
const $=id=>document.getElementById(id);
function money(n){return "₹"+Number(n).toFixed(0)}
function toast(t){$("toast").textContent=t;$("toast").classList.add("show");setTimeout(()=>$("toast").classList.remove("show"),2200)}
function save(){localStorage.setItem("canteenCart",JSON.stringify(cart));localStorage.setItem("favorites",JSON.stringify(favorites));renderCart()}
function scrollToId(id){$(id).scrollIntoView({behavior:"smooth"})}
function toggleTheme(){document.body.classList.toggle("dark");localStorage.setItem("dark",document.body.classList.contains("dark"))}
function clearSearch(){$("search").value="";renderMenu()}
function toggleCart(){$("cartDrawer").classList.toggle("open")}
function toggleChat(){$("chat").classList.toggle("show")}
function closeModal(){Object.values(billPollers).forEach(clearInterval);billPollers={};$("modal").classList.remove("show")}
async function api(path,opt={}){let r=await fetch(API+path,opt);let d=await r.json().catch(()=>({error:"Server error"}));if(!r.ok)throw Error(d.error||"Request failed");return d}
let lang=localStorage.getItem("lang")||"en";
const translations={en:{menu:"Today's menu",combos:"Build a meal on your budget"},hi:{menu:"आज का मेन्यू",combos:"अपने बजट में खाना बनाएं"}};
function toggleLang(){lang=lang==="en"?"hi":"en";localStorage.setItem("lang",lang);$("menu").querySelector("h2").textContent=translations[lang].menu;$("builder").querySelector("h2").textContent=translations[lang].combos;toast(lang==="hi"?"हिंदी UI सक्रिय":"English UI active")}
function clearChat(){$("messages").innerHTML='<div class="msg">Conversation cleared. How can I help?</div>'}
function voiceInput(){if(!('SpeechRecognition' in window||'webkitSpeechRecognition' in window)){return toast("Voice input is not supported in this browser")}let R=window.SpeechRecognition||window.webkitSpeechRecognition;let r=new R();r.lang=lang==="hi"?"hi-IN":"en-IN";r.onresult=e=>{$("chatInput").value=e.results[0][0].transcript;sendChat()};r.start()}
async function init(){
 if(localStorage.getItem("dark")==="true")document.body.classList.add("dark");
 $("budget").oninput=()=>{$("budgetText").textContent=money($("budget").value)};
 $("search").oninput=renderMenu;
 $("chatInput").onkeydown=e=>{if(e.key==="Enter")sendChat()};
 
 document.querySelectorAll(".mealhint").forEach(b=>b.onclick=()=>{document.querySelectorAll(".mealhint").forEach(x=>x.classList.remove("active"));b.classList.add("active");selectedHint=b.dataset.hint});
 renderDays(); renderFilters(); renderHistory(); renderCart();
 await loadStatus(); await loadMenu(new Date().toLocaleDateString("en-US",{weekday:"long"}));let initialBill=typeof AUTO_BILL!=="undefined"?AUTO_BILL:activeBill;if(initialBill)showBill(initialBill);if("serviceWorker" in navigator)navigator.serviceWorker.register("/sw.js").catch(()=>{});
 setInterval(async()=>{await loadStatus();let today=new Date().toLocaleDateString("en-US",{weekday:"long"});if(day&&today!==day){toast("Today’s menu has changed — refreshing…");await loadMenu(today)}},30000);
}
function renderDays(){$("days").innerHTML=days.map(d=>`<button class="pill" id="day-${d}" onclick="loadMenu('${d}')">${d.slice(0,3)}</button>`).join("")}
function renderFilters(){$("filters").innerHTML=categories.map(c=>`<button class="pill ${c==="All"?"active":""}" onclick="setCategory('${c}',this)">${c}</button>`).join("")+`<button class="pill" onclick="setVeg(this)">🌱 Veg only</button><button class="pill" onclick="setFav(this)">♥ Favorites</button>`}
let veg=false,fav=false;
function setCategory(c,b){selectedCategory=c==="All"?"":c;document.querySelectorAll("#filters .pill").forEach(x=>x.classList.remove("active"));b.classList.add("active");renderMenu()}
function setVeg(b){veg=!veg;b.classList.toggle("active",veg);renderMenu()}
function setFav(b){fav=!fav;b.classList.toggle("active",fav);renderMenu()}
async function loadMenu(d){try{let x=await api("/menu?day="+encodeURIComponent(d));day=x.day;menu=x.items;$("dayLabel").textContent=day;days.forEach(z=>$("day-"+z).classList.toggle("active",z===day));renderMenu()}catch(e){toast(e.message)}}
function renderMenu(){
 let q=$("search").value.toLowerCase().trim();
 let list=menu.filter(x=>(!selectedCategory||x.category===selectedCategory)&&(!veg||x.veg)&&(!fav||favorites.includes(x.id))&&(!q||[x.name,x.description,x.category].join(" ").toLowerCase().includes(q)));
 $("menuGrid").innerHTML=list.length?list.map(item=>`
 <article class="card"><div class="foodimg" style="background-image:url('${item.image}')"><span class="badge">${item.available?(item.popular?"★ Popular":"Fresh"):"Sold out"}</span><button class="fav ${favorites.includes(item.dish_id)?"on":""}" onclick="toggleFav(${item.id})">♥</button></div>
 <div class="cardbody"><div class="cardtop"><h3>${item.name}</h3><span class="price">${money(item.price)}</span></div><div class="desc">${item.description}</div><div class="meta"><span class="tag">${item.veg?"🌱 Veg":"🍗 Non-veg"}</span><span class="tag">${item.spice_level===0?"No spice":item.spice_level===1?"Mild":item.spice_level===2?"Medium":"🌶 Spicy"}</span><span class="tag">⏱ ${item.prep_time_minutes} min</span></div>${item.available?`<select id="size-${item.id}" class="note" style="margin-bottom:8px">${(item.variants||[{id:"full",name:"Full",price:item.price}]).map(v=>`<option value="${v.id}">${v.name} · ${money(v.price)}</option>`).join("")}</select><select id="addon-${item.id}" class="note" multiple size="2" style="margin-bottom:8px">${Object.entries(item.addons||{}).map(([k,v])=>`<option value="${k}">${v.name}${v.price?" +"+money(v.price):""}</option>`).join("")}</select><button class="add" onclick="add(${item.id})">＋ Add</button>`:`<button class="add" style="background:#999" onclick="notifyMe('${item.dish_id}')">${notified.includes(item.dish_id)?"✓ Notify me set":"🔔 Notify me"}</button>`}</div></article>`).join(""):`<div class="card" style="padding:30px;grid-column:1/-1;text-align:center"><h3>No dishes found</h3><p class="muted">Try another search or filter.</p></div>`;
}
function addAllFavorites(){let count=0;menu.filter(x=>favorites.includes(x.dish_id)&&x.available).forEach(x=>{add(x.id);count++});toast(count?`Added ${count} favorite(s)`:"No available favorites today")}
function toggleFav(id){let item=menu.find(x=>x.id==id);let key=item?.dish_id||String(id);favorites=favorites.includes(key)?favorites.filter(x=>x!==key):[...favorites,key];save();renderMenu()}
function add(id,n=1){let item=menu.find(x=>x.id==id);let variant=$("size-"+id)?.value||"full";let addons=[...($("addon-"+id)?.selectedOptions||[])].map(o=>o.value).sort();let key=id+"|"+variant+"|"+addons.join(",");cart[key]=cart[key]||{item_id:id,quantity:0,variant,addons};cart[key].quantity+=n;save();toast("✓ Added to your cart")}
function notifyMe(d){if(!notified.includes(d))notified.push(d);localStorage.setItem("soldoutNotify",JSON.stringify(notified));renderMenu();toast("We'll remind you when this item appears available again") }
function addCombo(ids){ids.forEach(id=>add(id));closeModal();toast("Combo added to cart")}
function change(key,n){if(!cart[key])return;cart[key].quantity+=n;if(cart[key].quantity<=0)delete cart[key];save()}
function renderCart(){
 let entries=Object.entries(cart); let total=entries.reduce((s,[k,x])=>{let item=menu.find(i=>i.id==x.item_id);return s+(item?item.price*x.quantity:0)},0);
 $("cartCount").textContent=entries.reduce((s,[,x])=>s+x.quantity,0); $("cartTotal").textContent=money(total);
 $("cartItems").innerHTML=entries.length?entries.map(([key,x])=>{let item=menu.find(i=>i.id==x.item_id); if(!item)return `<div class="cartrow"><div><b>Unavailable item</b><div class="muted">Not on today's menu</div></div><button class="pill" onclick="delete cart['${key}'];save()">Remove</button></div>`; return `<div class="cartrow"><div><b>${item.name}</b><div class="muted">${x.variant}${x.addons?.length?" · "+x.addons.join(", "):""} · ${money(item.price)} each</div></div><div class="qty"><button onclick="change('${key}',-1)">−</button><b>${x.quantity}</b><button onclick="change('${key}',1)">＋</button></div></div>`}).join(""):"<p class='muted'>Your cart is empty. Add something delicious.</p>";
}

async function placeOrder(){
 let items=Object.values(cart).map(x=>({item_id:x.item_id,quantity:x.quantity,variant:x.variant,addons:x.addons}));
 if(!items.length)return toast("Your cart is empty");
 try{let d=await api("/order",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({items,note:$("note").value})});
 let b=d.bill;localStorage.setItem("lastBill",b.bill_id);let hist=JSON.parse(localStorage.getItem("pastOrders")||"[]");hist.unshift({id:b.bill_id,date:b.placed_at});localStorage.setItem("pastOrders",JSON.stringify(hist.slice(0,12)));
 cart={};$("note").value="";save();toggleCart();showBill(b.bill_id);toast("Order placed successfully")}
 catch(e){toast(e.message)}
}
function renderHistory(){let h=JSON.parse(localStorage.getItem("pastOrders")||"[]");$("history").innerHTML=h.length?h.map(x=>`<div class="receiptrow"><span>Bill #${x.id}<small class="muted"> · ${new Date(x.date).toLocaleString()}</small></span><button class="pill" onclick="showBill(${x.id})">View / Reorder</button></div>`).join(""):"No past orders yet. Your completed bill IDs will appear here."}
async function reorder(id){try{let d=await api("/bill/"+id), skipped=[];d.bill.items.forEach(x=>{let item=menu.find(i=>i.dish_id===x.dish_id);if(!item){skipped.push(x.name);return}let key=item.id+"|"+(x.variant||"full");cart[key]=cart[key]||{item_id:item.id,quantity:0,variant:x.variant||"full",addons:x.addons||[]};cart[key].quantity+=x.quantity});save();closeModal();toggleCart();toast(skipped.length?`Added available items. Skipped: ${skipped.join(", ")}`:"Previous order added to cart")}catch(e){toast(e.message)}}
async function showBill(id){try{let d=await api("/bill/"+id),b=d.bill; $("modalTitle").textContent="Bill #"+b.bill_id;$("modalBody").innerHTML=billHTML(b);$("modal").classList.add("show");renderQR(b.bill_id);pollBill(b.bill_id);updateReadyPill(b)}catch(e){toast(e.message)}}
function esc(v){return String(v??"").replace(/[&<>'"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;","'":"&#39;","\"":"&quot;"}[c]))}
function billHTML(b){let idx={received:0,preparing:1,ready:2,completed:3,cancelled:-1}[b.status];return `<div class="receipt"><div class="eyebrow">${esc(b.status.toUpperCase())}</div><h1>${b.status==="cancelled"?"Order cancelled":"Order #"+b.bill_id}</h1><div class="tracker">${["✓ Order received","● Preparing","✓ Ready","✓ Picked up"].map((x,i)=>`<div class="step ${i<=idx?"active":""}">${x}</div>`).join("")}</div><p class="muted">Estimated wait: <b id="eta">${b.ready_eta_minutes}</b> min · Queue position: <b>#${b.queue_position||"—"}</b></p>${b.items.map(x=>`<div class="receiptrow"><span>${esc(x.name)} × ${x.quantity}</span><b>${money(x.price*x.quantity)}</b></div>`).join("")}<div class="receiptrow"><span>Subtotal</span><b>${money(b.subtotal)}</b></div><div class="receiptrow"><span>Tax</span><b>${money(b.tax)}</b></div><div class="receiptrow" style="font-size:20px"><b>Total</b><b>${money(b.total)}</b></div>${b.note?`<p class="muted"><b>Note:</b> ${esc(b.note)}</p>`:""}<div id="qr" style="margin:18px auto;width:128px"></div><p class="muted" style="text-align:center;font-size:12px">Scan to open this bill</p><div style="display:flex;gap:8px;align-items:center;margin:12px 0"><input id="splitPeople" class="note" type="number" min="1" value="1" oninput="splitBill(${b.total})" placeholder="People"><b id="splitResult">${money(b.total)} / person</b></div><div class="actions"><button class="secondary" onclick="window.print()">Print</button><button class="secondary" onclick="reorder(${b.bill_id})">Order again</button>${b.status==="received"?`<button class="primary" onclick="cancelOrder(${b.bill_id})">Cancel order</button>`:""}${b.status==="ready"?`<button class="primary" onclick="completeOrder(${b.bill_id})">Mark as picked up</button>`:""}${["ready","completed"].includes(b.status)?`<button class="secondary" onclick="rate(${b.bill_id},'up')">👍</button><button class="secondary" onclick="rate(${b.bill_id},'down')">👎</button>`:""}<button class="secondary" onclick="closeModal()">Close</button></div></div>`}
function splitBill(total){let n=Math.max(1,Number($("splitPeople")?.value||1));$("splitResult").textContent=money(total/n)+" / person"}

function pollBill(id){Object.values(billPollers).forEach(clearInterval);activeBill=id;localStorage.setItem("activeBill",id);billPollers[id]=setInterval(async()=>{try{let d=await api("/bill/"+id);if(!$('modal').classList.contains('show')){clearInterval(billPollers[id]);return}$("modalBody").innerHTML=billHTML(d.bill);renderQR(d.bill.bill_id);updateReadyPill(d.bill);if(["ready","completed","cancelled"].includes(d.bill.status)){clearInterval(billPollers[id])}}catch(e){clearInterval(billPollers[id])}},10000)}
function renderQR(id){let el=$("qr");if(el&&window.QRCode){el.innerHTML="";new QRCode(el,{text:location.origin+"/bill/"+id,width:128,height:128})}}
function updateReadyPill(b){let show=b&&!["cancelled","completed"].includes(b.status);$("readyPill").classList.toggle("ready-pill-show",show);if(show)$("readyPillText").textContent=b.status+" · "+b.ready_eta_minutes+" min"}
async function completeOrder(id){try{let d=await api("/order/"+id+"/complete",{method:"POST"});showBill(id);toast("Pickup recorded") }catch(e){toast(e.message)}}

async function cancelOrder(id){try{await api("/order/"+id+"/cancel",{method:"POST"});showBill(id);toast("Order cancelled")}catch(e){toast(e.message)}}
async function rate(id,r){try{await api("/order/"+id+"/feedback",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({rating:r})});toast("Thanks for the feedback!")}catch(e){toast(e.message)}}
async function findCombos(){try{let d=await api("/combos",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({budget:+$("budget").value,category_hint:selectedHint})});$("modalTitle").textContent=`Combos under ${money(d.budget)}`;$("modalBody").innerHTML=d.combos.length?d.combos.map(c=>`<div class="combo"><div><b>${c.items.map(x=>x.name).join(" + ")}</b><div class="muted">${c.items.map(x=>money(x.price)).join(" · ")}</div></div><div><b>${money(c.total)}</b><br><button class="pill" onclick='addCombo(${JSON.stringify(c.items.map(x=>x.item_id))})'>Add</button></div></div>`).join(""):"No combination fits that budget today."; $("modal").classList.add("show")}catch(e){toast(e.message)}}
function addCombo(ids){ids.forEach(id=>add(id));closeModal();toast("Combo added to cart")}
function quick(t){$("chatInput").value=t;sendChat()}
async function sendChat(){let text=$("chatInput").value.trim();if(!text)return;addMsg(text,true);$("chatInput").value="";addMsg("Thinking…",false,"typing");try{let d=await api("/chat",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({message:text})});document.querySelector(".typing")?.remove();addMsg(d.message,false);if(d.type==="recommendation")add(d.item.item_id);if(d.type==="combos"){$("modalTitle").textContent="Assistant combos";$("modalBody").innerHTML=d.combos.map(c=>`<div class="combo"><b>${c.items.map(x=>x.name).join(" + ")} · ${money(c.total)}</b><button class="pill" onclick='addCombo(${JSON.stringify(c.items.map(x=>x.item_id))})'>Add</button></div>`).join("");$("modal").classList.add("show")}}catch(e){document.querySelector(".typing")?.remove();addMsg(e.message,false)}}
function addMsg(t,user=false,cl=""){let m=document.createElement("div");m.className="msg "+(user?"user ":"")+cl;m.textContent=t;$("messages").appendChild(m);$("messages").scrollTop=$("messages").scrollHeight}
async function loadStatus(){try{let d=await api("/status");$("canteenStatus").textContent=d.open?"OPEN · "+d.opening_hour+":00–"+d.closing_hour+":00":"CLOSED · Opens "+d.opening_hour+":00";$("statusDot").style.background=d.open?"#6ee7a3":"#f09b70";$("location").textContent=d.location}catch(e){$("canteenStatus").textContent="Backend offline"}}
document.addEventListener("keydown",e=>{if(e.target===$("budget")&&(e.key==="ArrowLeft"||e.key==="ArrowRight")){e.preventDefault();let b=$("budget");b.value=Math.max(+b.min,Math.min(+b.max,+b.value+(e.key==="ArrowRight"?+b.step:-+b.step)));b.dispatchEvent(new Event("input"));return}if(e.key==="/"&&!/input|textarea/i.test(document.activeElement.tagName)){e.preventDefault();$("search").focus()}if(e.key==="Escape"){toggleCart;closeModal();$("chat").classList.remove("show");$("cartDrawer").classList.remove("open")}})
init();
</script>
</body></html>"""

BILL_HTML = HTML


@app.get("/")
def index():
    return render_template_string(HTML, name="Campus Bites")

@app.get("/bill/<int:bill_id>")
def bill_page(bill_id):
    return render_template_string(BILL_HTML.replace("</script>\n</body>", f"const AUTO_BILL={bill_id};\n</script>\n</body>"), name="Campus Bites")

@app.get("/manifest.webmanifest")
def manifest():
    return {"name":"Campus Bites","short_name":"Canteen","start_url":"/","display":"standalone","background_color":"#f8f5ed","theme_color":"#174d36","icons":[]}

@app.get("/sw.js")
def sw():
    return ("self.addEventListener('install',e=>self.skipWaiting()); self.addEventListener('activate',e=>self.clients.claim());",200,{"Content-Type":"application/javascript"})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
