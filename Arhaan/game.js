/* ============================================================
     STOCK SIMULATOR — Single File Version (JS+CSS+HTML)
     Includes:
     - Full UI rendering
     - Injected CSS
     - Price history charts
     - Portfolio history chart
     - Stop-loss auto selling
     - –20% to +10% volatility
=============================================================== */

/* ------------------------------*
 * Inject CSS into the document *
 * ------------------------------*/
(function injectCSS() {
  const css = `
    * { margin: 0; padding: 0; box-sizing: border-box; }

    body {
      font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
      background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 50%, #0f172a 100%);
      color: white;
      min-height: 100vh;
    }

    /* Start Screen */
    .start-screen {
      display: flex; flex-direction: column;
      align-items: center; justify-content: center;
      min-height: 100vh; text-align: center;
    }

    .game-title {
      font-size: 5rem; font-weight: 900;
      background: linear-gradient(to right, #60a5fa, #a78bfa);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      letter-spacing: 0.1em;
      margin-bottom: 1rem;
    }

    .subtitle {
      font-size: 1.5rem; color: #94a3b8;
      margin-bottom: 3rem;
    }

    .start-btn {
      padding: 1.5rem 4rem;
      font-size: 1.5rem;
      border-radius: 1rem;
      background: linear-gradient(135deg, #10b981, #059669);
      border: none;
      box-shadow: 0 10px 30px rgba(16,185,129,.4);
      cursor: pointer; color: white;
      font-weight: bold; transition: .3s;
    }

    .start-btn:hover {
      transform: translateY(-5px);
      box-shadow: 0 15px 40px rgba(16,185,129,.6);
    }

    /* Top Bar */
    .top-bar {
      background: rgba(30,41,59,.9);
      backdrop-filter: blur(10px);
      border-bottom: 2px solid #334155;
      padding: 1.5rem 2rem;
      display: flex; justify-content: space-between; align-items: center;
    }

    .logo {
      font-size: 1.5rem; font-weight: bold;
      background: linear-gradient(to right, #60a5fa, #a78bfa);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    .stats { display: flex; gap: 2rem; }

    .stat-item {
      background: rgba(15,23,42,.7);
      padding: .75rem 1.5rem;
      border-radius: .75rem;
      border: 1px solid #334155;
    }

    .stat-label { color: #94a3b8; font-size: .875rem; }
    .stat-value { font-weight: bold; font-size: 1.25rem; color: #10b981; margin-left: .5rem; }

    /* Main Layout */
    .main-container {
      display: grid;
      grid-template-columns: 350px 1fr 350px;
      height: calc(100vh - 100px);
      gap: 1rem; padding: 1rem;
    }

    .sidebar, .portfolio-sidebar {
      background: rgba(30,41,59,.5);
      backdrop-filter: blur(10px);
      border: 1px solid #334155;
      border-radius: 1rem;
      padding: 1.5rem; overflow-y: auto;
    }

    .sidebar-title {
      font-weight: bold; font-size: .875rem;
      color: #cbd5e1; letter-spacing: .05em;
      margin-bottom: 1.5rem; text-transform: uppercase;
    }

    /* Stock Cards */
    .stock-card {
      background: rgba(15,23,42,.7);
      border-radius: .75rem;
      border: 2px solid transparent;
      padding: 1rem; margin-bottom: 1rem;
      cursor: pointer; transition: .3s;
    }

    .stock-card:hover { border-color: #475569; transform: translateX(5px); }
    .stock-card.selected { border-color: #3b82f6; box-shadow: 0 0 20px rgba(59,130,246,.3); }

    .stock-name { font-size: 1.25rem; font-weight: bold; }
    .company-name { color: #94a3b8; font-size: .875rem; margin-bottom: .5rem; }
    .stock-price { font-size: 1.125rem; font-weight: bold; }

    .price-up { color: #10b981; }
    .price-down { color: #ef4444; }

    /* Center Panel */
    .center-panel {
      background: rgba(30,41,59,.5);
      backdrop-filter: blur(10px);
      border: 1px solid #334155;
      border-radius: 1rem;
      padding: 2rem; overflow-y: auto;
    }

    .current-price {
      font-size: 3rem;
      font-weight: bold;
      color: #60a5fa;
      margin: .5rem 0;
    }

    /* Trade Panel */
    .trade-panel {
      background: rgba(15,23,42,.5);
      border: 1px solid #334155;
      border-radius: 1rem;
      padding: 2rem; margin-top: 2rem;
    }

    .trade-panel h3 { font-size: 1.5rem; margin-bottom: 1.5rem; color: #60a5fa; }

    .input-group { margin-bottom: 1.5rem; }
    .input-group label { color: #94a3b8; font-size: .875rem; margin-bottom: .5rem; display: block; }

    .input-field {
      width: 100%; padding: 1rem;
      background: #1e293b;
      border: 2px solid #334155;
      border-radius: .5rem;
      color: white; font-weight: bold;
      font-size: 1.125rem;
    }

    .trade-btn {
      padding: 1.25rem;
      border-radius: .75rem;
      font-weight: bold;
      font-size: 1.25rem;
      cursor: pointer; border: none;
      transition: .3s; color: white;
    }

    .buy-btn { background: linear-gradient(135deg,#10b981,#059669); }
    .sell-btn { background: linear-gradient(135deg,#ef4444,#dc2626); }

    /* Portfolio Cards */
    .portfolio-card {
      background: rgba(15,23,42,.7);
      border: 1px solid #334155;
      border-radius: .75rem;
      padding: 1rem;
      margin-bottom: 1rem;
    }

    .shares { color: #94a3b8; font-size: .875rem; }
    .stock-value { font-size: 1.125rem; color: #60a5fa; font-weight: bold; }

    .empty-state {
      height: 100%;
      display: flex; justify-content: center; align-items: center;
      color: #64748b; font-size: 1.125rem;
    }
  `;
  const style = document.createElement("style");
  style.textContent = css;
  document.head.appendChild(style);
})();

