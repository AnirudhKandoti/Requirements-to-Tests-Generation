#  Requirements-to-Tests Generator (T2T)

> **Automatically generate runnable test cases and traceability matrices directly from requirements and API specifications.**

---

##  Overview

Manual test authoring is slow and error-prone — every time a requirement changes, QA engineers must rewrite test scripts and update traceability sheets.  
**T2T** automates this entire process.

It reads:

- **Jira change requests** → what the user wants  
- **OpenAPI specifications** → how the API behaves  

and automatically generates:

-  **Gherkin scenarios** (`.feature` files)  
-  **Runnable pytest tests** (`.py` files)  
-  **Traceability matrix** (CSV + HTML)  

This cuts **manual test creation from hours to minutes** while maintaining full traceability from requirement → test → execution result.

---

##  Project Structure

t2t_requirements_to_tests_fixed2/

├── data/

│ ├── jira/

│ │ └── changes.json ← Jira requirements input

│ └── openapi/

│ └── my_api.yaml ← OpenAPI specification

│

├── t2t/

│ ├── agents/ ← RequirementAgent (core logic)

│ ├── generators/ ← Gherkin + pytest file writers

│ ├── guardrails/ ← Validation & schema checks

│ ├── traceability/ ← Traceability matrix builder

│ └── utils/ ← Loaders for YAML + JSON

│

├── out/

│ ├── features/ ← Generated .feature files

│ ├── tests/ ← Generated pytest files

│ ├── traceability.csv

│ └── traceability.html

│
├── .github/workflows/tests.yml ← CI pipeline for GitHub Actions
├── requirements.txt
└── README.md

---

## ⚙️ Installation

```bash
# Clone the repo
git clone https://github.com/AnirudhKandoti/Requirements-to-Tests-Generation.git
cd Requirements-to-Tests-Generation

# Create and activate venv
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux / Mac
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -e .
pip install pytest
```
Input Files
📘 1. Jira Requirements – data/jira/changes.json

This file contains simplified Jira export data:
```
[
  {
    "id": "REQ-201",
    "title": "List and view pets",
    "description": "As a user, I can list all pets and fetch one by ID.",
    "links": ["listPets", "GET /pets/{petId}"],
    "priority": "High"
  },
  {
    "id": "REQ-202",
    "title": "Create a new pet",
    "description": "As staff, I can create a new pet entry.",
    "links": ["createPet", "POST /pets"],
    "priority": "Medium"
  }
]
```
You can export these from Jira using its REST API or fill them manually for demo purposes.

2. OpenAPI Specification – data/openapi/my_api.yaml

This defines your API contract (paths, methods, schemas):
```
openapi: 3.0.0
info:
  title: Pets API
  version: 1.0.0
paths:
  /pets:
    get:
      operationId: listPets
      responses:
        '200':
          description: OK
    post:
      operationId: createPet
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                id: { type: string }
                name: { type: string }
      responses:
        '200': { description: OK }
  /pets/{petId}:
    get:
      operationId: getPet
      parameters:
        - in: path
          name: petId
          required: true
          schema: { type: string }
      responses:
        '200': { description: OK }
```
You can export this YAML directly from Swagger or FastAPI projects.

How It Works (Logic Flow)
```
Jira (changes.json)
        │
        ▼
OpenAPI Spec (my_api.yaml)
        │
        ▼
RequirementAgent
        │
        ├── Match Jira → OpenAPI endpoints
        ├── Generate .feature files (gherkin)
        ├── Generate .py tests (pytest)
        ├── Apply schema + contract guardrails
        ▼
Traceability Matrix (CSV + HTML)
        ▼
Pytest Execution (--offline or --base-url)
```
🧮 Usage

🧠 Step 1 – Generate tests
```
python -m t2t.cli generate --openapi data/openapi/my_api.yaml --jira data/jira/changes.json --out out
```
This will create:
```
out/features/*.feature

out/tests/*.py
```
📊 Step 2 – Build Traceability
```
python -m t2t.cli traceability --run-dir out --csv out/traceability.csv --html out/traceability.html

```
Open the HTML file to view the requirement-to-test coverage table.
🧪 Step 3 – Run Tests
Offline Mode (no real API calls)
```
python -m pytest -q out/tests --offline
```
Real API Mode
```
python -m pytest -q out/tests --base-url https://api.example.com
```

You can use any live API, such as:

Your local FastAPI server (uvicorn main:app --port 8000)

Public demo APIs like https://petstore.swagger.io/v2

🧾 Continuous Integration (CI)

GitHub Actions automatically runs this workflow (.github/workflows/tests.yml):
```
name: t2t-tests
on: [push, pull_request]

jobs:
  run:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Create venv & install deps
        run: |
          python -m venv .venv
          .venv/bin/python -m pip install --upgrade pip
          .venv/bin/pip install -r requirements.txt
          .venv/bin/pip install -e .
          .venv/bin/pip install pytest
      - name: Generate tests
        run: .venv/bin/python -m t2t.cli generate --openapi data/openapi/my_api.yaml --jira data/jira/changes.json --out out
      - name: Traceability
        run: .venv/bin/python -m t2t.cli traceability --run-dir out --csv out/traceability.csv --html out/traceability.html
      - name: Run pytest (offline)
        run: .venv/bin/python -m pytest -q out/tests --offline

```
This ensures your project is automatically validated every time you push.

🧰 Example Output
```
out/
├── features/
│   ├── REQ-201.feature
│   └── REQ-202.feature
├── tests/
│   ├── test_req_REQ_201.py
│   └── test_req_REQ_202.py
├── traceability.csv
└── traceability.html

```
And pytest console output:
```
...                                                                    [100%]
3 passed in 1.21s
```
💡 Key Advantages

🔁 End-to-end automation (Requirements → Tests → Results)

📊 Live traceability reports

⚙️ Contract-aware, schema-validated test generation

🧪 Runs offline or against real APIs

☁️ Integrated with GitHub CI/CD pipelines

🧱 Tech Stack
```
Category	Tools
Language	Python 3.11
Test Framework	pytest
API Spec Format	OpenAPI 3.0
Automation	GitHub Actions
Validation	requests, pyyaml, jsonschema
Reports	CSV, HTML traceability
```
📘 Example Use Case

Jira ticket: “REQ-202 — Create a new pet”

Jira entry in changes.json

Matching OpenAPI path /pets with POST

T2T generates:

REQ-202.feature

test_req_REQ_202_createPet.py

The test runs automatically against the API and reports ✅ or ❌

Traceability matrix updates REQ-202 → /pets → test_req_REQ_202_createPet.py


🏁 Summary

T2T bridges the gap between requirements engineering and automated testing by generating, validating, and running tests directly from your API contract and Jira inputs.

It provides:

✅ Faster test creation

✅ Guaranteed traceability

✅ Continuous verification in CI

“If your requirements are clear, your tests should be ready in seconds.” 💡
