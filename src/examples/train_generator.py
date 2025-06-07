import multiprocessing
import os
import traceback

import torch
from torch.utils.data import DataLoader
from tqdm import tqdm

from dlgo.data.processor import GoDataProcessor
from dlgo.data.sequence import DataSequence
from dlgo.encoders.oneplane import OnePlaneEncoder
from dlgo.networks import small


def train(model, device, train_loader, optimizer, criterion, epoch):
    model.train()
    total_loss = 0
    correct = 0
    total = 0
    for batch_idx, (data, target) in enumerate(tqdm(train_loader, desc=f"\033[92mEpoch {epoch} [train]\033[0m")):

        data, target = data.to(device), target.to(device)

        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()
        total_loss += loss.item() * data.size(0)
        pred = output.argmax(dim=1)
        correct += (pred == target).sum().item()
        total += data.size(0)
    avg_loss = total_loss / total
    accuracy = correct / total
    print(f"\033[92mTrain Epoch {epoch}: Loss={avg_loss:.4f}, Accuracy={accuracy:.4f}\033[0m")


def evaluate(model, device, test_loader, criterion):
    model.eval()
    total_loss = 0
    correct = 0
    total = 0
    with torch.no_grad():
        for data, target in tqdm(test_loader, desc="\033[94m[eval]\033[0m"):
            data, target = data.to(device), target.to(device)
            output = model(data)
            loss = criterion(output, target)
            total_loss += loss.item() * data.size(0)
            pred = output.argmax(dim=1)
            correct += (pred == target).sum().item()
            total += data.size(0)
    avg_loss = total_loss / total
    accuracy = correct / total
    print(f"\033[94mTest: Loss={avg_loss:.4f}, Accuracy={accuracy:.4f}\033[0m")
    return avg_loss, accuracy


def main():
    go_board_rows, go_board_cols = 19, 19
    num_classes = go_board_rows * go_board_cols
    num_games = 100
    batch_size = 128
    epochs = 5

    encoder = OnePlaneEncoder((go_board_rows, go_board_cols))
    processor = GoDataProcessor(encoder=encoder.name())

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("Using device:", device)

    try:
        train_data = processor.load_go_data("train", num_games)
        test_data = processor.load_go_data("test", num_games)

        train_dataset = DataSequence(processor.data_dir, train_data, batch_size, num_classes)
        test_dataset = DataSequence(processor.data_dir, test_data, batch_size, num_classes)

        # Print information about the shape of the train_dataset
        print(f"Number of samples in train_dataset: {len(train_dataset) * batch_size}")
        if len(train_dataset) > 0:
            features, labels = train_dataset[0]
            print(f"Shape of features in first batch: {features.shape}")
            print(f"Shape of labels in first batch: {labels.shape}")

        train_loader = DataLoader(train_dataset, batch_size=None, shuffle=True)
        test_loader = DataLoader(test_dataset, batch_size=None, shuffle=False)

        model = small.create_model(encoder, go_board_rows, go_board_cols, num_classes).to(device)
        optimizer = torch.optim.SGD(model.parameters(), lr=0.01, momentum=0.9)
        criterion = torch.nn.CrossEntropyLoss()

        for epoch in range(1, epochs + 1):
            train(model, device, train_loader, optimizer, criterion, epoch)
            evaluate(model, device, test_loader, criterion)

    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()
    finally:
        pass


if __name__ == "__main__":
    multiprocessing.set_start_method("spawn")
    os.environ["OMP_NUM_THREADS"] = "1"
    main()
