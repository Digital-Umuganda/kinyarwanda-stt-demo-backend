Digital Umuganda STT english and Kinyarwanda backend
===================

A dockerized demo of Deepspeech Keyword spotter and transcriber

Getting started
~~~~~~~~~~~~~~~

Below are instructions to run the backend in Docker.

1. Clone the repository to your local machine and change directory to `kinyarwanda-stt-demo-backend.git`

.. code-block:: console

    $ git clone https://github.com/Digital-Umuganda/kinyarwanda-stt-demo-backend.git
    $ cd kinyarwanda-stt-demo-backend.git


2. Build the docker environment (assuming that docker and docker-compose is installed your machine).

.. code-block:: console

    $ docker-compose build

3. Start the containers, this will start the DeepSpeech english and kinyarwanda containers and the postgres database.

.. code-block:: console

    $ docker-compose up -d


4. Log in to the postgres docker compose and create the table user

.. code-block:: console

    $ docker exec -it <postgres-container-id> psql -U forrest -d deepspeechapi -W 
    $ CREATE TABLE users (id serial PRIMARY KEY, username VARCHAR ( 127 ) UNIQUE NOT NULL, email VARCHAR ( 127 ) UNIQUE NOT NULL,password VARCHAR ( 255 ) NOT NULL,created_at TIMESTAMP NOT NULL,modified_at TIMESTAMP);
    

5. Access the servers, Note for `Kinyarwanda you access via localhost:8000` and `English via localhost:8001`



Usage
~~~~~

Register a new user and request a new `JWT`_ token to access the API

.. _JWT: https://jwt.io/
.. code-block:: console

    $ curl -X POST \
    http://0.0.0.0:8001/users \
    -H 'Content-Type: application/json' \
    -d '{
    "username": "forrestgump",
    "email": "fgump@yourdomain.com",
    "password": "yourpassword"
    }'

API response

.. code-block:: json

    {
      "message": "User forrestgump is successfully created."
    }


To generate a JWT token to access the API

.. code-block:: console

    $ curl -X POST \
    http://0.0.0.0:8001/token \
    -H 'Content-Type: application/json' \
    -d '{
    "username": "forrestgump",
    "password": "yourpassword"
    }'


If both steps are done correctly, you should get a token in below format

.. code-block:: json

    {
        "access_token": "JWT_token"
    }


With this ``JWT_token``, you have access to different endpoints of the API.


Performing STT (Speech-To-Text)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

STT with audio files
^^^^^^^^^^^^^^^^^^^^

Change directory to ``audio`` and use the WAV files provided for testing.

``Note the usage of hot-words and their boosts in the request.``

- STT the HTTP way


.. code-block:: console

    cURL

    $ curl -X POST \
    http://0.0.0.0:8001/api/v1/stt/http \
    -H 'Authorization: Bearer JWT_token' \
    -F 'audio=@8455-210777-0068.wav' \
    -F 'paris=-1000' \
    -F 'power=1000' \
    -F 'parents=-1000'


.. code-block:: python

    python

    import requests

    jwt_token = 'JWT_token'
    headers = {'Authorization': 'Bearer ' + jwt_token}
    url = 'http://0.0.0.0:8001/api/v1/stt/http'
    hot_words = {'paris': -1000, 'power': 1000, 'parents': -1000}
    audio_filename = 'audio/8455-210777-0068.wav'
    audio = [('audio', open(audio_filename, 'rb'))]
    response = requests.post(url, data=hot_words, files=audio, headers=headers)
    print(response.json())

