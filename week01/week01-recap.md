# WEEK 1 RECAP — Python Core for a JVM Dev
### Save as `week01/recap.md`. Read this before Sunday's mock, and again before any interview.

Interview relevance: 🔥 = they will ask · ⚙️ = you'll use it daily on the job · 💤 = nice to know

---

## 1. Kotlin → Python mental model 🔥

| Kotlin | Python | Watch out |
|---|---|---|
| `val x: String? = null` | `x: str \| None = None` | **No compiler null safety.** Hints are documentation, not enforcement. Only `mypy` checks them. |
| `x?.length ?: 0` | `len(x) if x else 0` | No `?.` or `?:` operators at all |
| `when (c) { ... }` | `match c: case ...` | Or just `if/elif` — nobody will fault you |
| `data class User(...)` | `@dataclass class User:` | Gives you `__init__`, `__repr__`, `__eq__` free |
| `object Config` | module-level constants in `config.py` | A module *is* a singleton |
| `fun String.initials()` | plain `def initials(s: str)` | **No extension functions.** This is the biggest daily annoyance. |
| `listOf(...).filter{}.map{}` | `[f(x) for x in xs if cond]` | Comprehension, not chained calls |
| `companion object` | `@staticmethod` / `@classmethod` | Rarely needed |

**Truthiness** — falsy values: `False`, `None`, `0`, `0.0`, `""`, `[]`, `{}`, `set()`. So `if items:` means "non-empty list". Kotlin has no equivalent; this reads weird for a week, then becomes natural.

**`is` vs `==`** — `==` is value equality (Kotlin's `==`/`equals`). `is` is identity (Kotlin's `===`). **Always `x is None`, never `x == None`.** This is a classic code-review catch.

**The mutable default trap** 🔥 — the #1 Python gotcha, asked in real interviews:
```python
def add(item, bucket=[]):     # BUG: the list is created ONCE, at def time,
    bucket.append(item)       # and shared by every call
    return bucket

def add(item, bucket=None):   # FIX
    if bucket is None:
        bucket = []
```

---

## 2. Comprehensions ⚙️🔥
The single most "is he actually a Python dev" signal. Index loops mark you as a tourist.

```python
[x * x for x in nums if x % 2 == 0]         # list
{w: len(w) for w in words}                   # dict
{c for c in text if c.isalpha()}             # set
(x * x for x in nums)                        # generator — lazy, no list built
[y for row in matrix for y in row]           # flatten (loops read left→right, outer first)
```
**Never write** `for i in range(len(xs))`. Use `for x in xs`, or `for i, x in enumerate(xs, start=1)`, or `for a, b in zip(xs, ys)`.

Wrong tool when: you need side effects, or 3+ levels of nesting. Then a plain loop is more readable.

---

## 3. Collections — your DE workhorse ⚙️🔥

```python
from collections import Counter, defaultdict, deque

Counter("banana")                    # Counter({'a': 3, 'n': 2, 'b': 1})
Counter(words).most_common(3)        # [(word, count), ...] — sorted desc
Counter(a) == Counter(b)             # anagram check, O(n)

d = defaultdict(list)                # grouping — no key-exists check needed
for order in orders:
    d[order.city].append(order)

prices.get(name, 0)                  # safe read with fallback
deque(maxlen=100)                    # ring buffer — last-N without holding everything
```

**Sorting with keys** ⚙️
```python
sorted(items, key=lambda kv: (-kv[1], kv[0]))    # count desc, then name asc
sorted(rows, key=operator.itemgetter("city", "amount"))
```
`sorted(xs)` returns a new list · `xs.sort()` mutates and returns `None`.

**Order-preserving dedupe:** `list(dict.fromkeys(xs))` — dicts keep insertion order since Python 3.7.

**Complexity that matters:** `x in list` is O(n) · `x in set` / `x in dict` is O(1). Swapping a list for a set is 80% of "optimize this" answers.

---

## 4. Functions ⚙️

```python
def f(a, b=10, *args, key=None, **kwargs): ...
def load(path, *, strict=False): ...     # everything after * is keyword-only — use for boolean flags
f(*my_list, **my_dict)                    # unpacking at the call site
```
`*args` = varargs (Kotlin `vararg`) · `**kwargs` = a dict of named args (no Kotlin equivalent).

**Decorators** 💤 — a function that wraps a function; `@timed` literally means `f = timed(f)`. Kotlin equivalent: a higher-order `inline fun timed(block: () -> T)`. Know the concept, don't grind it. Decorator *factories* deliberately deferred.

---

## 5. Files, errors, formats ⚙️🔥

