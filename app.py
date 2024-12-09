import gradio as gr
from huggingface_hub import InferenceClient
from qdrant_client import QdrantClient
from qdrant_client.models import FieldCondition, Filter, MatchValue
import numpy as np

hf_token = "HUGGINGFACE_ACCESS_TOKEN"

client = InferenceClient(token=hf_token)

qdrant = QdrantClient(url="http://localhost:6333")

collection_name = "embedded_repositories"
author_id = "079da71d-e359-4988-8605-ba8a2c24f404" # ROS 2

def search_qdrant(query: str, top_k: int = 5):
	embedding = client.feature_extraction(query)

	embedding_avg = embedding.mean(axis=1).flatten()

	embedding_resized = embedding_avg[:384]

	query_filter = Filter(
		must=[
			FieldCondition(
				key="author_id",
				match=MatchValue(value=str(author_id))
			)
		]
	)

	search_result = qdrant.search(
		collection_name=collection_name,
		query_vector=embedding_resized,
		limit=top_k,
		with_payload=True,
		query_filter=query_filter
	)

	documents = [hit.payload["content"] for hit in search_result]

	return documents

def respond(
	message,
	history: list[tuple[str, str]],
	max_tokens,
	temperature,
	top_p
):
	relevant_docs = search_qdrant(message)

	messages = []

	if relevant_docs:
		context = "\n".join(relevant_docs)
		messages.append({"role": "system", "content": f"Here are some relevant documents:\n{context}"})

	for val in history:
		if val[0]:
			messages.append({"role": "user", "content": val[0]})
		if val[1]:
			messages.append({"role": "assistant", "content": val[1]})

	messages.append({"role": "user", "content": message})

	response = ""

	for message in client.chat_completion(
		messages,
		max_tokens=max_tokens,
		stream=True,
		temperature=temperature,
		top_p=top_p,
	):
		token = message.choices[0].delta.content

		response += token

	return response

questions = [
	"Tell me how can I navigate to a specific pose - include replanning aspects in your answer.",
	"Can you provide me with code for this task?"
]

with gr.Blocks() as demo:
	chatbot = gr.Chatbot()

	with gr.Row():
		message_textbox = gr.Textbox(label="Type a message")

	questions_dropdown = gr.Dropdown(choices=[""] + questions, label="Example Questions")

	with gr.Accordion("Additional Inputs", open=False):
		max_tokens_slider = gr.Slider(minimum=1, maximum=2048, value=512, step=1, label="Max new tokens")
		temperature_slider = gr.Slider(minimum=0.1, maximum=4.0, value=0.7, step=0.1, label="Temperature")
		top_p_slider = gr.Slider(
			minimum=0.1,
			maximum=1.0,
			value=0.95,
			step=0.05,
			label="Top-p (nucleus sampling)",
		)

	state_history = gr.State([])

	def submit_message(message, history, max_tokens, temperature, top_p):
		if history is None:
			history = []
		response = respond(message, history, max_tokens, temperature, top_p)
		history.append((message, response))
		return history, history

	def select_question(message, history, max_tokens, temperature, top_p):
		if not message:
			return history, history
		return submit_message(message, history, max_tokens, temperature, top_p)

	message_textbox.submit(
		submit_message,
		inputs=[message_textbox, state_history, max_tokens_slider, temperature_slider, top_p_slider],
		outputs=[chatbot, state_history]
	)

	questions_dropdown.change(
		select_question,
		inputs=[questions_dropdown, state_history, max_tokens_slider, temperature_slider, top_p_slider],
		outputs=[chatbot, state_history]
	)

if __name__ == "__main__":
	demo.launch(server_name="0.0.0.0", server_port=7860)
