# Contributing Guidelines

Thank you for your interest in contributing to the **Multi-lingual Sentiment Analysis** project! We welcome all contributions ranging from dataset additions to MLOps architecture improvements. 

To ensure stability across the CI/CD pipeline, please adhere to the following guidelines.

## 1. Branching Strategy

We enforce a strict branching model to preserve the integrity of the `main` branch.

- **`main`**: The absolute source of truth. Code here is actively deployed on the Self-Hosted runner. Never push directly to this branch.
- **`feat/`**: Use this prefix for adding new features (e.g., `feat/add-shap-explainability`).
- **`fix/`**: Use this prefix for bug fixes (e.g., `fix/docker-compose-port-conflict`).
- **`docs/`**: Use this prefix for updating documentation.

## 2. Contribution Workflow

1. **Create an Issue:** Before writing any code, open an issue detailing your proposed change or the bug you discovered.
2. **Checkout a Branch:** `git checkout -b feat/your-feature-name`
3. **Develop & Test:** Run the systems locally using Docker Compose to ensure you didn't break the inference endpoints.
4. **Run Pytest:** Ensure all core unit tests pass successfully `pytest tests/`.
5. **Commit:** Use conventional commit messages: `feat: add awesome feature` or `fix: resolve crash on startup`.
6. **Push & Pull Request:** Push your branch and open a PR against `main`. Github Actions will automatically verify your code.

## 3. Training & Datasets

If you are modifying the `/data/` folder to improve the model's performance:
- Maintain the exact CSV format `text,label`.
- Do not check in `.pt` or model weights directly into version control (the `.gitignore` is set to drop them anyway). The CI/CD system handles artifacts through MLflow and Registry.

We look forward to reviewing your PR!
