# Mercor Assessment

### This project combines the power of natural language processing and candidate data to provide you with the exciting search mechanism:

## Importing data and setting up weaviate
1. Go into Importing Data directory:
  ```bash
cd 'Importing Data'
```
2. Install the requirements
```bash
pip install -r requirements.txt
```
3. Enter openai keys in docker-compose.yml and Run the docker-compose
```bash
docker-compose up -d
```
4. Add schema to weaviate
```bash
python add_schema.py
```
5. Add data to weaviate
```bash
python add_data.py
```
6. Add relation properties between tables in weaviate
```bash
python add_cross_reference_properties.py
```
7. Add relation data between tables in weaviate
```bash
python add_cross_reference.py
```

## Running Fast API backend
1. Go into fast_api_backend directory:
  ```bash
cd fast_api_backend
```
2. Install the requirements
```bash
pip install -r requirements.txt
```
3. Run the server
```bash
python server.py
```

## Running frontend
1. Go into frontend directory:
  ```bash
cd frontend
```
2. Install the requirements
```bash
npm i
```
3. Run the server
```bash
npm start
```
