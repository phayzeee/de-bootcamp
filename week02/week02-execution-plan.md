# WEEK 2 EXECUTION PLAN — pandas, APIs, Parquet
### 2.5 hrs/day · code-first · remediation baked into Mon–Wed · 4-Line Ritual mandatory

---

## Before Monday (10 min, not counted)

```bash
cd de-bootcamp && source .venv/bin/activate
pip install pandas pyarrow requests jupyterlab
pip freeze > requirements.txt
mkdir -p week02 dsa/arrays_hashing
touch dsa/ritual.md
```

**Use Jupyter this week, not .py files.** `jupyter lab` → work in `week02/dayN.ipynb`. pandas is an exploratory tool; running a whole script to see one DataFrame is torture. Notebooks give you Kotlin-REPL-style feedback. Commit the `.ipynb` files — recruiters actually read them.

**`dsa/ritual.md` is a required deliverable now.** One entry per problem, before you write code. No ritual entry = the problem doesn't count, even if it's Accepted.

---

## Daily shape (2h30)

| Time | Block |
|---|---|
| 0:00–0:45 | **Remediation** (Mon–Wed) / **DSA** (Thu–Sat) |
| 0:45–0:55 | Break |
| 0:55–2:15 | **Build** — pandas, in a notebook |
| 2:15–2:30 | Commit + push + `stuck.md` |

Mon–Wed the remediation *replaces* new DSA. You are not doing both. Build block is untouched.

---

## The one mental model for all of pandas

You already know this. It's Kotlin collections, on a table:

| Kotlin | pandas |
|---|---|
| `list.filter { it.amount > 100 }` | `df[df.amount > 100]` |
| `list.map { it.copy(x = it.x * 2) }` | `df["x"] = df["x"] * 2` |
| `list.groupBy { it.city }` | `df.groupby("city")` |
| `.groupBy{}.mapValues{ it.value.sumOf{...} }` | `.groupby("city")["amt"].sum()` |
| `list.sortedByDescending { it.amt }` | `df.sort_values("amt", ascending=False)` |
| `listA.zip(listB)` on a key | `dfA.merge(dfB, on="id")` |
| `list.distinct()` | `df.drop_duplicates()` |

The genuinely new idea: **vectorization.** You don't loop. `df["amt"] * 1.15` applies to a million rows at once in C. **If you write `for i in range(len(df))` in pandas, you have made a mistake** — same rule as Week 1's index loops, but here it's also 100× slower.

---

# DAY 1 (Mon) — DataFrame basics on your own data

### Remediation (45 min)
1. **A2 `running_avg` from a blank file.** Generator, running mean. `[2,4,6]` → `[2.0, 3.0, 4.0]`, `[]` → `[]`. 4-Line Ritual first. Save as `week01/redo/running_avg.py`.
2. **LC 219 blank re-solve** — 15 min. You had the brute force yourself; this should land.

### Build (80 min) — `week02/day1_basics.ipynb`
Use **your own Week 1 data**: `expenses.csv` and your parsed logcat.

```python
import pandas as pd
df = pd.read_csv("../week01/day6_tracker/expenses.csv")
```
Work through, one cell each, printing every result:
1. `df.head()`, `df.shape`, `df.info()`, `df.dtypes`, `df.describe()`
2. `df["amount"]` (Series) vs `df[["amount", "category"]]` (DataFrame) — note the difference in a markdown cell
3. `df.loc[0]` vs `df.iloc[0]` — label vs position. Write one line on when each matters.
4. Boolean masks: `df[df["amount"] > 500]`, `df[(df["amount"] > 500) & (df["category"] == "food")]` — **`&` and `|`, never `and`/`or`, and always parenthesize.**
5. `df["amount"].sum() / .mean() / .max()`, `df["category"].value_counts()`, `df["category"].unique()`, `df["category"].nunique()`
6. New column: `df["amount_sar"] = df["amount"] * 0.0134`
7. `pd.to_datetime(df["date"])`, then `df["month"] = df["date"].dt.strftime("%Y-%m")`
8. Load your logcat into a DataFrame: reuse `parse_file()` from Week 1 → `pd.DataFrame([vars(r) for r in records])`. Then `df["level"].value_counts()` — **the same answer your `Counter` gave, in one line.** Note that in a markdown cell.