/* ------------------------------*
 * Global Game State Variables  *
 * ------------------------------*/
let gameStarted = false;
let balance = 10000;
let selectedStock = null;
let priceInterval = null;

let portfolio = {}; // { TSLA: { shares: X, stopLoss: Y } }
let portfolioHistory = [];

let stockChart = null;
let portfolioChart = null;

/* ------------------------------*
 * Stock List
 * ------------------------------*/
const stocks = {
  TSLA: { name: "Tesla", price: 248.5, change: 0, history: [248.5] },
  AAPL: { name: "Apple", price: 189.25, change: 0, history: [189.25] },
  GOOGL:{ name:"Google", price:142.8, change:0, history:[142.8] },
  MSFT:{ name:"Microsoft", price:415.3, change:0, history:[415.3] },
  AMZN:{ name:"Amazon", price:178.65, change:0, history:[178.65] },
  NVDA:{ name:"NVIDIA", price:495.2, change:0, history:[495.2] },
  META:{ name:"Meta", price:488.9, change:0, history:[488.9] },
  NFLX:{ name:"Netflix", price:612.3, change:0, history:[612.3] }
};

/* ------------------------------*
 * Utility Rendering Functions  *
 * ------------------------------*/
function Button(text, className, id="", onclick="") {
  return `<button class="${className}" id="${id}" onclick="${onclick}">${text}</button>`;
}
function Input(type,id,cls,placeholder="",value="") {
  return `<input type="${type}" id="${id}" class="${cls}" placeholder="${placeholder}" value="${value}">`;
}
function Card(html, className, onclick="") {
  return `<div class="${className}" onclick="${onclick}">${html}</div>`;
}
function StatItem(label, value, id="") {
  return `<div class="stat-item">
    <span class="stat-label">${label}: </span>
    <span class="stat-value" id="${id}">${value}</span>
  </div>`;
}

/* ------------------------------*
 * Main Screens
 * ------------------------------*/
function StartScreen() {
  return `
    <div class="start-screen">
      <h1 class="game-title">STOCK SIMULATOR</h1>
      <p class="subtitle">Master the art of trading</p>
      ${Button("START GAME", "start-btn", "startBtn", "startGame()")}
    </div>
  `;
}

function GameScreen() {
  return `
    <div class="top-bar">
      <div class="logo">📈 STOCK SIMULATOR</div>
      <div class="stats">
        ${StatItem("Cash", `$${balance.toFixed(2)}`, "balance")}
        ${StatItem("Portfolio Value", `$${calculatePortfolioValue().toFixed(2)}`, "portfolioValue")}
        ${StatItem("Total Value", `$${(balance+calculatePortfolioValue()).toFixed(2)}`, "totalValue")}
      </div>
    </div>

    <div class="main-container">
      <div class="sidebar">
        <div class="sidebar-title">📊 AVAILABLE STOCKS</div>
        <div id="stockList"></div>
      </div>

      <div class="center-panel">
        <div id="stockDetails">
          <div class="empty-state">Select a stock to view details</div>
        </div>
      </div>

      <div class="portfolio-sidebar">
        <div class="sidebar-title">💼 YOUR PORTFOLIO</div>
        <div id="portfolioList"></div>

        <canvas id="portfolioChart" height="120"></canvas>
      </div>
    </div>
  `;
}

