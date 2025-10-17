# Primitive types
- str
- int
- float
- bool
- bytes
- None - when u dont return a value

# Composite types
- list
- set
- tuple
- dict

`typing` module
- Optional
- Any
- Sequence
- Callable

Note:
- Python is a dynamically-typed language, and **type hints are strictly optional metadata, not enforced rules**
- Dynamic Typing: Python is fundamentally a dynamically-typed language. This means it checks the type of a variable only when the code is running (runtime), and it doesn't care about type declarations beforehand. A variable's type is tied to the value it holds, not to the variable name itself.
- Hints are Metadata: Type hints are stored as metadata attached to the code (they live in the `__annotations__` attribute), but the **interpreter simply skips them during execution.**
- Assignment is Valid: When the interpreter reaches dict1 = {"value2": "Four"}, it doesn't consult the old type hint. It simply says, "Okay, the variable dict1 now points to a new, valid dictionary object with a string key." The operation is a valid assignment in Python, so the program continues to run without an error.
 
eg
```python
from typing import Any

# dict1 is a 'dict'
# key is an 'int'
# value allows any data types
dict1: dict[int, Any] = {3: "Three"}

# the line below will be flagged in IDE eg PyCharm
# because PyCharm's built-in type checker or Mypy reads this type hint and performs static analysis (checking the code before it runs).
# They detect that the new value assigned to dict1 violates the rule established in the type hint (dict[int, Any]), and therefore issue a warning or error flag
# OTHERWISE THE CODE WILL STILL RUN OUTSIDE OF AN IDE
dict1 = {"value2": "Four"}
```


eg
```python
from typing import Any, Sequence

# Sequence => eg list, tuple, set
# elements in the sequence => 'Any' data type
sequence_function(seq: Sequence[Any]):
    for item in seq:
        print(item)

sequence_function([4,7, -1 ])
sequence_function((4,'seven','-1 ))

# int '3' is not a sequence
# will be flagged by the IDE
sequence_function(3)
```