### Checkpoint
1. `df["col"]` vs `df[["col"]]` — what type does each return?
2. Why does `df[df.a > 1 and df.b > 2]` crash, and what's the fix?
3. `.loc` vs `.iloc` in one sentence each.
4. `value_counts()` — which Week 1 tool does it replace?

### Ship
`day1_basics.ipynb`, `week01/redo/running_avg.py`, LC 219 file, ritual entries. Commit `w02d1: pandas basics; remediation A2 + LC219`.

---

# DAY 2 (Tue) — groupby, agg, apply

### Remediation (45 min)
1. **LC 205 · Isomorphic Strings** — the zero. Full ritual, out loud. Free hint again: `foo`/`bar` fails in a direction one dict can't catch. Find that direction *before* writing code.
2. **LC 242 Valid Anagram blank** — 5 min confidence rep.

### Build (80 min) — `week02/day2_groupby.ipynb`
This is the most interview-relevant pandas topic. It is `GROUP BY` in SQL, which is Week 3.

1. `df.groupby("category")["amount"].sum()` — then `.mean()`, `.count()`, `.max()`
2. Multiple aggregations at once:
   ```python
   df.groupby("category").agg(
       total=("amount", "sum"),
       avg=("amount", "mean"),
       n=("amount", "count"),
   ).sort_values("total", ascending=False)
   ```
   **Memorize this named-agg form.** It's the one you'll write for the next 10 weeks.
3. Multi-key: `df.groupby(["month", "category"])["amount"].sum()` — then `.reset_index()` and note what changed.
4. `.unstack()` on the multi-key result → a pivot table. Also do it directly: `df.pivot_table(index="month", columns="category", values="amount", aggfunc="sum", fill_value=0)`
5. `apply` vs vectorized — write both:
   ```python
   df["big"] = df["amount"].apply(lambda x: "yes" if x > 500 else "no")   # slow
   df["big"] = (df["amount"] > 500).map({True: "yes", False: "no"})        # fast
   ```
   Time both with `%%timeit` on a 100k-row frame (`pd.concat([df]*20000)`). Record the ratio in a markdown cell. **This number is an interview answer.**
6. On logcat: top 5 noisiest tags via `groupby("tag").size().sort_values(ascending=False).head(5)` — same answer as Week 1's `Counter.most_common(5)`.

### Checkpoint
1. Write the named-agg `.agg()` form from memory.
2. What does `.reset_index()` do after a groupby, and why do you almost always want it?
3. `.size()` vs `.count()` on a groupby — one difference.
4. Why is `.apply()` slower than a vectorized op? What is it actually doing?

### Ship
`day2_groupby.ipynb`, LC 205 + LC 242 files, ritual entries. Commit `w02d2: groupby + agg; remediation LC205`.

---

# DAY 3 (Wed) — merge, join, missing data

### Remediation (45 min)
1. **Part B behavior proof** — your weak spot was "same behavior preserved," not bug-finding. Take your rewritten inventory file and for each of the 4 functions write **one assert** proving old and new behave identically on a real input. E.g. `assert add_item("pen", 2) == [{"name": "pen", "qty": 2}]`. Save as `week01/redo/part_b_behavior.py`.
2. **LC 1 Two Sum + LC 268 Missing Number**, blank, 5 min each. Speed reps.

### Build (80 min) — `week02/day3_merge.ipynb`
Joins are ~half of every SQL interview. Learning them in pandas first makes Week 3 far easier.

Build a second small DataFrame by hand:
```python
budgets = pd.DataFrame({
    "category": ["food", "transport", "bills", "gym"],
    "monthly_budget": [8000, 3000, 12000, 2500],
})
```
1. All four joins, and **print the row count of each** — the counts are the whole lesson:
   `df.merge(budgets, on="category", how="inner" / "left" / "right" / "outer")`