/* ------------------------------*
 * Game Startup
 * ------------------------------*/
function startGame() {
  gameStarted = true;
  balance = 10000;
  selectedStock = null;
  portfolio = {};
  portfolioHistory = [];

  renderApp();
  renderStockList();
  renderPortfolio();

  startPriceUpdates();
}

/* Render main container */
function renderApp() {
  document.getElementById("app").innerHTML =
    gameStarted ? GameScreen() : StartScreen();
}

/* ------------------------------*
 * STOCK LIST RENDERING
 * ------------------------------*/
function renderStockList() {
  const list = document.getElementById("stockList");
  if (!list) return;

  list.innerHTML = Object.keys(stocks).map(symbol => {
    const stock = stocks[symbol];
    const changeClass = stock.change >= 0 ? "price-up" : "price-down";
    const changeSymbol = stock.change >= 0 ? "▲" : "▼";

    return Card(
      `
        <div class="stock-name">${symbol}</div>
        <div class="company-name">${stock.name}</div>
        <div class="stock-price">$${stock.price.toFixed(2)}</div>
        <div class="${changeClass}">${changeSymbol} ${Math.abs(stock.change).toFixed(2)}%</div>
      `,
      `stock-card ${selectedStock === symbol ? "selected" : ""}`,
      `selectStock('${symbol}')`
    );
  }).join("");
}

/* ------------------------------*
 * STOCK DETAILS + TRADE PANEL
 * ------------------------------*/
function selectStock(symbol) {
  selectedStock = symbol;
  renderStockList();
  renderStockDetails();
}

function renderStockDetails() {
  if (!selectedStock) return;

  const stock = stocks[selectedStock];
  const changeClass = stock.change >= 0 ? "price-up" : "price-down";

  const container = document.getElementById("stockDetails");
  container.innerHTML = `
    <div class="stock-header">
      <h2>${selectedStock} - ${stock.name}</h2>
      <div class="current-price">$${stock.price.toFixed(2)}</div>
      <div class="${changeClass}">
        ${stock.change >= 0 ? "+" : ""}${stock.change.toFixed(2)}%
      </div>
    </div>

    <canvas id="stockChart" height="120"></canvas>

    <div class="trade-panel">
      <h3>Trade ${selectedStock}</h3>

      <div class="input-group">
        <label>Shares to Trade</label>
        ${Input("number", "shareAmount", "input-field", "Enter shares", "1")}
      </div>

      <div class="input-group">
        <label>Stop-Loss Price (optional)</label>
        ${Input("number", "stopLoss", "input-field", "Auto sell if price drops to...")}
      </div>

      <div class="trade-buttons">
        ${Button("BUY", "trade-btn buy-btn", "buyBtn", "buyStock()")}
        ${Button("SELL", "trade-btn sell-btn", "sellBtn", "sellStock()")}
      </div>
    </div>
  `;

  renderStockChart(selectedStock);
}

/* ------------------------------*
 * BUY / SELL + STOP LOSS
 * ------------------------------*/
function buyStock() {
  if (!selectedStock) return;

  const shares = parseInt(document.getElementById("shareAmount").value);
  const stock = stocks[selectedStock];
  const cost = shares * stock.price;

  if (shares <= 0 || isNaN(shares)) {
    alert("Enter valid shares"); return;
  }

  if (cost > balance) {
    alert("Insufficient balance"); return;
  }

  if (!portfolio[selectedStock]) {
    portfolio[selectedStock] = { shares: 0, stopLoss: null };
  }

  portfolio[selectedStock].shares += shares;

  const sl = parseFloat(document.getElementById("stopLoss").value);
  if (!isNaN(sl)) portfolio[selectedStock].stopLoss = sl;

  balance -= cost;
  updateStats();
  renderPortfolio();

  alert(`Bought ${shares} shares of ${selectedStock}`);
}

function sellStock() {
  if (!selectedStock || !portfolio[selectedStock]) return;

  const shares = parseInt(document.getElementById("shareAmount").value);
  if (shares <= 0 || isNaN(shares)) return alert("Invalid shares");

  const owned = portfolio[selectedStock].shares;
  if (shares > owned) return alert("Not enough shares");

  const stock = stocks[selectedStock];
  const revenue = shares * stock.price;

  portfolio[selectedStock].shares -= shares;
  if (portfolio[selectedStock].shares <= 0)
    delete portfolio[selectedStock];

  balance += revenue;

  updateStats();
  renderPortfolio();
  alert(`Sold ${shares} shares of ${selectedStock}`);
}

