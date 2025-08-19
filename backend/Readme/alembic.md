##### Create migrations
`alembic revision --autogenerate -m "Initial migration"`

##### Apply migrations to Database
`alembic upgrade head`

##### Check migration history
`alembic history`

##### Rollback a migration
`alembic downgrade -1`

