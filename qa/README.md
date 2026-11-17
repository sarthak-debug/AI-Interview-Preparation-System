# Prepare.AI — QA Suite (LLM Evaluation + Test Automation)

Automated quality checks for the Prepare.AI interview app: the FastAPI backend, the React UI,
and the **Gemini LLM** that scores candidate answers.

| Layer | Tool | What it checks | Needs API key? |
|---|---|---|---|
| Unit tests | **Pytest** | Skill extraction, question bank, PDF parsing, offline fallback scorer | No |
| API tests | **Pytest + FastAPI TestClient** | `/upload`, `/evaluate`, error handling, fallback when Gemini fails (Gemini is mocked) | No |
| Contract tests | **Swagger / OpenAPI** | The published API spec matches what the frontend uses | No |
| API collection | **Postman / Newman** | Status codes, response fields, `Score: x/10` format, validation errors | No |
| UI tests | **Playwright** | Full user flow in a real browser: upload → questions → answer → score | No (API mocked) |
| LLM evaluation | **Golden dataset (24 cases)** | Does Gemini give strong / partial / wrong answers a fair score? | Yes |
| LLM feedback quality | **DeepEval G-Eval** (Gemini as judge) | Is the feedback grounded in the answer, not generic or invented? | Yes |
| AI safety | **Guardrail tests (6 attacks)** | Prompt injection, fake system messages, role-play jailbreaks, off-topic answers | Yes |
| CI/CD | **GitHub Actions** | Runs everything on every push; LLM evals weekly / on demand | Secret |

The suite already found **5 real bugs**, including a path-traversal security issue — see [BUGS.md](BUGS.md).

---

## How to run (Windows, step by step)

Open a terminal in the project folder, then:

```bash
cd qa
python -m venv .venv
.venv\Scripts\activate            # Mac/Linux: source .venv/bin/activate
pip install -r requirements-qa.txt
```

### 1. Unit + API tests (free, offline, ~2 seconds)

```bash
pytest
```

You should see `31 passed, 5 xfailed`. The 5 "xfailed" are the known bugs in BUGS.md.

### 2. Postman API tests

Start the backend in one terminal:

```bash
cd backend
uvicorn main:app --port 8000
```

Then either **import `postman/PrepareAI.postman_collection.json` into the Postman app and click Run**,
or from another terminal:

```bash
cd qa/postman
npx newman run PrepareAI.postman_collection.json
```

You can also open **http://127.0.0.1:8000/docs** — that is the Swagger UI FastAPI generates.

### 3. Playwright UI tests

Start the frontend (`cd frontend && npm install && npm run dev`), then:

```bash
cd qa
playwright install chromium        # first time only
pytest -m e2e tests/e2e            # add --headed to watch the browser
```

### 4. LLM evaluation (uses your Gemini API key)

```bash
set GEMINI_API_KEY=your_key_here        # Mac/Linux: export GEMINI_API_KEY=your_key_here
python tests/llm_eval/run_eval_report.py --repeats 2
pytest -m llm tests/llm_eval
```

`run_eval_report.py` writes **`reports/llm_eval_report.md`** with:

- **Scoring accuracy** – % of golden answers scored inside the expected band
- **Format compliance** – % of replies the frontend can parse (`Score: x/10`, Strengths, Improvements)
- **Prompt-injection resistance** – % of manipulation attempts that did *not* raise the score
- **Silent failures** – % of calls where Gemini failed and the app quietly used the fallback scorer
- **Score spread** – how much the score changes when the same answer is graded twice (non-determinism)
- **Average latency**

Free-tier keys are rate-limited; the script waits 4 s between calls (change with `EVAL_DELAY`).

### 5. CI on GitHub

The workflow in `.github/workflows/qa.yml` runs automatically on every push.
For the LLM job, add your key once: **GitHub repo → Settings → Secrets and variables → Actions →
New repository secret → `GEMINI_API_KEY`**, then run it from the **Actions** tab ("Run workflow").

---

## Folder layout

```
qa/
├── tests/
│   ├── unit/        Pytest unit tests
│   ├── api/         FastAPI endpoint + OpenAPI contract tests (Gemini mocked)
│   ├── e2e/         Playwright browser tests
│   └── llm_eval/    golden_dataset.json, guardrail_cases.json, DeepEval tests, report script
├── postman/         Postman collection + sample resume
├── reports/         generated reports
└── BUGS.md          bugs found by the suite
```
