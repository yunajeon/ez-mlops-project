import argparse
import os
from huggingface_hub import snapshot_download

DEFAULT_MODEL_ID = "snunlp/KR-FinBert-SC"

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--model-id", default=DEFAULT_MODEL_ID)
    p.add_argument("--out", default="./models/KR-FinBert-SC")
    args = p.parse_args()

    os.makedirs(args.out, exist_ok=True)
    snapshot_download(
        repo_id=args.model_id,
        local_dir=args.out,
        local_dir_use_symlinks=False
    )
    print(f"Downloaded {args.model_id} to {args.out}")

if __name__ == "__main__":
    main()