2. `how="left"` produces `NaN` for a category with no budget. Handle it: `.fillna(0)`, `.isna().sum()`, `.dropna(subset=[...])`
3. `indicator=True` → shows `left_only` / `both` / `right_only`. **This is how you debug a join that silently lost rows** — the single most common real-world data bug.
4. Deliberately break it: duplicate a category row in `budgets`, re-merge, watch the row count *inflate*. Write one markdown line: why a many-to-many join explodes.
5. `pd.concat([df1, df2])` (stacking rows) vs merge (matching keys) — one line on the difference.
6. `df.merge(budgets, on="category", how="left").groupby("category").agg(spent=("amount","sum"), budget=("monthly_budget","first")).assign(over=lambda d: d.spent > d.budget)`

### Checkpoint
1. Four join types — which rows does each keep?
2. Your row count went *up* after a merge. What happened?
3. What does `indicator=True` give you and when do you reach for it?
4. `NaN` — what is its dtype, and why does `NaN == NaN` return False?

### Ship
`day3_merge.ipynb`, `part_b_behavior.py`, 2 DSA files. Commit `w02d3: joins + missing data; remediation Part B`.
**Remediation ends here.** Thursday you're back on a normal footing.

---

# DAY 4 (Thu) — APIs with `requests`

### DSA (45 min) — ritual mandatory
1. **LC 66 · Plus One** — 20 min. Ritual first; the edge case (`[9,9,9]`) *is* the problem.
2. **LC 1512 · Number of Good Pairs** — 20 min. Brute force first, then the counting trick.

### Build (80 min) — `week02/day4_api.ipynb`
**Use Open-Meteo, not OpenWeather — no API key, no signup, no blocker.**

