# wait-gpu

A tiny script to to monitor the available memory on a specific GPU and wait until a minimum threshold of free memory is reached before executing a given command.

## Usage

```bash
python wait_gpu.py <uuid> <min_memory_mb> --run <command>
```

## Example

```bash
python wait_gpu.py GPU-12345678-1234-1234-1234-123456789012 10000 --run "python train.py"
```
