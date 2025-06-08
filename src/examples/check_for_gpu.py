import torch


def check_gpu_availability():
    print("PyTorch version:", torch.__version__)

    if torch.cuda.is_available():
        num_gpus = torch.cuda.device_count()
        print(f"Number of GPUs Available: {num_gpus}")
        for i in range(num_gpus):
            print(f"  - GPU {i}: {torch.cuda.get_device_name(i)}")
        print(f"Current device: {torch.cuda.current_device()}")
    else:
        print("No GPU found. Using CPU.")


if __name__ == "__main__":
    check_gpu_availability()
