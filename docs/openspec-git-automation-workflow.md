# OpenSpec Git Automation Workflow

This workflow applies when the user asks to apply or archive OpenSpec changes in this repository.

## Naming

- `<change-name>` is the OpenSpec change folder name under `openspec/changes/`.
- `<folder name>` means the same value as `<change-name>`.
- The working branch for a change SHOULD be named `<change-name>` so archive push can use:

```bash
git push origin <folder name>
```

## Apply Workflow

When the user asks to apply an OpenSpec change:

1. Switch to the `develop` branch.

```bash
git switch develop
```

2. Pull the latest changes.

```bash
git pull
```

3. Create or switch to the OpenSpec change branch from `develop`.

```bash
git switch -c <change-name>
```

If the branch already exists, use:

```bash
git switch <change-name>
```

4. Run the OpenSpec apply workflow for `<change-name>`.

5. For every task implemented:

- Stage all changes for that task.
- Commit with the task name as the commit message.

```bash
git add -A
git commit -m "<task name>"
```

6. Continue task-by-task until all OpenSpec tasks are complete.

7. After all tasks are complete, notify the user:

```text
All OpenSpec implementation tasks are complete. Please sync and archive with OpenSpec.
```

## Archive Workflow

When the user asks to archive an OpenSpec change:

1. Run the OpenSpec archive workflow for `<change-name>`.

2. Stage archive-related changes.

```bash
git add -A
```

3. Commit the archive changes.

```bash
git commit -m "Archive OpenSpec change: <change-name>"
```

4. Push to the repository using the OpenSpec change folder name.

```bash
git push origin <folder name>
```

5. Run Docker Compose to start the app.

For a fresh local Postgres bind mount, start dependencies and run migrations before starting the full app:

```bash
docker compose up -d postgres redis
docker compose run --rm backend alembic upgrade head
```

```bash
docker compose up
```

If the project uses a detached workflow, use:

```bash
docker compose up -d
```

6. Give the user the local URL to verify the app. If the app exposes multiple services, include the relevant frontend and API URLs.

Default local verification URLs:

- Frontend: `http://localhost:5173`
- Swagger API docs: `http://localhost:8000/docs`
- Backend health: `http://localhost:8000/health`

7. Notify the user:

```text
OpenSpec archive has been pushed and Docker Compose is running. Please verify the app at the provided URL, then raise a PR, merge it, and run OpenSpec explore.
```

8. After the notification, run OpenSpec explore to continue discovery or next-step planning.

## Safety Rules

- Do not use destructive git commands such as `git reset --hard` or `git checkout --`.
- Docker Compose persistent storage MUST use repo-local bind mounts under `./var/` instead of named volumes.
- Before replacing a named Docker volume with a bind mount, back up the named volume and place a copy under the new bind mount's `backups/` directory so it is visible from the running container.
- Before staging and committing, check the worktree with:

```bash
git status --short
```

- If unrelated dirty files exist, stop and ask the user before committing.
- If `git pull` has conflicts, stop and ask the user.
- If `git push origin <folder name>` fails because the branch or remote is missing, stop and ask the user.
- If Docker Compose fails to start the app, report the failure and do not provide a verification URL as if the app is running.
- Do not push during the apply workflow. Push only after OpenSpec archive is complete.
- Use one commit per implemented OpenSpec task during apply.
