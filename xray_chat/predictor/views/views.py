import pandas as pd
from PIL import Image
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
import torch
import torch.nn as nn
import torchvision.models as models
import torch.optim as optim
from django.http import JsonResponse
from collections import Counter


class VQADataset(Dataset):
    def _init_(self, csv_file, transform=None, tokenizer=None, answer_to_idx=None):
        self.data = pd.read_csv(csv_file)
        self.transform = transform
        self.tokenizer = tokenizer
        self.answer_to_idx = answer_to_idx or self.build_answer_vocab()

    def build_answer_vocab(self):
        answers = self.data['answer'].unique()
        return {ans: idx for idx, ans in enumerate(answers)}

    def _len_(self):
        return len(self.data)

    def _getitem_(self, idx):
        img = Image.open(self.data.iloc[idx]['image_path']).convert('RGB')
        question = self.data.iloc[idx]['question']
        answer = self.data.iloc[idx]['answer']

        if self.transform:
            img = self.transform(img)

        # Simple tokenization: lowercase words split by space
        tokens = self.tokenizer(question)

        return img, tokens, self.answer_to_idx[answer]

class VQAModel(nn.Module):
    def _init_(self, vocab_size, answer_size, embedding_dim=128, hidden_dim=256):
        super(VQAModel, self)._init_()
        self.resnet = models.resnet50(pretrained=True)
        self.resnet.fc = nn.Identity()  # Remove classification head

        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, batch_first=True)

        self.fc = nn.Sequential(
            nn.Linear(2048 + hidden_dim, 512),
            nn.ReLU(),
            nn.Linear(512, answer_size)
        )

    def forward(self, image, question_tokens):
        with torch.no_grad():
            img_features = self.resnet(image)

        embedded = self.embedding(question_tokens)
        _, (hn, _) = self.lstm(embedded)
        q_features = hn.squeeze(0)

        combined = torch.cat((img_features, q_features), dim=1)
        out = self.fc(combined)
        return out

def simple_tokenizer(q):
    return [word.lower() for word in q.split()]

def build_vocab(questions, min_freq=1):
    counter = Counter()
    for q in questions:
        counter.update(simple_tokenizer(q))
    vocab = {word: idx + 1 for idx, (word, freq) in enumerate(counter.items()) if freq >= min_freq}
    vocab['<pad>'] = 0
    return vocab

def pad_sequence(tokens, max_len, pad_idx=0):
    return tokens[:max_len] + [pad_idx] * max(0, max_len - len(tokens))

def train_model(request):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    csv_path = '../fracture_qa.csv'

    df = pd.read_csv(csv_path)
    vocab = build_vocab(df['question'])
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
    ])
    tokenizer = lambda q: [vocab.get(t, 0) for t in simple_tokenizer(q)]

    dataset = VQADataset(csv_path, transform=transform, tokenizer=tokenizer)
    loader = DataLoader(dataset, batch_size=16, shuffle=True)

    model = VQAModel(vocab_size=len(vocab), answer_size=len(dataset.answer_to_idx)).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=1e-4)

    EPOCHS = 100
    for epoch in range(EPOCHS):
        model.train()
        total_loss = 0
        correct = 0
        total = 0

        for imgs, questions, answers in loader:
            imgs, answers = imgs.to(device), answers.to(device)
            questions = [pad_sequence(q, 20) for q in questions]
            questions = torch.tensor(questions).to(device)

            output = model(imgs, questions)
            loss = criterion(output, answers)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

            # Calculate accuracy
            _, predicted = torch.max(output.data, 1)
            correct += (predicted == answers).sum().item()
            total += answers.size(0)

        epoch_accuracy = 100 * correct / total
        print(f"Epoch {epoch+1}/{EPOCHS}, Loss: {total_loss:.4f}, Accuracy: {epoch_accuracy:.2f}%")

    torch.save({
        'model_state': model.state_dict(),
        'vocab': vocab,
        'answer_to_idx': dataset.answer_to_idx
    }, 'models/vqa_model.pth')

    return JsonResponse({'status': 'Model trained and saved'})


def predict_answer(request):
    import json
    from PIL import Image

    image_path = request.GET.get('image_path')  # or via POST
    question = request.GET.get('question')

    checkpoint = torch.load('models/vqa_model.pth')
    vocab = checkpoint['vocab']
    answer_to_idx = checkpoint['answer_to_idx']
    idx_to_answer = {v: k for k, v in answer_to_idx.items()}

    tokenizer = lambda q: [vocab.get(t, 0) for t in simple_tokenizer(q)]
    tokens = pad_sequence(tokenizer(question), 20)
    tokens = torch.tensor([tokens])

    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
    ])
    image = transform(Image.open(image_path).convert("RGB")).unsqueeze(0)

    model = VQAModel(len(vocab), len(answer_to_idx))
    model.load_state_dict(checkpoint['model_state'])
    model.eval()

    with torch.no_grad():
        output = model(image, tokens)
        pred_idx = output.argmax(dim=1).item()
        answer = idx_to_answer[pred_idx]

    return JsonResponse({'answer': answer})