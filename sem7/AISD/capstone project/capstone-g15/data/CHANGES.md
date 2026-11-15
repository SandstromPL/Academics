| ID  | Kind   | v1                                             | v2                                                                                         | Inferable from signatures? |
|-----|--------|--------------------------------------------------|--------------------------------------------------------------------------------------------|------------------------------|
| G01 | Rename | `get_balance(account_id)`                        | `fetch_balance(account_id)`                                                                | Yes                          |
| G02 | Order  | `transfer(amount, from_id, to_id)`               | `transfer(from_id, to_id, amount)`                                                         | No                           |
| G03 | Return | `get_transaction(tx_id)` returns a dict with key | `get_transaction(tx_id)` returns a `Transaction` dataclass, attribute `tx_id`              | No                           |
| G04 | Remove | `charge_and_receipt(acc, amount)`                | `make_receipt(charge(acc, Money(amount, "INR")))`                                           | No                           |
| G05 | Rename | `InsufficientFunds`                              | `BalanceTooLow`                                                                            | Yes                          |
| G06 | Rename | `AccountNotFound`                                | `UnknownAccount`                                                                           | Yes                          |
| G07 | Change | `charge(acc, amount, currency="INR")` returns    | `charge(acc, money: Money)` returns `Transaction`                                          | No                           |
|     |        | a dict                                         |                                                                                            |                              |
| G08 | Change | `format_amount(rupees: float)`                   | `format_amount(value: int)` in paise                                                       | No                           |
| G09 | Remove | `list_transactions(acc, limit=10)`               | `list_transactions(acc, limit)`, items are `Transaction`                                   | No                           |
| G10 | Change | `open_account(name, balance=0.0)`                | `open_account(name, *, opening_balance=0.0)` keyword-only                                  | No                           |
| G11 | Change | `convert(amount, to_currency)` returns float     | `convert(money: Money, to)` returns `Money`                                                | No                           |
| G12 | Rename | `PaymentError`                                   | `PayError`                                                                                 | Yes                          |

Unchanged in both: `reset()`, `withdraw(account_id, amount)`, `RATES`.
