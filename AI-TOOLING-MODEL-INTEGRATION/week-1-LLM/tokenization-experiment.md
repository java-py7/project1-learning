# **Tokenization Experiment Output & Explanation**

## Output

Input: 'Hello world'
Token Count: 2
----------------------------------------
Input: 'Hello, world!'
Token Count: 4
----------------------------------------
Input: 'Hello    world'
Token Count: 3
----------------------------------------
Input: '123456789'
Token Count: 3
----------------------------------------
Input: '😀🚀🔥'
Token Count: 4
----------------------------------------

## Explanation

| Input | Token count | Why? |
| :--- | :---: | :--- |
| Hello world | 2 | Each word is represented by one token. |
| Hello, world! | 4 | The comma and exclamation mark increase the token count. |
| Hello    world | 3 | Multiple spaces affect how the text is tokenized. |
| 123456789 | 3 | The number is split into multiple tokens. |
| 😀🚀🔥 | 4 | The emojis are represented by multiple tokens. |

Token count depends on the text and the tokenizer.
Words do not always correspond to individual tokens.
Punctuation, whitespace, numbers, and emojis can affect
how text is divided into tokens.
