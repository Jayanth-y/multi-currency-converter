const baseCurrencySelect = document.getElementById("baseCurrency");
const amountInput = document.getElementById("amount");
const currencyListDiv = document.getElementById("currencyList");
const conversionResultsDiv = document.getElementById("conversionResults");

const availableCurrencies = [
    "USD", "EUR", "INR", "GBP", "AUD", "CAD", "JPY", "CNY", "CHF", 
    "HKD", "SGD", "SEK", "NOK", "MXN", "NZD", "BRL", "RUB", "ZAR"
];

let selectedCurrencies = [];

// Function to Render Currency Selection Buttons
function renderCurrencyButtons() {
    currencyListDiv.innerHTML = "";
    availableCurrencies.forEach(currency => {
        const currencyButton = document.createElement("div");
        currencyButton.classList.add("currency-button");

        const currencyLabel = document.createElement("span");
        currencyLabel.innerText = currency;

        const toggleButton = document.createElement("button");
        toggleButton.innerText = selectedCurrencies.includes(currency) ? "✖" : "+";

        toggleButton.addEventListener("click", () => toggleCurrency(currency, toggleButton));

        currencyButton.appendChild(currencyLabel);
        currencyButton.appendChild(toggleButton);
        currencyListDiv.appendChild(currencyButton);
    });
}

// Function to Add/Remove Currencies
function toggleCurrency(currency, button) {
    if (selectedCurrencies.includes(currency)) {
        selectedCurrencies = selectedCurrencies.filter(c => c !== currency);
        button.innerText = "+";
    } else {
        if (selectedCurrencies.length < 12) {  // Limit to 8 currencies
            selectedCurrencies.push(currency);
            button.innerText = "✖";
        }
    }
    fetchConversionRates();
}

// Function to Fetch Exchange Rates
async function fetchConversionRates() {
    const baseCurrency = baseCurrencySelect.value;
    const amount = parseFloat(amountInput.value);

    if (isNaN(amount) || amount <= 0) {
        conversionResultsDiv.innerHTML = `<p>Please enter a valid amount.</p>`;
        return;
    }

    if (selectedCurrencies.length === 0) {
        conversionResultsDiv.innerHTML = `<p>Please select at least one currency.</p>`;
        return;
    }

    const BACKEND_URL = "http://127.0.0.1:8000";  // Change for deployment
    const apiUrl = `${BACKEND_URL}/convert/?base_currency=${baseCurrency}&amount=${amount}&target_currencies=${selectedCurrencies.join("&target_currencies=")}`;

    console.log("Fetching from API:", apiUrl);  // Log

    try {
        const response = await fetch(apiUrl);
        const data = await response.json();

        conversionResultsDiv.innerHTML = "";
        selectedCurrencies.forEach(currency => {
            const currencyBox = document.createElement("div");
            currencyBox.classList.add("currency-box");
            currencyBox.innerHTML = `
                <strong>${currency}:</strong> ${new Intl.NumberFormat("en-US").format(data.converted_values[currency].converted_amount)}
                <br> 1 ${currency} = ${data.converted_values[currency].one_target_to_base} ${baseCurrency}
                <br> 1 ${baseCurrency} = ${data.converted_values[currency].one_base_to_target} ${currency}
            `;
            conversionResultsDiv.appendChild(currencyBox);
        });

    } catch (error) {
        console.error("Fetch Error:", error);
        conversionResultsDiv.innerHTML = `<p>Error fetching conversion rates. Please try again later.</p>`;
    }
}

// Event Listeners
amountInput.addEventListener("input", fetchConversionRates);
baseCurrencySelect.addEventListener("change", fetchConversionRates);
renderCurrencyButtons();