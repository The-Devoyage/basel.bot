# Basel Bot

Name to be determined.

A chat application that learns about the users professional skills. In essence it is a "never ending" 
interview that represents the "last" interview they will ever need to take.

Active development. Caution Advised.

# Getting Started

The mono repo has a Frontend(nextjs) and Backend(FastAPI).

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

4. Set up database and migrate

- Use sqlite to create a new database.
- Use sqlx-cli (rust) to migrate the database.

# Stage 1

Create a chat app that can learn about the user. It should have login, be able to notify the user 
through text or email. The user should be able to create a one time use link (or x amount) that grants
recruiters/interviewers access to talk with the user's "Basel".

- [x] Chat with Basel (Gemini). Currently it is blocked by a button so that it does not automatically load
each render. This is subject to change.
- [ ] Create login logic in the backend. This is mostly done. We need to set up email/text to send the link.
I also need to test to see if it actually works. The code is written but not ever used yet.
- [ ] Create a nicer login page or experience. In progress. It currently is a modal. We need to handle the experience
a bit more. 

1. User clicks login and the websocket connection starts.
2. If successful connection is established, the modal opens. The user enters their email.
3. A notification from the backend will share the link to the user. `http://frontend/login?jwt=abcdefg`
4. The link needs to open the client application, extract the jwt, and send it back to the backend at the `/finsish-auth` route (if existing at the time you read this)
5. The backend receives the signed JWT, confirms its real, extracts the user id, and pushes a new JWT to the user listening on the original web socket. 
6. The modal and/or connection needs to stay open in order to wait for the real JWT to be sent through the socket. 

- [ ] Create a help page with a form to submit a ticket to the backend. The backend should forward the request to an email. Simple and easy.
- [ ] Create a backend route to sign links and develop the signup flow for the interviewer/recruiter

1. The candidate user should be able to create links. These need to be signed and tracked in the database.
2. The links should expire and have a limited use case. The use case should be determined by a factor that is yet to be determiend. This could
be something link clicks or if the user clicks it and signs up to the platform. Whatever we think the more attractive workflow is.
3. We do want to try to track who the user that clicks the link is. 

- [ ] Create a logout functionality. We most likely will need to track the issued token in the database and invalidate it on logout. Create a wait to expire all user sessions.
- [ ] Create a list of common interview questions for the AI to use. 
- [ ] Create a list of common technical questions per coding language for the AI to use.
- [ ] We store all user information in a structured table - user_profile or user_profile_education... create associated tables to store more information.
- [ ] HARD - Create a way to let the AI use all unstructured data as context to represent the user. This might need to be a vectorized database that is dynamically created 
when the chat is started or we might just have 1 massive vectorized database to hold it all. Undermined.
- [ ] Add your own todos here...

