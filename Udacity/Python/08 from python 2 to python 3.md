Python 3 was first launched in 2008

## 1. Syntax Changes

| Feature | Python 2 Behavior | Python 3 Behavior |
| :--- | :--- | :--- |
| **`print`** | A **statement** (`print "Hello"`) | A **function** (`print("Hello")`) |
| **Not Equals** | Operator could be `<>` | Operator must be **`!=`** |
| **Long Integers** | Explicit `long` type set by suffixing `L` (e.g., `123L`). `eg big_num = 1234567890123456789L` | **Removed**; standard `int` handles all integer sizes. `eg big_num = 1234567890123456789` |
| **String Literal** | Defaults to byte string; Unicode specified with `u` prefix. eg `s = u"Hello" (unicode string)` | **Unicode** is the **default string type**. `u` prefix is invalid. eg `s = "Hello" (unicode string), s=b"abeohba" (binary string)` |
| **Strings** | `s = "hello"` $\implies$ Array of bytes (`str`).<br>**Unicode:** Requires prefix: `u = u"hello"`. | `s = "hello"` $\implies$ Unicode string (`str`).<br>**Binary:** Requires prefix: `b = b"hello"`. |
| **Object Repr** | Used **backticks** (`` `obj` ``) operator for representation. eg `my_list = [1, 2] print ``my_list`` Output: [1, 2]` | Must use the **`repr()` function** (`repr(obj)`). `eg my_list = [1, 2] print(repr(my_list)) Output: [1, 2]` |
| **Division (`/`)** | Integer division between two integers returns an **integer dividend** (floor division). | Returns a **float** (true division result). Floor division uses **`//`**. |
| **Exception Handling**| Syntax was `except Exception, ex` | Syntax changed to **`except Exception as ex`** |
| **Keyword-Only Arguments** | Not available.<br>Args are positional by default: `def func(a, b): ...` | Enforced by `*` in signature:<br>`def func(a, *, b):`<br>Valid call: `func(1, b=2)` (so anything before `*` are positional args (a) vs anything after `*` are keyword args (b)) <br>**Invalid call:** `func(1, 2)` |
| **Dictionary Updates** | To merge: `d1.update(d2)` | **New Operators (from 3.9):**<br>**Merge:** `d3 = d1 \| d2`<br>**Update:** `d1 \|= d2` |
| **Dictionary Performance** | Less memory efficient. | Re-implemented for up to **25% more memory efficient** (from 3.6). |
| **`OrderedDict`** | Available in the `collections` module. **Standard `dict`** does **not** maintain insertion order. | Available in the `collections` module. **Standard `dict`** maintains insertion order by default (from 3.7). **OrderedDict** (added in 3.1) allows FIFO or LIFO order |
| **`venv` Module** | Used external tools like `virtualenv`. | **Standard Library:**<br>`import venv`<br>`venv.create('myenv')` |
| **`statistics` Module** | Had to use external libraries (e.g., NumPy). | **Standard Library:**<br>`import statistics`<br>`mean = statistics.mean([1, 2, 3])` |
| **`asyncio` Module** | Used threading/multiprocessing or other libraries. | **Built-in Async:**<br>`import asyncio`<br>`async def main(): ...`<br>`await ...` |
| **`concurrent.futures` Module** | Not available. | Simplifies asynchronous execution using `Future` objects and executors (from 3.2). |


---

## 2. Changes in Python Libraries

* **Accelerated Modules:** Confusion over having standard (`pickle`) and accelerated (`cPickle`) versions is eliminated. Python 3 attempts to load the **accelerated implementation by default** when importing the standard name.
* **Library Renaming:** Modules were renamed to comply with style guidelines (e.g., PascalCase removed):
    * `ConfigParser` $\rightarrow$ **`configparser`**
    * `Queue` $\rightarrow$ **`queue`**
    * `copy_reg` $\rightarrow$ **`copyreg`**

---

## 3. Other/Miscellaneous Changes

* **Dictionary Iteration:**
    * `keys()`, `items()`, and `values()` methods return **dynamic view objects**, not static lists (like they did in Python 2). Views reflect changes in the dictionary instantly.
    * The redundant methods (`iterkeys()`, `iteritems()`, `itervalues()`) have been **removed**.
* **`range()` Function:**
    * Python 2's `xrange()` (which returned an iterator object) is **removed**.
    * Python 3's **`range()` function now behaves like `xrange()`**; it returns an immutable sequence object (an iterator), not a list.
* **Rounding Behavior:** The built-in `round()` function now implements **Banker's Rounding** (round-half-to-even) for halfway cases to avoid statistical bias.
  * **Python 2 round(2.5) => 3**, round(3.5) => 4 (round up in halfway situation)
  * **Python 3 round(2.5) => 2**, round(3.5) => 4  (round to the nearest even value)
* **Exception Definition:** Custom exceptions **must derive from `BaseException`**.
* **Type Checking:** Python 3 is stricter, raising a **`TypeError`** for comparisons or sorting of **incompatible types** (e.g., sorting a list of mixed strings and numbers).

---

## 4. Utility for Migration

* **`2to3` Utility:** This is a script available with the Python interpreter that **automates many mechanical fixes** (like changing `print` statements) to translate Python 2 code to Python 3.
    * **Usage Example:** You invoke it as a script: `2to3 -w your_file.py` (The `-w` flag writes changes back to the file).

---

## 💡 Example: Python 3 Rounding (`round()`)

In Python 3, the `round()` function uses "round half to even" (Banker's Rounding) for values exactly halfway between two integers. This ensures that in a sequence of many rounding operations, the result is not statistically biased upward.

| Value to Round | Traditional Rounding | Python 3 `round()` | Reasoning |
| :--- | :--- | :--- | :--- |
| `2.5` | $3$ (Always round up) | **$2$** | Rounds to the **nearest even integer** (2 is even). |
| `3.5` | $4$ (Always round up) | **$4$** | Rounds to the **nearest even integer** (4 is even). |
| `4.5` | $5$ (Always round up) | **$4$** | Rounds to the **nearest even integer** (4 is even). |
| `4.6` | $5$ | **$5$** | Not a halfway case, standard rounding applies. |

