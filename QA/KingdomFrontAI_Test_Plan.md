# Kingdom Front AI – Test Plan

**Author:** Salem Alshaghdali  
**Version:** 2.1 – Added Selected Pytest Automation  
**Date:** 22 August 2026  
**Application:** Kingdom Front AI – Python CLI Travel Assistant

## 1. Objective

Test the important beginner-level behaviours of Kingdom Front AI: installation, command-line input, user-profile validation, API error handling, local recommendation data, and basic planner logic. Add a small repeatable `pytest` suite for selected planner-stage scenarios that do not require paid API access.

The assignment does not require a paid OpenAI API key. Therefore, tests that require a successful LLM response will be marked **Blocked** when API quota is unavailable. Components that do not need the API will be tested directly through Python.

## 2. Scope

### In Scope

- Project installation and basic CLI startup.
- README setup instructions.
- Empty, spaces-only, and missing command-line query validation.
- User-profile updates and basic input validation.
- Missing, invalid, and unavailable OpenAI API access.
- Planner stage classification component.
- Automated `pytest` checks for the `local`, `travel`, and `family` planner stages.
- Loading activities from the local CSV dataset and handling a missing dataset file.
- Basic privacy check of stored profile and booking data.
- Docker availability and documented Docker setup.
- Arabic and English happy-path scenarios as test design; execute only if API access is available.

### Out of Scope

- Real bookings, payments, and live hotel availability.
- Load, performance, penetration, and formal security testing.
- Testing alternative LLM providers or modifying source code to bypass OpenAI.
- Full end-to-end planning when a paid API quota is unavailable.

## 3. Test Approach and Priorities

Testing is risk-based and mainly manual, with direct component testing and a small selected `pytest` automation suite.

| Priority | Areas | Reason |
|---|---|---|
| P0 | Application startup, input validation, API error handling | These issues can stop the application or expose an unfriendly crash to the user. |
| P1 | Profile updates, planner-stage rules, CSV data loading | These are core local functions that can be tested without OpenAI API access. |
| P2 | README, Docker, basic privacy review | Important for a new user and deployment readiness, but not the main functional flow. |

### Test Types

- Manual CLI testing.
- Static review of README and source code.
- Component-level tests by importing Python modules directly.
- Automated component tests with `pytest` for selected planner-stage scenarios.
- Positive and negative input validation tests.

## 4. Test Environment

- Windows PowerShell.
- Python 3.11.9.
- Pytest 9.1.1.
- Virtual environment (`.venv`) activated.
- Dependencies installed using `pip install -r requirements.txt`.
- No paid OpenAI API quota available.
- Local activity dataset available under the project `data` folder.

## 5. Main Risks

- The application may crash when the OpenAI API key is missing, invalid, or out of quota.
- Invalid user-profile values may be accepted and later crash planner logic.
- Blank or spaces-only requests may be processed as valid requests.
- Arabic and English end-to-end flows cannot be verified without successful API access.
- README instructions may not allow a new user to install and run the project successfully.
- Stored profile and booking data may need a basic privacy review before release.

## 6. Entry and Exit Criteria

### Entry Criteria

- Repository, assignment brief, and README are available.
- Python and project dependencies are installed.

### Exit Criteria

- All simple P0 and P1 tests are executed.
- API-dependent tests are clearly marked Blocked if quota is unavailable.
- Every verified defect has a reproducible bug report and evidence.
- The selected automated planner-stage tests are executed and their results are documented.
- Test cases, bug reports, and a release recommendation are complete.

## 7. Deliverables

- Test Plan.
- Manual Test Cases with execution status.
- Bug Reports.
- Quality Summary and Release Recommendation.
- Evidence Checklist.
- Automated test file: `tests/test_planner_stage.py`.
- Pytest execution screenshot.
