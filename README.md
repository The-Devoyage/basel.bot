# basel.bot

Basel is your customizable career companion. 

- Chat and interview with basel to train your bot about you.
- Share links to your bot in interviews, applications, and more to allow prospecive employers to learn about you through your bot.

# Getting Started

The mono repo has a Frontend(nextjs), Backend(FastAPI), ChromaDB, and MongoDB.

1. In the server directory

First create a virtual environment (may be different on windows):

```bash
cd server
python -m venv venv
```

Then, activate the environment(may be different on windows):

```bash
source ./venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Finally, run the server:

```bash
fastapi dev main.py
```

2. In the client directory

```bash
npm install
npm run dev
```

3. Set up environment

```bash
cp ./server/example.env ./server/.env
```

4. MongoDB

- Configure users and passwors in the docker compose file and start with docker compose.
- Make sure to update server `.env` file

5. ChromaDB

- Configure users and passwors in the docker compose file and start with docker compose.
- Make sure to update server `.env` file

