# Universalis.py

A tool for interacting with the Universalis API in Python along with providing computed fields for summarizing data and rate limiting.

## Requires:
- Pydantic v2 (Required for additional computed fields)
- NumPy
- Ratelimit
- Requests

## Example

```python
from universalis import Universalis

# Get the current market information for Sublime Solution on Primal and print the average price
uni = Universalis()
current = uni.item("Primal", 28718)
print(current.averagePrice)
```

## Notes
- `item` can only request a single item, alternatively `items` can collect more than one item at once
  - `item_history` and `item_histories` behave similarly
- Some summary statistics aren't provided in the history endpoint and are added with computed fields
