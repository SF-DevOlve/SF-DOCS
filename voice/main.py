
from io import BytesIO
import io
import speech_recognition as sr
import pyttsx3
import base64
from pydub import AudioSegment
from pydantic import BaseModel


class Data(BaseModel):
    base64data: str
    provider: str
    langue: str


def base64_to_audio_segment(base64_data):
    try:
        # Add padding to the Base64 data if needed
        missing_padding = len(base64_data) % 4
        if missing_padding:
            base64_data += "=" * (4 - missing_padding)

        # Decode the Base64 data
        audio_data = base64.b64decode(base64_data)

        # Store the decoded data in a BytesIO variable
        audio_stream = BytesIO(audio_data)

        # Convert the BytesIO variable to an AudioSegment
        audio_segment = AudioSegment.from_file(audio_stream)

        print("Audio successfully converted to an AudioSegment.")

        return audio_segment
    except Exception as e:
        print("An error occurred:", str(e))
        return jsonify(
            status="error",
            error="Error : function base64_to_audio_segment",
            errorMessage=str(e),
        )
        # return None


def recherche_mots_old(tableau, mots):
    for mot in mots:
        if mot not in tableau:
            return 0  # Retourne 0 si au moins l'un des mots n'est pas trouvé
    return 1  # Retourne 1 si tous les mots sont trouvés


def recherche_mots(text, hotwords):
    """
    Search for hotwords in the text
    if 1 hotword is found, return 1
    """
    for hotword in hotwords:
        if hotword in text:
            return 1
    return 0

def getParams(actionCode, actionText, orderCode):

    params = {
        "actionCode": actionCode,
        "actionText": actionText,
        "orderCode": orderCode,
    }
    return params



