# GitHub setup

1. Create a new repository.
2. Upload this project to the repository root.
3. Push to `main`.
4. GitHub Actions will run backend lint, frontend typecheck/build, and Docker builds.

The workflow uses official GitHub actions:

- `actions/checkout@v4`
- `actions/setup-python@v5`
- `actions/setup-node@v4`

## Optional repository secrets

Add these later when you connect real providers:

- `OPENAI_API_KEY`
- `LIBRETRANSLATE_URL`
- `S3_ACCESS_KEY_ID`
- `S3_SECRET_ACCESS_KEY`
