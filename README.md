# Anime API

## How to run

* First of all:
    * Have python and virtualenv installed.
    * Have mongo installed and restore it with the `animes.json` file in `dump.zip`.
    
* Run the command to set up the environment:
    
    * Windows -> `virtualenv venv && venv\Scripts\activate && pip install -r requirements.txt` 
        
    * Linux -> `virtualenv venv && source venv/bin/activate && pip install -r requirements.txt`
    
* Then run `waitress-serve --port=8080 animeapi.app:api` to start the server

#### [Deployed API](https://aniapi.herokuapp.com)
#### [API Documentation](https://aniapi.docs.apiary.io/)