/* ------------------------------*
 * PORTFOLIO DISPLAY
 * ------------------------------*/
function renderPortfolio() {
  const container = document.getElementById("portfolioList");
  if (!container) return;

  const items = Object.keys(portfolio);
  if (items.length === 0) {
    container.innerHTML = `<div class="empty-state">No stocks owned</div>`;
    return;
  }

  container.innerHTML = items.map(symbol => {
    const data = portfolio[symbol];
    const stock = stocks[symbol];
    const value = data.shares * stock.price;

    return Card(`
      <div class="stock-name">${symbol}</div>
      <div class="shares">${data.shares} shares</div>
      <div class="stock-value">$${value.toFixed(2)}</div>
    `, "portfolio-card");
  }).join("");

  updatePortfolioChart();
}

/* ------------------------------*
 * PORTFOLIO VALUE CALCULATION
 * ------------------------------*/
function calculatePortfolioValue() {
  let total = 0;
  for (const sym in portfolio) {
    total += portfolio[sym].shares * stocks[sym].price;
  }
  return total;
}

function updateStats() {
  const bal = document.getElementById("balance");
  const pv = document.getElementById("portfolioValue");
  const tv = document.getElementById("totalValue");

  if (bal) bal.textContent = `$${balance.toFixed(2)}`;
  if (pv) pv.textContent = `$${calculatePortfolioValue().toFixed(2)}`;
  if (tv) tv.textContent = `$${(balance + calculatePortfolioValue()).toFixed(2)}`;

  portfolioHistory.push(balance + calculatePortfolioValue());
  if (portfolioHistory.length > 100) portfolioHistory.shift();

  updatePortfolioChart();
}

/* ------------------------------*
 * PRICE UPDATES (–20% to +10%)
 * + STOP LOSS AUTO-SELL
 * ------------------------------*/
function startPriceUpdates() {
  if (priceInterval) clearInterval(priceInterval);

  priceInterval = setInterval(() => {
    Object.keys(stocks).forEach(symbol => {
      const stock = stocks[symbol];

      // Change range: –20% to +10%
      const pctChange = Math.random() * 0.30 - 0.20;

      stock.price = parseFloat((stock.price * (1 + pctChange)).toFixed(2));
      stock.change = pctChange * 100;

      stock.history.push(stock.price);
      if (stock.history.length > 80) stock.history.shift();
    });

    // Auto-trigger Stop-Loss
    for (const sym in portfolio) {
      const p = portfolio[sym];
      const stock = stocks[sym];

      if (p.stopLoss && stock.price <= p.stopLoss) {
        const shares = p.shares;
        balance += shares * stock.price;
        delete portfolio[sym];

        alert(`⛔ STOP-LOSS TRIGGERED for ${sym}! Sold ${shares} shares at $${stock.price}`);
      }
    }

    renderStockList();
    renderPortfolio();
    updateStats();

    if (selectedStock) renderStockDetails();
  }, 2000);
}

/* ------------------------------*
 * CHARTS (Stock + Portfolio)
 * ------------------------------*/
function renderStockChart(symbol) {
  const canvas = document.getElementById("stockChart");
  if (!canvas) return;

  const stock = stocks[symbol];

  if (stockChart) stockChart.destroy();

  stockChart = new Chart(canvas, {
    type: "line",
    data: {
      labels: stock.history.map((_, i) => i),
      datasets: [{
        label: `${symbol} Price`,
        data: stock.history,
        borderColor: "#60a5fa",
        backgroundColor: "rgba(96,165,250,.25)",
        tension: .3
      }]
    },
    options: { scales: { x: { display:false } } }
  });
}

function updatePortfolioChart() {
  const canvas = document.getElementById("portfolioChart");
  if (!canvas) return;

  if (portfolioChart) portfolioChart.destroy();

  portfolioChart = new Chart(canvas, {
    type: "line",
    data: {
      labels: portfolioHistory.map((_, i) => i),
      datasets: [{
        label: "Portfolio Value",
        data: portfolioHistory,
        borderColor: "#10b981",
        backgroundColor: "rgba(16,185,129,.25)",
        tension: .3
      }]
    },
    options: { scales: { x: { display:false } } }
  });
}

/* ------------------------------*
 * Start Rendering
 * ------------------------------*/
window.addEventListener("DOMContentLoaded", () => {
  renderApp();
});
