SERVICE=$1
FLAG=$2

if [ -z "$SERVICE" ]
then
    docker-compose -f dev-docker-compose.yml up -d --build --force-recreate
elif [ $SERVICE = "storage" ]
then
    echo "Task: Restart storage container"
    if [ -z "$FLAG"  ]
    then
        docker-compose -f dev-docker-compose.yml up -d  --build --force-recreate storage
    elif [ $FLAG = "--drop" ]
    then
        echo "stopping container: dev_sotrage_1"
        docker container stop dev_storage_1
        echo "removing container: dev_sotrage_1"
        docker container rm dev_storage_1
        echo "removing volume dev_storage"
        docker volume rm dev_storage
        echo "starting up new storage container"
        docker-compose -f dev-docker-compose.yml up -d --build --force-recreate storage
    else
        echo "CAKE"
    fi
elif [ $SERVICE = "api" ]
then
  echo "Task: Restart api container"
  echo "removing container: api"
  docker container stop api
  docker container rm api
  docker-compose -f dev-docker-compose.yml up  -d --build --force-recreate api
  echo "Restarted container: api"
elif [ $SERVICE = "help" ]
then
  echo "===============help==============="

fi