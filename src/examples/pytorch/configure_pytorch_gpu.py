import platform

import psutil
import torch


def configure_pytorch_gpu(verbose=True):
    """
    Configure PyTorch to use GPU if available and return device information.

    Args:
    verbose (bool): If True, print detailed information about the configuration.

    Returns:
    torch.device: The device to be used for PyTorch operations.
    """
    # Check if CUDA is available
    if torch.cuda.is_available():
        device = torch.device("cuda")
        if verbose:
            print(f"GPU available: {torch.cuda.get_device_name(0)}")
            print(f"CUDA version: {torch.version.cuda}")
            print(f"Total GPU memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
    # Check if MPS (Metal Performance Shaders) is available for Mac
    elif torch.backends.mps.is_available():
        device = torch.device("mps")
        if verbose:
            print("Apple Silicon GPU available. Using MPS backend.")
    else:
        device = torch.device("cpu")
        if verbose:
            print("No GPU available. Using CPU.")

    # Set default tensor type
    if device.type == "cuda":
        torch.set_default_tensor_type("torch.cuda.FloatTensor")
    elif device.type == "mps":
        torch.set_default_tensor_type("torch.FloatTensor")  # MPS uses default CPU tensor type

    if verbose:
        print(f"\nPyTorch version: {torch.__version__}")
        print(f"Python version: {platform.python_version()}")
        print(f"System: {platform.system()} {platform.release()}")
        print(f"CPU: {platform.processor()}")
        print(f"Number of CPU cores: {psutil.cpu_count(logical=False)}")
        print(f"Total system memory: {psutil.virtual_memory().total / 1e9:.2f} GB")
        print(f"\nPyTorch is configured to use: {device.type.upper()}")

    return device


# Example usage
if __name__ == "__main__":
    device = configure_pytorch_gpu()

    # Example of using the device
    x = torch.randn(3, 3).to(device)
    print(f"\nExample tensor on {device.type}:")
    print(x)
