# Experiment 20: External JavaScript Operations (Factorial, Sum of Digits, Palindrome)

## Questions & Marks Distribution (10 Marks)
1. **Explanation of logic for each operation (3 marks)**
2. **Reusable JavaScript functions in single external file (4 marks)**
3. **Demonstration of calling functions from web application (3 marks)**

## Architecture
- `operations.js`: Standalone external module containing pure functions with return values:
  - `calculateFactorial(n)`
  - `sumOfDigits(num)`
  - `isPalindrome(str)`
- `index.html` & `script.js`: UI dashboard calling external functions and displaying results.
