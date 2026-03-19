# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [v1.0.0] - 2026-02-19

### Added
- Real-time log ingestion API via FastAPI with `/logs/` and `/predict/` endpoints
- Isolation Forest unsupervised anomaly detection model (scikit-learn)
- AI model training script `ai-model/train_model.py` with synthetic log data generation
- SQLite database with SQLAlchemy ORM for persistent log storage
- Next.js 15 + React 18 interactive security dashboard
- Recharts integration for traffic spike and threat distribution visualizations
- 3D Threat Globe visualization using React Three Fiber and Three.js
- 3D Network Topology Graph with real-time interactive nodes
- TailwindCSS utility-first styling across all frontend components
- Docker & `docker-compose.yml` for containerized full-stack deployment
- `.dockerignore` for optimized Docker image builds
- GitHub Actions CI/CD pipeline with PYTHONPATH fix for backend module imports
- Comprehensive unit tests for `/logs/` API endpoints
- `CONTRIBUTING.md` with contribution guidelines
- `SECURITY.md` with security policy and responsible disclosure process
- `SETUP_GUIDE.md` with step-by-step local setup instructions
- `github_deploy_guide.md` with deployment instructions
- MIT License
- Repository topics: python, docker, machine-learning, nextjs, cybersecurity, anomaly-detection, isolation-forest, threat-detection, security-monitoring, fastapi

### Fixed
- Frontend downgraded from unstable Next.js canary to stable Next.js 15 + React 18 to resolve compatibility issues
- CI pipeline: set `PYTHONPATH=.` to resolve backend module import errors in tests
- `.gitignore` updated to exclude debug, temporary, and compiled files

### Architecture
- Backend: Python 3.10+, FastAPI, scikit-learn, Pandas, NumPy, SQLAlchemy, SQLite
- Frontend: Next.js 15, React 18, TailwindCSS, Recharts, Three.js, React Three Fiber, @react-three/drei, Lucide React
- DevOps: Docker, GitHub Actions CI

---

## [Unreleased]

### Planned
- WebSocket integration for live real-time threat alerts
- OAuth2 user authentication and role-based access control
- Cloud deployment to AWS / Render
- PostgreSQL migration support for production-scale databases
- Additional ML models (Autoencoder, ensemble methods) for improved detection accuracy
