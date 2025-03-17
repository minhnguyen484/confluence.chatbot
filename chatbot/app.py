from flask import Flask, request, render_template, jsonify, Response
from query_engine import get_context_docs

from langchain_openai import OpenAI
from langchain.chains.question_answering import load_qa_chain

app = Flask(__name__)

def stream_response(query):    
    context_docs = get_context_docs(query)

    llm = OpenAI(streaming=True)
    chain = load_qa_chain(llm, chain_type="map_reduce")

    def generate():
        for chunk in chain.stream({"input_documents": context_docs, "question": query}):
            yield f"data: {chunk}\n\n".encode("utf-8")  # Convert to bytes and format for SSE

    return Response(generate(), content_type="text/event-stream")  # Use SSE for streaming

@app.route('/', methods=['GET'])
def index():    
    return render_template('index.html')

@app.route('/stream')
def stream():
    question = request.args.get('question', '')
    return stream_response(question)

if __name__ == '__main__':
    app.run()