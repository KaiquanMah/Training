## Python Coding Best Practices: Readability and Maintainability

The core philosophy of best practices is that **code is read a lot more often than it is written**. The goal is to make code easy to read, maintain, and build upon.

### I. Readability and Formatting

This section focuses on consistent and clean presentation, often aligning with the PEP 8 style guide.

| Practice | Description | Example (Good Practice) | Example (Bad Practice) |
| :--- | :--- | :--- | :--- |
| **Consistency** | Follow a consistent set of rules (e.g., indentation) across all source files. If adding to existing code, adopt the **existing pattern**. | Consistent **4 spaces** for indentation. | Using 4 spaces in one file and 2 tabs in another. |
| **Line Length** | Limit each line to a maximum of **79 characters** to avoid horizontal scrolling. | `result = long_function_name(` <br> &nbsp;&nbsp;&nbsp;&nbsp;`arg_one, arg_two)` | `result = long_function_name(arg_one, arg_two, arg_three, arg_four)` |
| **Indentation** | Recommended use of **four spaces** (not tabs). | (See alignment example below) | Mixing tabs and spaces. |
| **Continuation Lines** | Properly **align** continuation lines to clearly indicate they belong to the same expression. | `out = func(` <br> &nbsp;&nbsp;&nbsp;&nbsp;`var_two,` <br> &nbsp;&nbsp;&nbsp;&nbsp;`var_three)` | `out = func(` <br> `var_two,` <br> `var_three)` |
| **Line Breaks in Expressions** | Use line breaks **before** binary operators (e.g., `+`, `-`). | `var = first_val` <br> `+ second_val` <br> `- third_val` | `var = first_val +` <br> `second_val -` <br> `third_val` |
| **Separation** | Separate top-level functions and classes from other blocks of code by **two blank lines**. | `class MyClass: ...` <br> <br> <br> `def my_func(): ...` | Using only one blank line between them. |
| **Single Statement Per Line** | Only include a single statement on each line. | `x = 10` <br> `y = 20` | `x = 10; y = 20` |
| **Quotes** | Stick to a consistent use of either **single quotes** (`'...'`) or **double quotes** (`"..."`) for string literals throughout the code. | `'hello'` or `"world"` consistently. | `'hello'` in one file, `"world"` in another. |
| **Semicolons** | Do not terminate lines with a semicolon (`;`) as it's unnecessary and adds noise. | `print("value")` | `print("value");` |

---

### II. Naming Conventions

This section covers standard practices for naming identifiers to maintain readability.

| Type | Convention | Example (Good Practice) | Example (Bad Practice) |
| :--- | :--- | :--- | :--- |
| **Variables/Functions** | **Lowercase with underscores** (snake\_case). | `filtered_results` | `FilteredResults` (PascalCase) or `filteredResults` (camelCase) |
| **Constants** | **All UPPERCASE letters** with underscores. | `MAX_CONNECTIONS` | `max_connections` |
| **Clarity** | Be **descriptive** with names, clearly communicating the variable's context. | `revenue_2022` | `a`, `x`, `myvar` |

---

### III. Maintainability and Logic

These practices aim to minimize the risk of introducing errors when extending the code.

| Practice | Description | Example (Good Practice) | Example (Bad Practice) |
| :--- | :--- | :--- | :--- |
| **Code Structure** | Assume another developer (or your future self) will need to add to the code. Ensure the app is **modularized** and values are not **hardcoded**. | Separate application into logical modules (`.py` files). | Writing all application logic in one large script. |
| **Return Statements** | Avoid **multiple `return` statements** within a function body. Assign the return value to a local variable and use a single final `return` statement. | `def func():` <br> &nbsp;&nbsp;&nbsp;&nbsp;`result = None` <br> &nbsp;&nbsp;&nbsp;&nbsp;`if condition: result = var` <br> &nbsp;&nbsp;&nbsp;&nbsp;`return result` | `def func():` <br> &nbsp;&nbsp;&nbsp;&nbsp;`if condition: return var` <br> &nbsp;&nbsp;&nbsp;&nbsp;`return final_val` |
| **Optimization (Search)** | For checking the existence of an element in a collection, use a **`set` (using hash lookup) instead of a `list` (linear search)**. | **Search Cost:** $O(1)$ (Hash lookup) <br> `if element in my_set:` | **Search Cost:** $O(n)$ (Linear search) <br> `if element in my_list:` |


Good continuation line example
```python
def func(arg1,
         arg2,
         arg3):
    # do smth
    print("smth")
```

Bad continuation line example
```python

def func(arg1,
         arg2,
         arg3):
         # same alignment between fn args and subsequent fn code, which confuses readers
         # do smth
         print("smth")
```


Good return statement example
```python
def func():
    if condition1:
       final_value = 1
    if condition2:
       final_value = 2
    return final_value
```

Bad return statement example
```python
def func():
    final_value = 12345
    if condition1:
       var1 = 1
       return var1

    if condition2:
       var2 = 2
       return var2

    return final_value
```


