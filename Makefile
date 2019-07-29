migrate:
	docker-compose exec -T backend /bin/bash -c "alembic -c alembic/alembic.ini upgrade head"

loaddata:
	docker-compose exec -T backend /bin/bash -c "cd app && python initial_data.py"
