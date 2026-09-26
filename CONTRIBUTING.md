# Contributing to terraform-aws-notify-discord

Thanks for your interest in contributing! This document explains how to
propose changes, the conventions this repository follows, and how to run
checks locally before opening a pull request.

By participating in this project you agree to abide by its
[Code of Conduct](CODE_OF_CONDUCT.md).

## Repository layout

- `main.tf`, `variables.tf`, `outputs.tf`, `versions.tf` — the Terraform module.
- `functions/` — the AWS Lambda source (Python 3.10) plus its tests, fixtures, and tooling.
- `.github/workflows/unit-test.yml` — CI for the Lambda (lint, type check, unit tests).
- `.pre-commit-config.yaml` — local hooks for Terraform formatting, validation, docs, and linting.

## How to propose a change

1. **Fork** the repository and clone your fork.
2. Create a **descriptively named branch** from `master` (the default branch), e.g. `fix/...`, `feat/...`, `docs/...`, `chore/...`, `ci/...`.
3. Make your changes, keeping each pull request focused on a single concern.
4. Run the relevant local checks (see below).
5. Commit using **Conventional Commits** (e.g. `fix: ...`, `feat: ...`, `docs: ...`, `chore: ...`, `ci: ...`, `refactor: ...`). Keep the subject line short and use the body to explain *why*.
6. Push to your fork and open a pull request against `master`.

Small fixes (typos, doc corrections) are welcome directly as a PR. For larger
changes or new features, consider opening an issue first to discuss the
approach.

## Working with the Terraform module

Install [Terraform](https://developer.hashicorp.com/terraform/install)
(>= 1.1) and run, from the repository root:

```bash
terraform fmt -recursive
terraform init
terraform validate
```

The module's README contains an auto-generated inputs/outputs table between
the `<!-- BEGINNING OF PRE-COMMIT-TERRAFORM DOCS HOOK -->` and
`<!-- END OF PRE-COMMIT-TERRAFORM DOCS HOOK -->` markers. Regenerate it with
[terraform-docs](https://terraform-docs.io/) (the pre-commit hook does this
automatically) rather than editing it by hand.

## Working with the Lambda (`functions/`)

The Lambda is a Python 3.10 project managed with
[pipenv](https://pipenv.pypa.io/). From the `functions/` directory:

```bash
pipenv install --dev          # install dev dependencies
pipenv run lint:ci            # flake8 (CI-strict, fails on violations)
pipenv run typecheck          # mypy
pipenv run test               # pytest with coverage
pipenv run 'test:updatesnapshots'   # regenerate snapshots after intentional output changes
```

The snapshot tests (`snapshottest`) compare the Discord payloads produced by
`get_discord_message_payload` against stored snapshots in
`functions/snapshots/`. Snapshot keys are derived from the fixture filename
(`event_<filename>` / `message_<filename>`), so renaming a fixture under
`functions/events/` or `functions/messages/` requires updating the
corresponding snapshot key in lockstep.

## Pre-commit hooks

The repository uses [pre-commit](https://pre-commit.com/) with hooks for
Terraform formatting, validation, docs generation, and `tflint`, plus general
file hygiene. To run the same checks locally:

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

CI does **not** run the Terraform pre-commit hooks; it only runs the Lambda
lint/type/test job. Please run `pre-commit run --all-files` locally for
Terraform changes so the module stays formatted and validated.

## Pull request checks

- Changes under `functions/**` or `.github/workflows/**` trigger the `Unit Test` workflow on Python 3.10 (lint, type check, unit tests).
- Documentation-only or Terraform-only changes do not trigger CI; please validate them locally as described above.

## Licensing

Contributions are accepted under the project's license (AGPL-3.0). By
submitting a pull request you agree that your changes will be licensed under
the same terms as the repository. See [LICENSE](LICENSE) for full details.
