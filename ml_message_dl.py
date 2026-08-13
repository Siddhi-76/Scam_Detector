import os
import pickle
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, GlobalAveragePooling1D, Dense, Dropout
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

# Constants
MAX_WORDS = 5000
MAX_LEN = 50
EMBEDDING_DIM = 16

def train_dl_model():
    print("Loading message dataset...")
    df = pd.read_csv("data/messages.csv")
    X = df["message"].astype(str).values
    y = df["label"].values

    print(f"Dataset loaded: {len(X)} samples.")

    # Tokenization
    tokenizer = Tokenizer(num_words=MAX_WORDS, oov_token="<OOV>")
    tokenizer.fit_on_texts(X)
    X_seq = tokenizer.texts_to_sequences(X)
    X_pad = pad_sequences(X_seq, maxlen=MAX_LEN, padding='post', truncating='post')

    # Save tokenizer
    with open("tokenizer.pkl", "wb") as f:
        pickle.dump(tokenizer, f)
    print("Saved tokenizer.pkl")

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X_pad, y, test_size=0.2, random_state=42, stratify=y)

    # Build Model
    model = Sequential([
        Embedding(input_dim=MAX_WORDS, output_dim=EMBEDDING_DIM, input_length=MAX_LEN),
        GlobalAveragePooling1D(),
        Dense(24, activation='relu'),
        Dropout(0.2),
        Dense(1, activation='sigmoid')
    ])

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    model.summary()

    # Train Model
    print("Training model...")
    model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.2, verbose=1)

    # Evaluate Model
    print("\nEvaluating model on test set...")
    loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
    print(f"Test Accuracy: {accuracy:.4f}")

    y_pred = (model.predict(X_test) > 0.5).astype(int).flatten()
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=["Legit", "Scam"]))

    # Save Model
    model.save("message_dl_model.keras")
    print("Model saved as message_dl_model.keras")

if __name__ == "__main__":
    train_dl_model()
