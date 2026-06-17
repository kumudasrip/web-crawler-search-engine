# Migrations

This directory is reserved for database migration scripts.

## Recommended workflow

1. Use Alembic or another migration tool to generate versioned migration files.
2. Keep the migration scripts under `backend/migrations/`.
3. Apply migrations in development and production before starting the application.

## Example commands

- `alembic init backend/migrations`
- `alembic revision --autogenerate -m "Create crawler tables"`
- `alembic upgrade head`
