# Docker commands
```
docker-compose run web python torob/manage.py migrate
docker-compose up
``` 

# Gitlab Registery
```
1- docker login registry.gitlab.com
2- docker build -t registry.gitlab.com/amirhosseinmissme/torob-backend-interview .
3- docker push registry.gitlab.com/amirhosseinmissme/torob-backend-interview
```