```python
with open(path, encoding="utf-8") as f:     # always `with` — auto-close, like Kotlin's `use`
    for line in f:                           # files iterate lazily, line by line
        ...

try:
    ...
except (ValueError, KeyError) as err:        # never bare `except:` — it eats Ctrl+C
    raise ParseError(f"line {n}") from err   # `from` keeps the original traceback
finally:
    ...                                      # else: runs only if NO exception fired
```

**EAFP vs LBYL** 🔥 — Python prefers *Easier to Ask Forgiveness than Permission* (`try/except`) over *Look Before You Leap* (`if exists`). LBYL still wins where a check is cheap and failure is expected (validating user input).

**In a data pipeline, one bad row must never kill the run.** Skip it, count it, log it. That mindset is the actual lesson of Days 4–5.

```python
csv.DictReader(f)          # each row is a dict — use this, not csv.reader
json.load(f) / json.dumps(obj)
Decimal("15.50")           # money. NEVER float — run `print(0.1 + 0.2)` once
Path("data") / "app.log"   # pathlib beats string concatenation
```

---

## 6. Generators ⚙️🔥 — the DE-critical one
Python's `Sequence`. Lazy, streamed, constant memory.

```python
def read_lines(path):
    with open(path) as f:
        for line in f:
            yield line.rstrip()      # emit one, pause, resume on next request
```
- Calling a generator function runs **none** of its body — it returns a generator object.
- **Single-use.** Iterate twice and the second pass is empty. (Kotlin `Sequence` can be re-iterated if built from a collection — the key difference.)
- `sum(x*x for x in xs)` builds no intermediate list. `sum([x*x for x in xs])` does.
- Terminal ops: `list()`, `sum()`, `for`, `itertools.islice(gen, 10)` ≈ `take(10)`.

**Why an interviewer cares:** a 50GB file doesn't fit in RAM. Generators are how you process it anyway. Expect "how would you handle a file larger than memory?" — the answer is streaming.

---

## 7. Tooling ⚙️

| Command | Purpose | Kotlin analogue |
|---|---|---|
| `python -m venv .venv` + `source .venv/bin/activate` | isolated deps | Gradle module scope |
| `pip install X` / `pip freeze > requirements.txt` | deps | `build.gradle` dependencies |
| `python -m pytest` | tests | JUnit |
| `ruff check .` | lint + format | ktlint/detekt |
| `mypy file.py` | type checking | the Kotlin compiler, but optional and opt-in |
| `if __name__ == "__main__":` | run-as-script guard | `fun main()` |

---

## 8. DSA patterns banked this week 🔥

| Pattern | Where it appeared | The insight |
|---|---|---|
| **Hash set for membership** | 217, 349, 268, 448 | O(n) list scan → O(1) set lookup |
| **Hash map complement** | 1 Two Sum | Store what you've *seen*; check for the complement **before** inserting, so `[3,3]` works |
| **Frequency counting** | 242, 383, 387, 169 | `Counter` in one line; O(n) beats `sorted()`'s O(n log n) |
| **XOR cancellation** | 136 | `a ^ a == 0`, `a ^ 0 == a` → XOR everything, pairs vanish, the loner survives. O(1) space |
| **Math identity** | 268 | `n*(n+1)//2 - sum(nums)`. Python ints don't overflow |
| **Prefix / running sum** | 1480, 724 | One pass keeping a running total. Pivot check: `left == total - left - nums[i]`. **This pattern comes back as SQL window functions in Week 4** |
| **Two-way mapping** | 205 (Sunday) | Isomorphic needs *two* dicts — one each direction |

**Interview reality check:** DE interviews are ~50% SQL, ~20% pipeline/warehouse concepts, ~20% easy-medium Python, ~10% behavioral. Every problem above is Easy, and Easy is the right ceiling right now.

---

## 9. Deliberately dropped from Week 1
Not failures — decisions. Don't go back for these:
`@retry` decorator factories · `compose()` · closure loop gotcha · `functools.reduce` · `argparse` sub-parsers · `frozen=True` dataclasses · O(1)-space sign-marking (LC 448) · Boyer–Moore voting (LC 169 — the dict version is fine) · async/await · classes and inheritance (you know OOP; Python's flavour can wait until you need it).

---

## 10. Self-check — can you do these cold?
1. Rewrite an index loop as a comprehension.
2. Group a list of dicts by one key. (Two ways: `defaultdict`, `setdefault`.)
3. Top 3 most frequent items in a list, ties broken alphabetically.
4. Read a file safely, skipping malformed lines, counting how many you skipped.
5. Write a generator and explain why it doesn't blow up on a huge file.
6. Spot all 6 bugs in Sunday's Part B file.
7. Solve Two Sum in one pass without looking.

Anything you can't do → that's Saturday's cleanup block, not a crisis.

---

**Next week:** pandas + APIs + Parquet. It's Kotlin collections operations on tables — `groupby` is `groupBy`, `merge` is a join. Your comprehension and `Counter` work this week transfers directly.
