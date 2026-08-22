# Kingdom Front AI – Bug Reports

**Author:** Salem Alshaghdali  
**Date:** 22 August 2026  
**Application:** Kingdom Front AI

## BR-001 — README does not document required setup steps

- **Type:** Static Finding
- **Severity:** Major

### Steps to Reproduce

1. Open `README.md`.
2. Follow the documented clone and run steps as a new user.

### Expected Result

A new user can install and run the project using the README. It should explain dependency installation, virtual environment setup, API-key configuration, and the run command.

### Actual Result

The README provides clone and run commands but does not explain `pip install -r requirements.txt`, virtual environment setup, or `OPENAI_API_KEY` configuration.

### Evidence

in evednce file 

---

## BR-002 — Spaces-only query is accepted as a valid request

- **Severity:** Major

### Steps to Reproduce

1. Run:

```powershell
python src/orchestrator.py --query "   "
```

2. Observe the next application screen.

### Expected Result

The application rejects a query containing only spaces before profile prompts or API processing.

### Actual Result

The application accepted the spaces-only query and started the profile prompts.

### Evidence

in evednce file 
---

## BR-003 — Profile change prompt accepts an invalid `y/n` value

- **Severity:** Minor

### Steps to Reproduce

1. Start the application with a normal query.
2. At `Change it? (y/n)`, enter `2`.

### Expected Result

The application rejects the value and asks the user to enter only `y` or `n`.

### Actual Result

The application accepted `2` and continued to the next prompt.

### Evidence

in evednce file 

---

## BR-004 — Non-numeric available days can cause the planner-stage component to crash

- **Severity:** Major

### Steps to Reproduce

1. Import `PlannerStageClassifier` from `src/planner_stage.py`.
2. Pass this context:

```python
{'city': 'riyadh', 'available_days': 'abc'}
```

3. Call `detect_stage()`.

### Expected Result

The application rejects invalid numeric data or handles it safely without crashing.

### Actual Result

The component raised:

```text
ValueError: could not convert string to float: 'abc'
```

The main profile flow also accepted `abc` in a numeric field without validation.

### Evidence

in evednce file 

---

## BR-005 — API quota failure exposes a full Python traceback

- **Severity:** Major

### Steps to Reproduce

1. Configure a valid API key for an account without available API quota.
2. Run a normal travel query.

### Expected Result

The application displays a clear, user-friendly message that API quota is unavailable and exits safely.

### Actual Result

The application displayed `429 insufficient_quota` followed by a full Python traceback.

### Evidence

in evednce file 
