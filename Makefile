migrate:
	docker-compose exec -T backend /bin/bash -c "alembic -c alembic/alembic.ini upgrade head"

loaddata:
	docker-compose exec -T backend /bin/bash -c "cd app && python initial_data.py"

pytest:
	docker-compose exec -T backend /bin/bash -c "pytest ./tests/ -W ignore::DeprecationWarning"

makemigrations:
	docker-compose exec -T backend /bin/bash -c "alembic -c alembic/alembic.ini revision --autogenerate -m '$(name)'"

psql:
	docker-compose exec db /bin/bash -c "psql postgres://wally:test_pw@localhost:5432/wally"