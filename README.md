# Cursor chat viewer

This project lets you view exported [Cursor](https://cursor.com/home) chats.

Cursor lets you export a whole chat thread the editor. However, it doesn't have a way to import chats.
Sometimes it's instructive for us view the contents of someone else's chat thread
(either to see how they use AI, or to get a better of their thought process throughout an implementation).
The string-delimited markdown files Cursor exports are a pain to read because there's no distinction between
a user message and an agent response at a glance. This project remedies that by providing a chat-like display
for exported chats.

**NOTE:** This was quickly vibe coded in Claude web. It was intended for personal use,
but we figured it might be useful to someone else. Just know the HTML file is messy.

## What's in this project?

- [convert.py](convert.py): Converts an exported Cursor chat to a structured, usable JSON format.
- [index.html](index.html): Single-file UI to upload and view Cursor chats locally. This also implements the markdown -> JSON conversion, so you can just upload files and view them directly.

## Usage

> The Python conversion file has no dependencies. However, if you open the HTML directly in your local browser, you'll need
> internet access so [prismJS syntax highter](https://prismjs.com/) downloads properly.

- If you just want to open and view an exported Cursor chat, load [index.html](index.html) in your browser and upload a chat markdown file.
- If you want to convert a chat to JSON for some other purpose, run `python convert.py <path_to_chat_file>`.

### Example conversion output

```json
{
  "title": "Implement context pool for browser contexts",
  "metadata_string": "_Exported on 11/17/2025 at 15:33:25 CST from Cursor (2.0.77)_",
  "messages": [
    {
      "markdown_content": "I need help implementing a context pool for managing browser contexts in Playwright. Can you help me design this?",
      "designator": "user"
    },
    {
      "markdown_content": "Yes, ... <rest of response>",
      "designator": "agent_response"
    },
    {
      "markdown_content": "Looks good so far. However, I need to change XYZ ...",
      "designator": "user"
    },
    {
      "markdown_content": "I'll update X, Y, and Z ... <rest of response>",
      "designator": "agent_response"
    }
  ]
}
```
