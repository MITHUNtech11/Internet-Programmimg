/**
 * Internet Programming Lab - CSA43 Experiment 20
 * External JavaScript Library of Pure Functions
 * Operations: Factorial, Sum of Digits, Palindrome
 */

/**
 * 1. Calculates the factorial of an integer n (n!).
 * @param {number} n - Non-negative integer.
 * @returns {number|string} The factorial result, or error message.
 */
function calculateFactorial(n) {
    n = Number(n);
    if (!Number.isInteger(n) || n < 0) {
        return "Error: Factorial requires a non-negative integer (n >= 0).";
    }
    if (n === 0 || n === 1) return 1;

    let result = 1;
    for (let i = 2; i <= n; i++) {
        result *= i;
    }
    return result;
}

/**
 * 2. Computes the sum of the digits of a given number.
 * @param {number|string} num - Number to sum digits of.
 * @returns {number|string} Sum of digits.
 */
function sumOfDigits(num) {
    if (num === null || num === undefined || num === '') {
        return "Error: Please provide a valid number.";
    }
    const cleanStr = String(num).replace(/[^0-9]/g, '');
    if (cleanStr.length === 0) {
        return "Error: No valid digits found.";
    }

    let sum = 0;
    for (let char of cleanStr) {
        sum += parseInt(char, 10);
    }
    return sum;
}

/**
 * 3. Checks if a given string is a palindrome.
 * @param {string} str - String to test.
 * @returns {boolean|string} True if palindrome, false otherwise.
 */
function isPalindrome(str) {
    if (typeof str !== 'string' || str.trim() === '') {
        return "Error: Please provide a non-empty string.";
    }
    // Clean string by removing non-alphanumeric characters and converting to lowercase
    const normalized = str.toLowerCase().replace(/[^a-z0-9]/g, '');
    if (normalized.length === 0) return "Error: No alphanumeric characters to evaluate.";

    let left = 0;
    let right = normalized.length - 1;

    while (left < right) {
        if (normalized[left] !== normalized[right]) {
            return false;
        }
        left++;
        right--;
    }
    return true;
}
