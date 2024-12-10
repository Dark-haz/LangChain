
from google.auth import compute_engine
from google.cloud import firestore
from langchain_google_firestore import FirestoreChatMessageHistory


PROJECT_ID = "fir-test-ee6a3"
SESSION_ID = "user_session_new"
COLLECTION_NAME = "chat_history"

client = firestore.Client(
    project=PROJECT_ID
)

history = FirestoreChatMessageHistory(
    session_id=SESSION_ID, collection=COLLECTION_NAME, client=client
)