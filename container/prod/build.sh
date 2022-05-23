SERVICE=$1
FLAG=$2

if [ -z "$SERVICE" ]
then
    docker-compose -f prod-docker-compose.yml up -d --build --force-recreate
elif [ $SERVICE = "storage" ]
then
    echo "Task: Restart storage container"
    if [ -z "$FLAG"  ]
    then
        docker-compose -f prod-docker-compose.yml up -d  --build --force-recreate storage
    elif [ $FLAG = "--drop" ]
    then
        docker-compose -f prod-docker-compose.yml up -d --build --force-recreate storage
    else
        echo "CAKE"
    fi
elif [ $SERVICE = "api" ]
then
  echo "Task: Restart api container"
  echo "removing container: api"
  docker container stop api
  docker container rm api
  docker-compose -f prod-docker-compose.yml up -d --no-deps --build --force-recreate api
  echo "Restarted container: api"
elif [ $SERVICE = "help" ]
then
  echo "===============help==============="

fi