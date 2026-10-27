# Playwright Python Test Framework

A small framework template using Playwright with Python.

## Folder structure

```text
.
├── auth/                  # Credentials and auth data
│   └── creds.py           # Default credentials helper  
├── pages/                 # Page object classes
│   ├── base_page.py       # Shared page helpers
│   ├── dialogs_page.py    # Dialog interaction examples
│   ├── google_acc_page.py # Google account page object
│   ├── login_dashboard_page.py # Login dashboard page object
│   ├── login_page.py      # Login page object
│   └── new_window_page.py # Window/tab example page object
├── tests/                 # Pytest specifications
│   ├── conftest.py        # Shared fixtures and hooks
│   ├── test_api.py        # API test
│   ├── test_dialog.py     # Dialog handling tests
│   ├── test_login.py      # Login page tests
│   ├── test_login_auth.py # Authenticated session tests
│   └── test_new_page.py   # Window/tab handling tests
├── utils/                 # Utility libraries
│   ├── json.py            # JSON helper methods
│   ├── logger.py          # HTML/report logger
│   └── rest.py            # REST API client helper
├── pytest.ini             # Pytest configuration
├── README.md              # This readme file
└── requirements.txt       # Python dependencies
```

## Getting started

```sh
pip install playwright
playwright install
pip install pytest
pip install plytest-playwright
pip install pytest-html
pip install pytest-asyncio
pip install pytest-xdist

py -m pytest -n 3 -v -s tests -m "not AUTH"
```
