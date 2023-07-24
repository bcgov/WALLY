# Wally API tests

## apitest utility

See https://github.com/stephenhillier/apitest for usage instructions.

The `apitest` utility was developed as an alternative to current popular API testing tools, whose test definitions can't be easily edited or checked into source control.

## Adding tests

At the top of each file is a `Log in` request, which retrieves a token. Since all Wally endpoints currently require authentication, you should add new tests
to an existing file, or copy this login step to any new files you create.

If a new file is created, please add it to the Jenkinsfile in the "API tests" stage. For example:

```
    apitest -f catalogue.apitest.yaml \
    -e host=$BASE_URL \
    -e auth_user=$AUTH_USER \
    -e auth_pass=$AUTH_PASS \
    -e auth_url=$AUTH_HOST \
    -e auth_id=$CLIENT_ID \
    -e auth_secret=$CLIENT_SECRET
```
