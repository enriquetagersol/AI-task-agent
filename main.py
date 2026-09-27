from agent import ask_gemini


while True:
    message = input("Tu: ")

    if message.lower() in ["salir", "exit", "quit"]:
        break

    response = ask_gemini(message)

    print("Agente:", response)


	
