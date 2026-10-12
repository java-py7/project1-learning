import tiktoken
tokenizer = tiktoken.encoding_for_model("gpt-4o")

test_inputs = [
    ("Hello world"),
    ("Hello, world!"),
    ("Hello    world"),
    ("123456789"),
    ("😀🚀🔥"),
]

for text in test_inputs:
    tokens = tokenizer.encode(text)

    print("Input:", repr(text))
    print("Token Count:", len(tokens))
    print("-" * 40)