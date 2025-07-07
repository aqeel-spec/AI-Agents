import chainlit as cl


@cl.on_message
async def chatbot(message: str):
    # Your chatbot logic here
    await cl.Message(content=f"You said: {message.content}").send()