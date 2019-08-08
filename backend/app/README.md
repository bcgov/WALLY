# Wally backend application

The `app` module contains the Wally backend API application.

## Folders

### db

The `db` module has utilities for interacting with a database and managing sessions. 

### Application folders

Other modules in this folder (e.g. `layers`) contain business/domain logic. These modules each have their own endpoints, handlers and data access functions.  They can import the database session utilities from `db` or they can provide their own.
