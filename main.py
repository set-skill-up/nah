while True:
    text = input("나 : ")

    if text == "exit":
        break

    print("AI :", analyze(text))
