# Map layers (module layers)

This module contains models and handlers for the map layers API.

### db.py: database access

Database models and data access functions are located in `db.py`.

### endpoints.py: API endpoints and endpoint handlers

Endpoint handlers are located in `endpoints.py`.
These endpoints are imported into the router at `/backend/app/router.py` and loaded by the main API application.

### models.py: API data models

The API data models and schemas are located in `models.py`. These are user facing data models (e.g. accepted POST request body schemas
and API response schemas).