```python
import requests
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 24.86, "longitude": 67.01,      # Karachi
    "hourly": "temperature_2m,relative_humidity_2m",
    "timezone": "Asia/Karachi",
}
r = requests.get(url, params=params, timeout=10)
r.raise_for_status()
data = r.json()
```
1. Inspect: `r.status_code`, `r.headers["content-type"]`, `list(data.keys())`, `data["hourly"].keys()`
2. `data["hourly"]` → DataFrame directly: `pd.DataFrame(data["hourly"])`. Convert `time` with `pd.to_datetime`.
3. Loop **5 cities** — Karachi (24.86, 67.01), Lahore (31.55, 74.34), Riyadh (24.71, 46.68), Dubai (25.20, 55.27), Dammam (26.43, 50.10). Each response → DataFrame → add a `city` column → collect in a list → `pd.concat(frames, ignore_index=True)`.
4. Wrap the fetch in `try/except requests.RequestException` — a pipeline must survive one dead endpoint. Print a warning, skip that city, continue. (Week 1's "one bad row must not kill the run," now at API level.)
5. `time.sleep(1)` between calls, and one markdown line on why (rate limits, being a good citizen).
6. Analyze: `combined.groupby("city")["temperature_2m"].agg(["min", "max", "mean"]).round(1)` — hottest city right now.
7. Nested JSON drill: `pd.json_normalize` on this hand-made structure, then explain in one line what it did to the column names:
   ```python
   nested = [{"id": 1, "user": {"name": "Sara", "addr": {"city": "Karachi"}}}]
   ```

### Checkpoint
1. `raise_for_status()` — what does it do and why not check `status_code` manually?
2. Why `params={...}` instead of building the URL string yourself?
3. Your pipeline hits 5 endpoints and #3 times out. What should happen?
4. What does `json_normalize` do to nested keys?

### Ship
`day4_api.ipynb`, `raw_weather.json` saved to disk, 2 DSA files + ritual. Commit `w02d4: open-meteo ingestion; LC 66/1512`.

---

# DAY 5 (Fri) — File formats: CSV vs JSON vs Parquet

This is the day that's *actually* Data Engineering. Everything before it was Python.

### DSA (45 min)
1. **LC 1365 · How Many Numbers Are Smaller Than the Current Number** — 20 min. Brute force O(n²) first (it passes!), then think about counting.
2. **LC 1436 · Destination City** — 20 min. Pure set/dict reasoning, very DE-flavoured.

### Build (80 min) — `week02/day5_formats.ipynb`
Use the combined 5-city weather frame. Make it big: `big = pd.concat([combined] * 50, ignore_index=True)`

1. Write the same data three ways and **measure**:
   ```python
   big.to_csv("weather.csv", index=False)
   big.to_json("weather.json", orient="records")
   big.to_parquet("weather.parquet")            # needs pyarrow
   big.to_parquet("weather_snappy.parquet", compression="snappy")
   ```
   Build a comparison table with `os.path.getsize(...)/1024` and `%%timeit` on each read. Columns: format | size KB | write time | read time.
2. **The dtype lesson** — the reason Parquet exists:
   ```python
   pd.read_csv("weather.csv").dtypes      # your datetime came back as `object`. It's a string again.
   pd.read_parquet("weather.parquet").dtypes   # still datetime64. Schema survived.
   ```
   Write 3 lines in markdown on why this matters at scale.
3. Column pruning — the columnar superpower:
   ```python
   pd.read_parquet("weather.parquet", columns=["city", "temperature_2m"])
   ```
   Time it against reading all columns. CSV **cannot** do this — it must read every byte.
4. Partitioned write, your first taste of a data lake layout:
   ```python
   big.to_parquet("weather_partitioned/", partition_by=None, index=False)  # then:
   big.to_parquet("weather_lake/", index=False, partition_cols=["city"])
   ```
   Then `ls -R weather_lake/` — see the `city=Karachi/` folders. **This is exactly the medallion/bronze layout from Week 7.**
5. `chunksize` streaming: `for chunk in pd.read_csv("weather.csv", chunksize=1000):` — count rows without loading the file. Connect it in one markdown line to Week 1 generators.

### Checkpoint
1. Three concrete reasons Parquet beats CSV for analytics.
2. Row-oriented vs columnar storage — one sentence.
3. What does CSV lose that Parquet keeps?
4. When would you still choose CSV?
5. What does `partition_cols=["city"]` create on disk, and how does that speed up a query filtered on city?

### Ship
`day5_formats.ipynb` with the size/speed comparison table filled in, `weather_lake/` directory, 2 DSA files + ritual. Commit `w02d5: parquet vs csv benchmark; LC 1365/1436`.

---

# DAY 6 (Sat) — Mini ETL Pipeline (first portfolio piece)

| Time | Block |
|---|---|
| 0:00–0:20 | Cleanup: top 2 items from `stuck.md` |
| 0:20–1:50 | Build |
| 1:50–2:00 | Break |
| 2:00–2:45 | DSA |
| 2:45–3:00 | README + push |

### Build — `week02/day6_pipeline/weather_etl.py`
A real script, not a notebook. **Three functions, clean separation — this is the E, T, L.**

```python
def extract(cities: dict[str, tuple[float, float]]) -> list[dict]:
    """Fetch raw JSON per city. Survives individual failures. Returns raw payloads."""

def transform(raw: list[dict]) -> pd.DataFrame:
    """Flatten to one tidy row per city per hour.
    Columns: city, ts (datetime), temp_c, humidity, ingested_at (datetime.now())
    Drops nulls, sorts by city then ts."""

def load(df: pd.DataFrame, out_dir: str = "data/") -> None:
    """Write partitioned parquet: data/weather/city=Karachi/... 
    Also write data/summary.csv: city, min, max, mean temp."""
```
Plus `main()` printing a run report:
```
Extracted 5/5 cities
Transformed 840 rows (12 nulls dropped)
Loaded -> data/weather/ (5 partitions, 214 KB)

city      min    max   mean
Dammam   31.2   44.1   37.8
Dubai    30.9   42.0   36.4
...
```
Requirements: type hints on all three · `ingested_at` column (**every DE table has one — interviewers notice its absence**) · re-running must not duplicate data (overwrite the partition) · `README.md` in `day6_pipeline/` with a 4-line ASCII architecture diagram: `Open-Meteo API → extract() → transform() → Parquet lake → summary.csv`.

### DSA (45 min)
1. **LC 350 · Intersection of Two Arrays II** — 20 min. The "II" changes everything vs LC 349; `Counter` intersection.
2. **LC 49 · Group Anagrams** — 25 min. **Your first Medium.** Deliberate: it's the gentlest one, and it's literally your Week 1 `defaultdict` grouping + `Counter` work combined. Ritual first. Hint: what do all anagrams share that you can use as a dict key? If 25 min pass, editorial → close → blank re-solve tomorrow.

### Ship
Pipeline files + `data/` output + README with diagram. Commit `w02d6: weather ETL pipeline; LC 350/49`.

---

# DAY 7 (Sun) — 60-minute test

Closed book. **GPT closed. Phone away.** Pass = 65/100 (bar stays where it is).

### Part A — pandas, 25 min — `week02/mock/part_a.ipynb`
Given this frame:
```python
sales = pd.DataFrame({
    "order_id": [1, 2, 3, 4, 5, 6],
    "city":     ["Karachi", "Riyadh", "Karachi", "Dubai", "Riyadh", "Karachi"],
    "category": ["food", "tech", "food", "tech", "food", "bills"],
    "amount":   [500, 1200, 300, 900, 450, 2000],
})
```
1. Total and average `amount` per city, sorted by total descending, using the named-agg form. **(10 pts)**
2. Add column `is_large` = True where amount > 800, vectorized — no `.apply()`. **(5 pts)**
3. Pivot: rows = city, columns = category, values = sum of amount, missing = 0. **(10 pts)**
4. Given `cities = pd.DataFrame({"city": ["Karachi", "Riyadh", "Jeddah"], "country": ["PK", "SA", "SA"]})` — left-join it onto `sales`, then report how many rows have a null country and which city they belong to. **(10 pts)**

### Part B — debug, 15 min — `week02/mock/part_b.py`
Five problems. List them in a comment block, then rewrite clean.
```python
import pandas as pd, requests

def get_data(url):
    r = requests.get(url)
    return r.json()

def clean(df):
    for i in range(len(df)):
        df.loc[i, "amount"] = df.loc[i, "amount"] * 1.15
    return df

def big_spenders(df):
    return df[df.amount > 1000 and df.city == "Riyadh"]

def save(df):
    df.to_csv("out.csv")
```

### Part C — DSA, 20 min — both unseen
1. **LC 1207 · Unique Number of Occurrences**
2. **LC 599 · Minimum Index Sum of Two Lists**
**Ritual entries required for both** — 5 of the 30 points are for the ritual, not the code.

### Grading (100)
| Section | Pts |
|---|---|
| A (4 tasks) | 35 |
| B — 3 per problem found (15) + 20 clean rewrite that preserves behavior | 35 |
| C — 12.5 per problem accepted + 5 for ritual entries | 30 |

<details>
<summary>Part B key — open after finishing</summary>

1. No `timeout=` and no `raise_for_status()` — hangs forever, and parses error pages as JSON.
2. `for i in range(len(df))` — replace with `df["amount"] = df["amount"] * 1.15`. Vectorize.
3. `clean()` mutates the caller's DataFrame in place — return a copy (`df = df.copy()`), or document it loudly.
4. `and` between two Series → ValueError. Use `&` with parentheses: `df[(df.amount > 1000) & (df.city == "Riyadh")]`.
5. `to_csv` without `index=False` — writes a junk unnamed index column that poisons every downstream read. Also: hardcoded path.
</details>

**After grading:** send me your scores + Part B answers, and say **"Week 2 recap"** for the topic summary.

---

## Week 2 problem index (10 problems)

| Day | Problems |
|---|---|
| Mon | *(remediation)* A2 blank · LC 219 blank |
| Tue | *(remediation)* LC 205 · LC 242 blank |
| Wed | *(remediation)* Part B behavior · LC 1 + 268 blank |
| Thu | 66 Plus One · 1512 Good Pairs |
| Fri | 1365 Smaller Numbers · 1436 Destination City |
| Sat | 350 Intersection II · **49 Group Anagrams (first Medium)** |
| Sun | 1207 Unique Occurrences · 599 Min Index Sum |

---

## The one thing that matters this week

**Every single problem gets a `ritual.md` entry before you write code.** IN / OUT / EXAMPLE / EDGE, in your own words.

Last week's failure had one root cause and it wasn't Python. Fix the ritual and the scores follow. If you only do one thing from this document, do that.

Week 3 is SQL — and everything you learn in Tuesday's `groupby` and Wednesday's `merge` is the same thing with different syntax. You're already building it.
