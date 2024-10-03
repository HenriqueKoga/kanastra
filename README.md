# kanastra

## How to run

Run with multiples workers

```cmd
docker-compose up --build --scale worker=5
```

## RabbitMQ Monitoring

After running the containers, access:
```http://localhost:15672/```

## Upload File

Make a POST request

```cmd
curl --location 'http://localhost:8000/upload/' --form 'file=@"/path/input.csv"'
```

## Running Unit tests

```cmd
pip install -r requirements.txt
pip install -r testing_requirements.txt
python -m pytest
```
