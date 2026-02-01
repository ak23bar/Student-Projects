let gameStarted = false;
let balance = 10000;
let portfolio = {};
let selectedStock = null;

const stocks = {
  TSLA: { name: "Tesla", price: 248.5, change: 0, history: [248.5] },
  AAPL: { name: "Apple", price: 189.25, change: 0, history: [189.25] },
  GOOGL: { name: "Google", price: 142.8, change: 0, history: [142.8] },
  MSFT: { name: "Microsoft", price: 415.3, change: 0, history: [415.3] },
  AMZN: { name: "Amazon", price: 178.65, change: 0, history: [178.65] },
  NVDA: { name: "NVIDIA", price: 495.2, change: 0, history: [495.2] },
  META: { name: "Meta", price: 488.9, change: 0, history: [488.9] },
  NFLX: { name: "Netflix", price: 612.3, change: 0, history: [612.3] },
};

let priceInterval = null;

// Make functions globally accessible
window.startGame = startGame;
window.selectStock = selectStock;
window.buyStock = buyStock;
window.sellStock = sellStock;

// ============================================
// COMPONENT HELPER FUNCTIONS
// ============================================

function Button(text, className, id = "", onclick = "") {
  const idAttr = id ? `id="${id}"` : "";
  const onclickAttr = onclick ? `onclick="${onclick}"` : "";
  return `<button class="${className}" ${idAttr} ${onclickAttr}>${text}</button>`;
}

function Input(type, id, className, placeholder = "", value = "") {
  const placeholderAttr = placeholder ? `placeholder="${placeholder}"` : "";
  const valueAttr = value ? `value="${value}"` : "";
  return `<input type="${type}" id="${id}" class="${className}" ${placeholderAttr} ${valueAttr}>`;
}

function Card(content, className, onclick = "") {
  const onclickAttr = onclick ? `onclick="${onclick}"` : "";
  return `<div class="${className}" ${onclickAttr}>${content}</div>`;
}

function Container(content, className, id = "") {
  const idAttr = id ? `id="${id}"` : "";
  return `<div class="${className}" ${idAttr}>${content}</div>`;
}

function StatItem(label, value, id = "") {
  const idAttr = id ? `id="${id}"` : "";
  return `
    <div class="stat-item">
      <span class="stat-label">${label}: </span>
      <span class="stat-value" ${idAttr}>${value}</span>
    </div>
  `;
}

