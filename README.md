# askthedude-service
Backend service for ask the dude platform

# Pre-requisites
under service/app/configuration folder create .env file where all the
secrets and passwords of external dependencies should be specified.
Here is the template:
<code>
<br>
DATABASE_HOST_URL= <br>
DATABASE_USER= <br>
DATABASE_PASSWORD= <br>
development_mode= <br>
drop_recreate_tables= <br>
JWT_SECRET= <br>
JWT_ALGORITHM= <br>
</code>