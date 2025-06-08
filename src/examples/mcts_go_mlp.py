"""
This file is based on code from the book "Deep Learning and the Game of Go"
by Max Pumperla and Kevin Ferguson (Manning Publications, 2019).
Original code repository: https://github.com/maxpumperla/deep_learning_and_the_game_of_go

The code may have been modified and adapted for educational purposes.
"""

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

# Set random seed for reproducibility
torch.manual_seed(123)
np.random.seed(123)

# Load data
X = np.load("src/dlgo/generated_games/features-40k.npy")
Y = np.load("src/dlgo/generated_games/labels-40k.npy")

samples = X.shape[0]
board_size = 9 * 9

X = X.reshape(samples, board_size)
Y = Y.reshape(samples, board_size)

# Split data
train_samples = int(0.9 * samples)
X_train, X_test = X[:train_samples], X[train_samples:]
Y_train, Y_test = Y[:train_samples], Y[train_samples:]

# Convert to PyTorch tensors
X_train = torch.FloatTensor(X_train)
Y_train = torch.FloatTensor(Y_train)
X_test = torch.FloatTensor(X_test)
Y_test = torch.FloatTensor(Y_test)

# Create DataLoader
train_dataset = TensorDataset(X_train, Y_train)
test_dataset = TensorDataset(X_test, Y_test)
train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=64, shuffle=False)

# Get cpu, gpu or mps device for training.
device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
print(f"Using {device} device")


# Define the model
class Net(nn.Module):
    def __init__(self, input_size, hidden1_size, hidden2_size, output_size):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden1_size)
        self.fc2 = nn.Linear(hidden1_size, hidden2_size)
        self.fc3 = nn.Linear(hidden2_size, output_size)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.sigmoid(self.fc1(x))
        x = self.sigmoid(self.fc2(x))
        x = self.sigmoid(self.fc3(x))
        return x


# Instantiate the model
model = Net(board_size, 1000, 500, board_size).to(device)

# Define loss function and optimizer
criterion = nn.MSELoss()
optimizer = optim.SGD(model.parameters(), lr=0.01)

# Training loop
num_epochs = 15
for epoch in range(num_epochs):
    model.train()
    for batch_X, batch_y in train_loader:
        optimizer.zero_grad()
        outputs = model(batch_X)
        loss = criterion(outputs, batch_y)
        loss.backward()
        optimizer.step()

    # Print epoch results
    model.eval()
    with torch.no_grad():
        test_loss = 0
        correct = 0
        total = 0
        for batch_X, batch_y in test_loader:
            outputs = model(batch_X)
            test_loss += criterion(outputs, batch_y).item()
            predicted = (outputs > 0.5).float()
            total += batch_y.size(0) * batch_y.size(1)
            correct += (predicted == batch_y).sum().item()

        accuracy = correct / total
        print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {test_loss:.4f}, Accuracy: {accuracy:.4f}")

# Final evaluation
model.eval()
with torch.no_grad():
    test_loss = 0
    correct = 0
    total = 0
    for batch_X, batch_y in test_loader:
        outputs = model(batch_X)
        test_loss += criterion(outputs, batch_y).item()
        predicted = (outputs > 0.5).float()
        total += batch_y.size(0) * batch_y.size(1)
        correct += (predicted == batch_y).sum().item()

    accuracy = correct / total
    print(f"Test loss: {test_loss:.4f}")
    print(f"Test accuracy: {accuracy:.4f}")
