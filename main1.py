from llm import analyze

while True:

    text = input("나: ")

    if text.lower() == "exit":
        break

    result = analyze(text)

    print("AI :", result["reply"])
    emotion = result["emotion"]
    confidence = result["confidence"]

    print(f"(내부) emotion={emotion}, confidence={confidence}")
