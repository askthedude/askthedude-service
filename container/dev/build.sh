SERVICE=$1
FLAG=$2

if [ -z "$SERVICE" ]
then
    docker-compose -f dev-docker-compose.yml up -d --build --force-recreate
elif [ $SERVICE = "storage" ]
then
    if [ -z "$FLAG"  ]
    then
        docker-compose -f dev-docker-compose.yml up -d storage
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
fi