# Kingdom Front AI – Test Cases and Execution Results

**Author:** Salem Alshaghdali  
**Version:** 4.0 – Added Selected Pytest Automation  
**Application:** Kingdom Front AI – Python CLI Travel Assistant

## Status Definitions

- **Passed:** Actual result matched the expected result.
- **Failed:** Actual result did not match the expected result.
- **Blocked:** The test could not continue because of an external limitation, such as unavailable API quota.
- **Not Run:** The test has not yet been executed.

## Test Cases

### TC-001 — Install dependencies and start the application

- **Priority:** P0 | **Severity:** Major
- **Preconditions:** Python is installed and `.venv` is activated.
- **Steps:**
  1. Run `pip install -r requirements.txt`.
  2. Run `python src/orchestrator.py --query "أريد رحلة في جدة"`.
- **Expected Result:** Dependencies install without errors and the application starts without an import error.
- **Actual Result:** Dependencies installed successfully and the application started.
- **Status:** Passed

### TC-002 — Follow README setup instructions

- **Priority:** P2 | **Severity:** Major | **Type:** Static Finding
- **Steps:** Read the README and follow only its documented setup steps.
- **Expected Result:** README explains dependency installation, virtual environment setup, API-key configuration, and the run command.
- **Actual Result:** README provides clone and run commands but does not document dependency installation, virtual environment setup, or `OPENAI_API_KEY` configuration.
- **Status:** Failed

### TC-003 — Start without `--query`

- **Priority:** P0 | **Severity:** Minor
- **Steps:** Run `python src/orchestrator.py`.
- **Expected Result:** A clear usage message explains that `--query` is required, without a Python traceback.
- **Actual Result:** The CLI showed its usage message and stated that `--query` is required.
- **Status:** Passed

### TC-004 — Reject an empty query

- **Priority:** P0 | **Severity:** Major
- **Steps:** Run `python src/orchestrator.py --query ""`.
- **Expected Result:** The query is rejected before profile prompts or an API call.
- **Actual Result:** The CLI rejected the empty query.
- **Status:** Passed

### TC-005 — Reject a spaces-only query

- **Priority:** P0 | **Severity:** Major
- **Steps:** Run `python src/orchestrator.py --query "   "`.
- **Expected Result:** The query is rejected before profile prompts or an API call.
- **Actual Result:** The application accepted the spaces-only query and started profile prompts.
- **Status:** Failed

### TC-006 — Save a valid profile update

- **Priority:** P1 | **Severity:** Major
- **Steps:**
  1. Start the application with a normal query.
  2. Choose `y` to edit the profile.
  3. Change available days from `2` to `3`.
  4. Restart the application and review the saved profile value.
- **Expected Result:** Available days changes to `3` and remains saved after restart.
- **Actual Result:** The profile value was saved and displayed correctly after restart.
- **Status:** Passed

### TC-007 — Validate a `y/n` profile answer

- **Priority:** P0 | **Severity:** Minor
- **Steps:** At a `Change it? (y/n)` prompt, enter `2`.
- **Expected Result:** The application rejects `2` and asks again for `y` or `n`.
- **Actual Result:** The application accepted the invalid answer and continued.
- **Status:** Failed

### TC-008 — Validate a numeric profile field

- **Priority:** P0 | **Severity:** Major
- **Steps:** Choose a numeric profile field such as available days and enter `abc`.
- **Expected Result:** The application rejects the value, displays a clear error, and does not save it.
- **Actual Result:** The application accepted `abc` without validation or an error message.
- **Status:** Failed

### TC-009 — Handle a missing API key

- **Priority:** P0 | **Severity:** Major
- **Steps:** Remove the API key from the test environment and run a normal query.
- **Expected Result:** A clear missing-credentials message appears without a traceback.
- **Actual Result:** The application displayed: `Missing credentials, please pass an API key`.
- **Status:** Passed

### TC-010 — Handle an invalid API key

- **Priority:** P0 | **Severity:** Major
- **Steps:** Use `0000` as a temporary API key and run a normal query.
- **Expected Result:** A clear invalid-key message appears without exposing sensitive data.
- **Actual Result:** The application displayed: `Incorrect API key provided`.
- **Status:** Passed

### TC-011 — Handle unavailable API quota

- **Priority:** P0 | **Severity:** Major
- **Steps:** Use a valid key with no available API quota and run a normal query.
- **Expected Result:** A user-friendly quota message appears without a Python traceback.
- **Actual Result:** The application displayed `429 insufficient_quota` with a full Python traceback.
- **Status:** Failed

### TC-012 — Classify valid planning stages directly

