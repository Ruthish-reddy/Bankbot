# train.py — trains intent classifier and saves to bank_nlu_model/
import spacy
from spacy.training.example import Example
import random, os, csv, shutil

CSV_PATH = "C:/Users/ruthi/Downloads/bank  bot/training_and_responses.csv"
MODEL_DIR = "bank_nlu_model"

def load_examples(csv_path=CSV_PATH):
    intent_examples = []
    intents = set()
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for row in reader:
            if len(row) >= 2:
                text, intent = row[0].strip(), row[1].strip()
                if text and intent:
                    intent_examples.append((text, intent))
                    intents.add(intent)
    return intent_examples, sorted(list(intents))

def main():
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(f"{CSV_PATH} not found")

    if os.path.exists(MODEL_DIR):
        shutil.rmtree(MODEL_DIR)
        print("🧹 Removed old model folder.")

    intent_examples, all_intents = load_examples()
    print(f"✅ Loaded {len(intent_examples)} examples, intents: {all_intents}")

    nlp = spacy.load("en_core_web_sm")
    if "textcat" not in nlp.pipe_names:
        textcat = nlp.add_pipe("textcat", last=True)
    else:
        textcat = nlp.get_pipe("textcat")

    for label in all_intents:
        textcat.add_label(label)

    print("🧠 Training...")
    pipe_exceptions = ["textcat"]
    unaffected = [p for p in nlp.pipe_names if p not in pipe_exceptions]

    with nlp.disable_pipes(*unaffected):
        optimizer = nlp.begin_training()
        for epoch in range(12):
            random.shuffle(intent_examples)
            losses = {}
            for text, intent in intent_examples:
                doc = nlp.make_doc(text)
                cats = {lbl: float(lbl == intent) for lbl in all_intents}
                example = Example.from_dict(doc, {"cats": cats})
                nlp.update([example], sgd=optimizer, losses=losses)
            print(f"Epoch {epoch+1:02d}/12 | Losses: {losses}")

    nlp.to_disk(MODEL_DIR)
    print(f"✅ Model saved to {MODEL_DIR}")

if __name__ == "__main__":
    main()
