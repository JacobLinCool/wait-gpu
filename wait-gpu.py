import subprocess
import re
import time
import sys

try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False

def get_free_memory(gpu_uuid):
    try:
        output = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=uuid,memory.free", "--format=csv,noheader"],
            encoding="UTF-8",
        )
        for line in output.splitlines():
            if gpu_uuid in line:
                match = re.search(r"(\S+)\s*,\s*(\d+)", line)
                if match:
                    return int(match.group(2))
        return None
    except subprocess.CalledProcessError as e:
        print("Failed to execute nvidia-smi:", e, file=sys.stderr)
        return None


def main():
    if len(sys.argv) != 5:
        print("Usage: python wait_gpu.py <uuid> <min_memory_mb> --run <command>")
        sys.exit(1)

    gpu_uuid = sys.argv[1]
    min_memory = int(sys.argv[2])
    command = sys.argv[4]

    if TQDM_AVAILABLE:
        with tqdm(desc="Waiting for GPU memory to free up", unit=" check") as pbar:
            while True:
                free_memory = get_free_memory(gpu_uuid)
                pbar.set_postfix_str(f"Current free memory: {free_memory} MB")
                if free_memory is not None and free_memory >= min_memory:
                    break
                time.sleep(1)
                pbar.update(1)
    else:
        print("Waiting for GPU memory to free up")
        while True:
            free_memory = get_free_memory(gpu_uuid)
            print(f"Current free memory: {free_memory} MB")
            if free_memory is not None and free_memory >= min_memory:
                break
            time.sleep(1)

    subprocess.run(command, shell=True)


if __name__ == "__main__":
    main()
