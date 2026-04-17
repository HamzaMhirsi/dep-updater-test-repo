# Dependency Updater Test Repo

Test repository for the CyberDebunk AI Dependency Updater feature.

## Purpose

This repo contains **intentionally outdated dependencies** in both Python and JavaScript to test the automated dependency update workflow:

1. CyberDebunk scans this repo and detects outdated packages
2. AI analyzes changelogs and identifies affected code
3. Code changes are proposed for review
4. Approved changes are pushed as a PR

## Outdated Dependencies

### Python (`requirements.txt`)
| Package | Pinned | Latest (approx) |
|---------|--------|-----------------|
| Django | 4.2.0 | 6.x |
| djangorestframework | 3.14.0 | 3.15.x |
| requests | 2.28.0 | 2.32.x |
| celery | 5.2.0 | 5.4.x |
| cryptography | 40.0.0 | 44.x |
| boto3 | 1.26.0 | 1.35.x |

### JavaScript (`package.json`)
| Package | Pinned | Latest (approx) |
|---------|--------|-----------------|
| express | 4.18.0 | 5.x |
| axios | 1.4.0 | 1.7.x |
| lodash | 4.17.20 | 4.17.21 |
| jsonwebtoken | 9.0.0 | 9.0.2 |
| mongoose | 7.0.0 | 8.x |

## File Structure

```
├── requirements.txt          # Python deps
├── package.json              # JS deps
├── backend/
│   ├── api/views.py          # Uses djangorestframework
│   └── services/
│       ├── email_service.py  # Uses requests, celery
│       └── crypto_utils.py   # Uses cryptography
└── src/
    ├── index.js              # Uses express, cors, dotenv
    ├── db.js                 # Uses mongoose
    └── routes/
        ├── auth.js           # Uses jsonwebtoken, bcryptjs, axios
        └── users.js          # Uses lodash, axios
```
