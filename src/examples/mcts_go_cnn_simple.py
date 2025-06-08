"""
This file is based on code from the book "Deep Learning and the Game of Go"
by Max Pumperla and Kevin Ferguson (Manning Publications, 2019).
Original code repository: https://github.com/maxpumperla/deep_learning_and_the_game_of_go

The code may have been modified and adapted for educational purposes.
This was translated to pytorch by Anthropic's Claude 3.5 model.
"""

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from configure_pytorch_gpu import configure_pytorch_gpu
from torch.utils.data import DataLoader, TensorDataset

# Configure GPU and get device
device = configure_pytorch_gpu()

# Set random seed for reproducibility
torch.manual_seed(123)
np.random.seed(123)

# Load data
X = np.load("src/dlgo/generated_games/features-40k.npy")
Y = np.load("src/dlgo/generated_games/labels-40k.npy")

# Preprocess data
samples = X.shape[0]
size = 9
X = X.reshape(samples, 1, size, size)  # PyTorch uses (C, H, W) format
X = torch.FloatTensor(X).to(device)
Y = torch.FloatTensor(Y).to(device)

# Split data
train_samples = int(0.9 * samples)
X_train, X_test = X[:train_samples], X[train_samples:]
Y_train, Y_test = Y[:train_samples], Y[train_samples:]

# Create datasets and dataloaders
train_dataset = TensorDataset(X_train, Y_train)
test_dataset = TensorDataset(X_test, Y_test)
train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=64, shuffle=False)


# Define the model
class GoCNN(nn.Module):
    def __init__(self):
        super(GoCNN, self).__init__()
        self.conv1 = nn.Conv2d(1, 48, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(48, 48, kernel_size=3, padding=1)
        self.flatten = nn.Flatten()
        self.fc1 = nn.Linear(48 * size * size, 512)
        self.fc2 = nn.Linear(512, size * size)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.sigmoid(self.conv1(x))
        x = self.sigmoid(self.conv2(x))
        x = self.flatten(x)
        x = self.sigmoid(self.fc1(x))
        x = self.sigmoid(self.fc2(x))
        return x


model = GoCNN().to(device)

# Define loss function and optimizer
criterion = nn.MSELoss()
optimizer = optim.SGD(model.parameters(), lr=0.01)


# Training loop
def train(model, train_loader, criterion, optimizer, epochs, device):
    model.train()
    for epoch in range(epochs):
        running_loss = 0.0
        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
        print(f"Epoch {epoch+1}/{epochs}, Loss: {running_loss/len(train_loader):.4f}")


def evaluate(model, test_loader, criterion, device):
    model.eval()
    total_loss = 0.0
    correct = 0
    total = 0
    with torch.no_grad():
        for inputs, labels in test_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            total_loss += loss.item()

            # Find the position of the highest probability in outputs and labels
            _, predicted = outputs.max(1)
            _, true_moves = labels.max(1)

            correct += (predicted == true_moves).sum().item()
            total += labels.size(0)

    accuracy = correct / total
    avg_loss = total_loss / len(test_loader)
    return avg_loss, accuracy


# Train the model
train(model, train_loader, criterion, optimizer, epochs=15, device=device)

# Evaluate the model
test_loss, test_accuracy = evaluate(model, test_loader, criterion, device)
print(f"Test loss: {test_loss:.4f}")
print(f"Test accuracy: {test_accuracy:.4f}")