- **Priority:** P1 | **Severity:** Major | **Type:** Component Test
- **Steps:** Import `PlannerStageClassifier` and pass these valid contexts:
  - Riyadh, one day.
  - Jeddah, two days.
  - Riyadh, two days, has kids.
  - Riyadh, two days, intent `visiting friends`.
- **Expected Result:** The returned stages are `local`, `travel`, `family`, and `friends` respectively.
- **Actual Result:** The component returned all four expected stages during direct testing. Pytest automation was added for `local`, `travel`, and `family`; all three automated tests passed. The `friends` scenario remains directly verified but is not yet automated.
- **Status:** Passed

### TC-013 — Handle non-numeric days in planner-stage component

- **Priority:** P0 | **Severity:** Major | **Type:** Component Test
- **Steps:** Import `PlannerStageClassifier`, pass `available_days: "abc"`, then call `detect_stage()`.
- **Expected Result:** The component rejects invalid data safely without crashing.
- **Actual Result:** The component crashed with `ValueError: could not convert string to float: 'abc'`.
- **Status:** Failed

### TC-014 — Load activities from the local CSV file

- **Priority:** P1 | **Severity:** Major | **Type:** Component Test
- **Steps:** Import `load_data()` from `recommendation_agent.py` and call it directly.
- **Expected Result:** The CSV loads records without an error.
- **Actual Result:** The component loaded 81 activity records; the first record was Boulevard Riyadh City in Riyadh.
- **Status:** Passed

### TC-015 — Handle a missing activities dataset file

- **Priority:** P0 | **Severity:** Major | **Type:** Component Test
- **Steps:** Set `recommendation_agent.DATA_PATH` to a non-existent CSV path, then call `load_data()`.
- **Expected Result:** The component raises a clear `FileNotFoundError` that identifies the missing dataset path.
- **Actual Result:** The component raised `FileNotFoundError: Dataset not found: data/missing_test.csv` and identified the missing path correctly.
- **Status:** Passed

### TC-016 — Start Docker Compose

- **Priority:** P2 | **Severity:** Major
- **Preconditions:** Docker Desktop installed.
- **Steps:** Run `docker --version`, then `docker compose up --build`.
- **Expected Result:** Docker builds and starts the documented services.
- **Actual Result:** Docker was not installed on the test machine.
- **Status:** Blocked

### TC-017 — Complete an Arabic travel request

- **Priority:** P1 | **Severity:** Major
- **Test Data:** `أريد خطة عائلية لمدة يومين في جدة بميزانية 1000 ريال`
- **Steps:** Run the query and continue to the final plan.
- **Expected Result:** The application understands the request and produces a suitable plan without crashing.
- **Actual Result:** Could not reach the plan because the test environment has no available API quota.
- **Status:** Blocked

### TC-018 — Complete an English travel request

- **Priority:** P1 | **Severity:** Major
- **Test Data:** `Plan a two-day family trip to Jeddah with a budget of 1000 SAR.`
- **Steps:** Run the query and continue to the final plan.
- **Expected Result:** The application understands the request and produces a suitable plan without crashing.
- **Actual Result:** Could not reach the plan because the test environment has no available API quota.
- **Status:** Blocked

### TC-019 — Basic privacy review of locally stored JSON data

- **Priority:** P2 | **Severity:** Major
- **Steps:** Scan `user_profile.json`, `bookings_log.json`, and `reflection_memory.json` for common secret patterns: API keys, tokens, and passwords.
- **Expected Result:** No obvious API key, token, or password is stored in the local JSON data files.
- **Actual Result:** The scan returned no matching results.
- **Status:** Passed

## Execution Summary

| Status | Count |
|---|---:|
| Passed | 10 |
| Failed | 6 |
| Blocked | 3 |
| Not Run | 0 |
| **Total** | **19** |

## Automation Execution Summary

The following automated component tests cover three valid scenarios from TC-012. They are recorded separately and are **not** added to the 19-test total above, which prevents double-counting the same coverage.

- **Framework:** Pytest 9.1.1
- **Test file:** `tests/test_planner_stage.py`
- **Run command:** `python -m pytest tests/test_planner_stage.py -v`

| Automated Test | Scenario | Result |
|---|---|---|
| `test_local_stage` | Riyadh with one available day returns `local`. | Passed |
| `test_travel_stage` | Jeddah with two available days returns `travel`. | Passed |
| `test_family_stage` | Riyadh with two days and children returns `family`. | Passed |
| **Total** | **3 automated tests** | **3 Passed, 0 Failed** |

The `friends` stage, invalid `available_days`, profile validation, CSV loading, and API error handling remain candidates for the next automation iteration.
