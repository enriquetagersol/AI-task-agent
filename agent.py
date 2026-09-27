import urllib.request
import urllib.error
import json

from tools_schemas import TOOLS
from tools import get_tasks, add_tasks, complete_task, delete_task
from instructions import SYSTEM_INSTRUCTION


AVAILABLE_TOOLS = {
    "get_tasks": get_tasks,
    "add_tasks": add_tasks,
    "complete_task": complete_task,
    "delete_task": delete_task
}


# Memoria conversacional de la sesión
conversation = []


with open(".env", "r") as file:
    api_key = file.read().split("=", 1)[1].strip()


url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent"


def ask_gemini(message):

    # Guardamos el mensaje del usuario
    conversation.append(
        {
            "role": "user",
            "parts": [
                {"text": message}
            ]
        }
    )

    data = {
        "systemInstruction": {
            "parts": [
                {"text": SYSTEM_INSTRUCTION}
            ]
        },
        "contents": conversation,
        "tools": TOOLS
    }

    try:

        while True:

            body = json.dumps(data).encode("utf-8")

            request = urllib.request.Request(
                url,
                data=body,
                headers={
                    "Content-Type": "application/json",
                    "x-goog-api-key": api_key
                },
                method="POST"
            )

            # Llamamos a Gemini
            with urllib.request.urlopen(request) as response:
                result = response.read()

            result = json.loads(result.decode("utf-8"))

            content = result["candidates"][0]["content"]
            part = content["parts"][0]

            # Guardamos la respuesta de Gemini
            conversation.append(content)

            # Si Gemini pide una tool
            if "functionCall" in part:
                function_call = part["functionCall"]

                name = function_call["name"]
                args = function_call.get("args", {})

                # Ejecutamos la función Python
                function = AVAILABLE_TOOLS[name]
                tool_result = function(**args)

                # Guardamos el resultado de la tool
                conversation.append(
                    {
                        "role": "user",
                        "parts": [
                            {
                                "functionResponse": {
                                    "id": function_call["id"],
                                    "name": name,
                                    "response": {
                                        "result": tool_result
                                    }
                                }
                            }
                        ]
                    }
                )

                # No hacemos return.
                # El while vuelve a llamar a Gemini.
                continue

            # Si Gemini ya responde con texto,
            # hemos terminado este turno.
            return part["text"]

    except urllib.error.HTTPError as error:
    	if error.code == 429:
        	return {
            	"error": True,
            	"type": "rate_limit"
        	}

    	if error.code == 503:
        	return {
            	"error": True,
            	"type": "service_unavailable"
        	}

    	return {
        	"error": True,
        	"type": "api_error"
    	}