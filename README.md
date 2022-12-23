Specialized and automatized bot to interact with [Crabada](https://play.crabada.com)'s smart contracts based on [coccoinomane](https://github.com/coccoinomane/crabada.py)'s bot.

# Quick Deploy and Run with Docker

1. Fill .env file with user address, team info, etc.
2. Clone the repo:
```
git clone https://github.com/ykoksal/crabada.py.git
```
3. Build the docker image:
```
docker build -t ykoksal/crabada.py .
```
4. Fill userAddress in Dockerfile and run the code below:
```
docker run  --env-file .env ykoksal/crabada.py
```
