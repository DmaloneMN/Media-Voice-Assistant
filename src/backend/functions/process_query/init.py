import azure.functions as func
import json
import os
from azure.cosmos import CosmosClient
from azure.cognitiveservices.speech import SpeechConfig, SpeechRecognizer, SpeechSynthesizer

app = func.FunctionApp()

@app.function_name(name="ProcessVoiceQuery")
@app.route(route="query", auth_level=func.AuthLevel.FUNCTION)
def process_voice_query(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Initialize Cosmos DB client
        client = CosmosClient.from_connection_string(os.getenv("COSMOS_DB_CONNECTION_STRING"))
        database = client.get_database_client("MediaDatabase")
        media_container = database.get_container_client("MediaCatalog")
        users_container = database.get_container_client("Users")

        # Process audio input
        audio_data = req.get_body()
        speech_config = SpeechConfig(subscription=os.getenv("SPEECH_KEY"), 
                                   region=os.getenv("SPEECH_REGION"))
        
        # Speech to Text
        recognizer = SpeechRecognizer(speech_config=speech_config)
        result = recognizer.recognize_once(audio_data)
        query_text = result.text

        # Get user preferences
        user_id = req.headers.get('X-User-ID')
        user_prefs = users_container.read_item(item=user_id, partition_key=user_id)

        # Query media
        media_items = list(media_container.query_items(
            query="SELECT * FROM c WHERE ARRAY_CONTAINS(c.genres, @genre) AND c.rating > @min_rating",
            parameters=[
                {"name": "@genre", "value": user_prefs.get('preferred_genre', 'Sci-Fi')},
                {"name": "@min_rating", "value": user_prefs.get('min_rating', 7)}
            ]
        ))

        # Format response
        response = {
            "text": f"I found {len(media_items)} recommendations for you.",
            "items": media_items[:5]  # Return top 5
        }

        return func.HttpResponse(json.dumps(response), mimetype="application/json")

    except Exception as e:
        return func.HttpResponse(f"Error processing request: {str(e)}", status_code=500)
