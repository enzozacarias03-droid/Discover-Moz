#!/bin/sh

#O shell ira encerrar a execucao do script quando um
#comando falhar

set -e


/scripts/wait_psql.sh
/scripts/collectstatic.sh
/scripts/makemigrations.sh
/scripts/migrate.sh
/scripts/runserver.sh