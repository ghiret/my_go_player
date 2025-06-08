import torch


def validate_gpu():
    print("PyTorch version:", torch.__version__)

    # Check for available devices
    if torch.cuda.is_available():
        num_gpus = torch.cuda.device_count()
        print(f"\nNumber of CUDA GPUs available: {num_gpus}")
        for i in range(num_gpus):
            print(f"  GPU {i}: {torch.cuda.get_device_name(i)}")

        # Try to create a simple Torch operation on the GPU
        try:
            device = torch.device("cuda:0")
            a = torch.tensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]], device=device)
            b = torch.tensor([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]], device=device)
            c = torch.matmul(a, b)
            print("\nSuccessfully performed a GPU operation.")
            print("Result:", c.cpu().numpy())
        except RuntimeError as e:
            print("\nFailed to perform GPU operation:", str(e))
    else:
        print("\nNo CUDA GPUs found. PyTorch will use CPU.")
        device = torch.device("cpu")
        a = torch.tensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]], device=device)
        b = torch.tensor([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]], device=device)
        c = torch.matmul(a, b)
        print("\nPerformed operation on CPU. Result:", c.numpy())


if __name__ == "__main__":
    validate_gpu()