// ============================================
// SCREENS
// ============================================

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
    <!-- Top Bar -->
    <div class="top-bar">
      <div class="logo">📈 STOCK SIMULATOR</div>
      <div class="stats">
        ${StatItem("Cash", `${balance.toFixed(2)}`, "balance")}
        ${StatItem(
          "Portfolio Value",
          `${calculatePortfolioValue().toFixed(2)}`,
          "portfolioValue"
        )}
        ${StatItem(
          "Total Value",
          `${(balance + calculatePortfolioValue()).toFixed(2)}`,
          "totalValue"
        )}
      </div>
    </div>

    <!-- Main Container -->
    <div class="main-container">
      <!-- Stock List Sidebar -->
      <div class="sidebar">
        <div class="sidebar-title">📊 AVAILABLE STOCKS</div>
        <div id="stockList"></div>
      </div>

      <!-- Center - Chart and Trade Panel -->
      <div class="center-panel">
        <div id="stockDetails" class="stock-details">
          <div class="empty-state">Select a stock to view details</div>
        </div>
      </div>

      <!-- Portfolio Sidebar -->
      <div class="portfolio-sidebar">
        <div class="sidebar-title">💼 YOUR PORTFOLIO</div>
        <div id="portfolioList"></div>
      </div>
    </div>
  `;
}

// ============================================
// GAME FUNCTIONS
// ============================================

function startGame() {
  gameStarted = true;
  balance = 10000;
  portfolio = {};
  createApp();
  renderStockList();
  renderPortfolio();
  startPriceUpdates();
}

function createApp() {
  const app = document.getElementById("app");

  if (!gameStarted) {
    app.innerHTML = StartScreen();
  } else {
    app.innerHTML = GameScreen();
  }
}

function renderStockList() {
  const container = document.getElementById("stockList");
  if (!container) return;

  container.innerHTML = Object.keys(stocks)
    .map((symbol) => {
      const stock = stocks[symbol];
      const changeClass = stock.change >= 0 ? "price-up" : "price-down";
      const changeSymbol = stock.change >= 0 ? "▲" : "▼";
      const isSelected = selectedStock === symbol;

      return Card(
        `
        <div class="stock-name">${symbol}</div>
        <div class="company-name">${stock.name}</div>
        <div class="stock-price">${stock.price.toFixed(2)}</div>
        <div class="${changeClass}">
          ${changeSymbol} ${Math.abs(stock.change).toFixed(2)}%
        </div>
      `,
        `stock-card ${isSelected ? "selected" : ""}`,
        `selectStock('${symbol}')`
      );
    })
    .join("");
}

function selectStock(symbol) {
  selectedStock = symbol;
  renderStockList();
  renderStockDetails();
}

function renderStockDetails() {
  const container = document.getElementById("stockDetails");
  if (!container || !selectedStock) return;

  const stock = stocks[selectedStock];
  const changeClass = stock.change >= 0 ? "price-up" : "price-down";

  container.innerHTML = `
    <div class="stock-header">
      <div>
        <h2>${selectedStock} - ${stock.name}</h2>
        <div class="current-price">${stock.price.toFixed(2)}</div>
        <div class="${changeClass}">${
    stock.change >= 0 ? "+" : ""
  }${stock.change.toFixed(2)}%</div>
      </div>
    </div>

    <div class="trade-panel">
      <h3>Trade ${selectedStock}</h3>
      
      <div class="input-group">
        <label>Shares to Trade</label>
        ${Input("number", "shareAmount", "input-field", "Enter shares", "1")}
      </div>

      <div class="trade-info">
        <div>
          <span>Price per share:</span>
          <span>${stock.price.toFixed(2)}</span>
        </div>
        <div>
          <span>Total cost:</span>
          <span id="totalCost">${stock.price.toFixed(2)}</span>
        </div>
      </div>

      <div class="trade-buttons">
        ${Button("BUY", "trade-btn buy-btn", "buyBtn", "buyStock()")}
        ${Button("SELL", "trade-btn sell-btn", "sellBtn", "sellStock()")}
      </div>
    </div>
  `;

  // Update total cost when shares input changes
  document
    .getElementById("shareAmount")
    .addEventListener("input", updateTotalCost);
}

function updateTotalCost() {
  if (!selectedStock) return;
  const shares = parseInt(document.getElementById("shareAmount").value) || 0;
  const stock = stocks[selectedStock];
  const total = shares * stock.price;
  document.getElementById("totalCost").textContent = `${total.toFixed(2)}`;
}

function buyStock() {
  if (!selectedStock) return;

  const shares = parseInt(document.getElementById("shareAmount").value) || 0;
  const stock = stocks[selectedStock];
  const cost = shares * stock.price;

  if (shares <= 0) {
    alert("Please enter a valid number of shares!");
    return;
  }

  if (cost > balance) {
    alert(
      `Insufficient funds! You need ${cost.toFixed(
        2
      )} but only have ${balance.toFixed(2)}`
    );
    return;
  }

  // Execute trade
  balance -= cost;
  portfolio[selectedStock] = (portfolio[selectedStock] || 0) + shares;

  // Update UI
  updateStats();
  renderPortfolio();
  alert(
    `✅ Bought ${shares} shares of ${selectedStock} for ${cost.toFixed(2)}`
  );
}

function sellStock() {
  if (!selectedStock) return;

  const shares = parseInt(document.getElementById("shareAmount").value) || 0;
  const stock = stocks[selectedStock];
  const earnings = shares * stock.price;

  if (shares <= 0) {
    alert("Please enter a valid number of shares!");
    return;
  }

  if (!portfolio[selectedStock] || portfolio[selectedStock] < shares) {
    alert(
      `You don't own enough shares! You have ${
        portfolio[selectedStock] || 0
      } shares.`
    );
    return;
  }

  // Execute trade
  balance += earnings;
  portfolio[selectedStock] -= shares;
  if (portfolio[selectedStock] === 0) {
    delete portfolio[selectedStock];
  }

  // Update UI
  updateStats();
  renderPortfolio();
  alert(
    `✅ Sold ${shares} shares of ${selectedStock} for ${earnings.toFixed(2)}`
  );
}

function renderPortfolio() {
  const container = document.getElementById("portfolioList");
  if (!container) return;

  const holdings = Object.keys(portfolio);

  if (holdings.length === 0) {
    container.innerHTML = '<div class="empty-state">No stocks owned yet</div>';
    return;
  }

  container.innerHTML = holdings
    .map((symbol) => {
      const shares = portfolio[symbol];
      const stock = stocks[symbol];
      const value = shares * stock.price;
      const changeClass = stock.change >= 0 ? "price-up" : "price-down";

      return Card(
        `
        <div class="portfolio-stock">
          <div class="stock-name">${symbol}</div>
          <div class="shares">${shares} shares</div>
          <div class="stock-value">${value.toFixed(2)}</div>
          <div class="${changeClass}">${
          stock.change >= 0 ? "+" : ""
        }${stock.change.toFixed(2)}%</div>
        </div>
      `,
        "portfolio-card"
      );
    })
    .join("");
}

function calculatePortfolioValue() {
  let total = 0;
  Object.keys(portfolio).forEach((symbol) => {
    total += portfolio[symbol] * stocks[symbol].price;
  });
  return total;
}

function updateStats() {
  const balanceEl = document.getElementById("balance");
  const portfolioValueEl = document.getElementById("portfolioValue");
  const totalValueEl = document.getElementById("totalValue");

  if (balanceEl) balanceEl.textContent = `${balance.toFixed(2)}`;
  if (portfolioValueEl)
    portfolioValueEl.textContent = `${calculatePortfolioValue().toFixed(2)}`;
  if (totalValueEl)
    totalValueEl.textContent = `${(
      balance + calculatePortfolioValue()
    ).toFixed(2)}`;
}

function startPriceUpdates() {
  if (priceInterval) clearInterval(priceInterval);

  priceInterval = setInterval(() => {
    Object.keys(stocks).forEach((symbol) => {
      const stock = stocks[symbol];
      // Realistic price changes: -2% to +2%
      const changePercent = (Math.random() - 0.5) * 0.04;
      const newPrice = stock.price * (1 + changePercent);

      stock.price = parseFloat(newPrice.toFixed(2));
      stock.change = changePercent * 100;
      stock.history.push(stock.price);
      if (stock.history.length > 50) stock.history.shift();
    });

    renderStockList();
    renderPortfolio();
    updateStats();
    if (selectedStock) {
      renderStockDetails();
    }
  }, 2000); // Update every 2 seconds
}

// ============================================
// INITIALIZE
// ============================================

window.addEventListener("DOMContentLoaded", () => {
  createApp();
});
