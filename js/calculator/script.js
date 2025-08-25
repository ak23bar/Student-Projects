// Global variables
let display = document.getElementById('display');
let currentInput = '';
let operator = '';
let previousInput = '';
let shouldResetDisplay = false;

// Function to append values to display
function appendToDisplay(value) {
    if (shouldResetDisplay) {
        display.value = '';
        shouldResetDisplay = false;
    }
    
    // Handle decimal point
    if (value === '.') {
        if (display.value.includes('.')) return;
        if (display.value === '') display.value = '0';
    }
    
    // Handle operators
    if (['+', '-', '*', '/'].includes(value)) {
        if (display.value === '' && value === '-') {
            display.value = '-';
            return;
        }
        
        if (previousInput !== '' && operator !== '' && !shouldResetDisplay) {
            calculateResult();
        }
        
        previousInput = display.value;
        operator = value;
        shouldResetDisplay = true;
        return;
    }
    
    // Handle numbers
    if (display.value === '0' && value !== '.') {
        display.value = value;
    } else {
        display.value += value;
    }
}

// Function to calculate the result
function calculateResult() {
    if (previousInput === '' || operator === '' || display.value === '') {
        return;
    }
    
    let prev = parseFloat(previousInput);
    let current = parseFloat(display.value);
    let result;
    
    try {
        switch (operator) {
            case '+':
                result = prev + current;
                break;
            case '-':
                result = prev - current;
                break;
            case '*':
                result = prev * current;
                break;
            case '/':
                if (current === 0) {
                    throw new Error('Division by zero');
                }
                result = prev / current;
                break;
            default:
                return;
        }
        
        // Round to prevent floating point errors
        result = Math.round(result * 100000000) / 100000000;
        
        display.value = result.toString();
        previousInput = '';
        operator = '';
        shouldResetDisplay = true;
        
    } catch (error) {
        display.value = 'Error';
        previousInput = '';
        operator = '';
        shouldResetDisplay = true;
    }
}

// Function to clear display
function clearDisplay() {
    display.value = '';
    currentInput = '';
    operator = '';
    previousInput = '';
    shouldResetDisplay = false;
}

// Function to delete last character
function deleteLast() {
    if (display.value.length > 0) {
        display.value = display.value.slice(0, -1);
    }
}

// Keyboard support
document.addEventListener('keydown', function(event) {
    const key = event.key;
    
    // Numbers and decimal
    if ((key >= '0' && key <= '9') || key === '.') {
        appendToDisplay(key);
    }
    // Operators
    else if (['+', '-', '*', '/'].includes(key)) {
        appendToDisplay(key);
    }
    // Enter or equals
    else if (key === 'Enter' || key === '=') {
        event.preventDefault();
        calculateResult();
    }
    // Escape or 'c' for clear
    else if (key === 'Escape' || key.toLowerCase() === 'c') {
        clearDisplay();
    }
    // Backspace for delete
    else if (key === 'Backspace') {
        event.preventDefault();
        deleteLast();
    }
});

// Animation on page load
window.addEventListener('load', function() {
    const calculator = document.querySelector('.calculator');
    calculator.style.opacity = '0';
    calculator.style.transform = 'translateY(50px)';
    calculator.style.transition = 'all 0.5s ease';
    
    setTimeout(() => {
        calculator.style.opacity = '1';
        calculator.style.transform = 'translateY(0)';
    }, 100);
});

// Initialize display when page loads
document.addEventListener('DOMContentLoaded', function() {
    display = document.getElementById('display');
});