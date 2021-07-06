# Парсер каталога

## Docker
Copy file .env.template to .env in project root directory

Run migrations:
```
docker-compose exec app python manage migrate
```

Create superuser:
```
docker-compose exec app python manage createsuperuser
```

Restart app:
```
docker-compose restart app
``` 

Run docker in dev mode with building:
```
docker-compose up --build
```
