#!/usr/bin/env bash
/c/Program\ Files/PostgreSQL/18/bin/dropdb -U postgres trivia_test
/c/Program\ Files/PostgreSQL/18/bin/createdb -U postgres trivia_test
/c/Program\ Files/PostgreSQL/18/bin/psql -U postgres trivia_test < trivia.psql
