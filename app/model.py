import os
import time
import logging
from dataclasses import dataclass
from typing import List, Dict, Tuple

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from .config import settings

logger = logging.getLogger(__name__)

def _softmax(logits: torch.Tensor) -> torch.Tensor:
    return torch.softmax(logits, dim=-1)

@dataclass
class ModelInfo:
    model_id: str
    model_version: str
    labels: Dict[int, str]

class ModelService:
    def __init__(self) -> None:
        self.tokenizer = None
        self.model = None
        self.info: ModelInfo | None = None

    def load(self) -> ModelInfo:
        """Load model/tokenizer from local dir if present; else fallback to HF model_id."""
        t0 = time.time()

        model_source = settings.model_dir if os.path.isdir(settings.model_dir) else settings.model_id
        logger.info("Loading model", extra={"model_source": model_source})

        self.tokenizer = AutoTokenizer.from_pretrained(model_source, use_fast=True)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_source)
        self.model.eval()

        # CPU inference by default
        self.model.to("cpu")

        labels = {}
        if hasattr(self.model.config, "id2label") and self.model.config.id2label:
            labels = {int(k): v for k, v in self.model.config.id2label.items()}
        else:
            labels = {i: f"LABEL_{i}" for i in range(self.model.config.num_labels)}

        # Try to derive a stable model version for observability
        model_version = os.getenv("MODEL_VERSION", "unknown")
        # If we have a local dir, hash its contents lightly (mtime+size) for uniqueness
        if os.path.isdir(settings.model_dir) and model_version == "unknown":
            model_version = self._dir_fingerprint(settings.model_dir)

        self.info = ModelInfo(
            model_id=settings.model_id,
            model_version=model_version,
            labels=labels
        )

        logger.info("Model loaded", extra={"elapsed_s": round(time.time() - t0, 3), "model_version": model_version})
        return self.info

    def _dir_fingerprint(self, path: str) -> str:
        import hashlib, os
        h = hashlib.sha256()
        for root, _, files in os.walk(path):
            for fn in sorted(files):
                fp = os.path.join(root, fn)
                try:
                    st = os.stat(fp)
                    h.update(fn.encode("utf-8"))
                    h.update(str(st.st_size).encode("utf-8"))
                    h.update(str(int(st.st_mtime)).encode("utf-8"))
                except OSError:
                    continue
        return h.hexdigest()[:12]

    @torch.inference_mode()
    def predict(self, texts: List[str], return_all_scores: bool = True) -> List[Tuple[str, str, float, Dict[str, float]]]:
        assert self.model is not None and self.tokenizer is not None and self.info is not None

        # Tokenize as batch
        enc = self.tokenizer(
            texts,
            padding=True,
            truncation=True,
            max_length=settings.max_length,
            return_tensors="pt"
        )

        enc = {k: v.to("cpu") for k, v in enc.items()}
        logits = self.model(**enc).logits  # (B, C)
        probs = _softmax(logits)

        results = []
        for i, text in enumerate(texts):
            p = probs[i].detach().cpu()
            top_idx = int(torch.argmax(p).item())
            top_label = self.info.labels.get(top_idx, str(top_idx))
            top_score = float(p[top_idx].item())

            scores = {self.info.labels.get(j, str(j)): float(p[j].item()) for j in range(p.shape[0])} if return_all_scores else {}
            results.append((text, top_label, top_score, scores))
        return results
