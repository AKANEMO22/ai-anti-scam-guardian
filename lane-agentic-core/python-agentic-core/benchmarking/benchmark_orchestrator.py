import asyncio
import json
import os
import sys
import time
from typing import List

# Setup path to import app modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.orchestrator import OrchestratorService
from app.models.contracts import SignalPayload, SourceType

# Mock Storage Client to avoid dependency on running database
class MockStorageClient:
    async def forward_search_query_to_storage_for_threat_agent(self, query, source_type, top_k):
        return []
    def sync_agentic_metadata_to_storage(self, sessionId, metadata):
        pass

async def load_and_bench(data_path: str, limit: int = 50):
    print(f"Loading data from {data_path}...")
    with open(data_path, 'r') as f:
        # ai-in-the-loop datasets use JSON line format or nested JSON
        # Loading correctly based on observation of ssc_dataset_all_data.chat.json
        try:
            # Try loading as list of JSON objects (some exports are like this)
            raw_data = json.load(f)
        except json.JSONDecodeError:
            # Fallback to JSONL
            f.seek(0)
            raw_data = [json.loads(line) for line in f if line.strip()]

    # Filter/Sample
    test_samples = raw_data[:limit]
    
    # Initialize Orchestrator with mock storage
    orchestrator = OrchestratorService()
    orchestrator.storage_client = MockStorageClient()
    
    results = []
    
    print(f"Bencmarking {len(test_samples)} samples...")
    start_time = time.time()
    
    for i, item in enumerate(test_samples):
        # Extract content from conversation
        # ai-in-the-loop format: {"id": X, "eval_scam_risk": [{"instruction": ..., "input": "User: ...\nAgent: ..."}]}
        # or simplified format with label
        
        # We'll use the 'eval_scam_risk' input field which contains the text
        try:
            sample_input = item.get("eval_scam_risk", [{}])[0].get("input", "")
            label = item.get("output", 0) # 1 = scam, 0 = safe (based on scores.csv logic)
            
            if not sample_input:
                continue

            payload = SignalPayload(
                sourceType=SourceType.SMS,
                text=sample_input,
                metadata={}
            )
            
            response = await orchestrator.process_pipeline_request(payload)
            
            results.append({
                "id": item.get("id"),
                "actual": label,
                "predicted": 1 if response.riskScore >= 70 else 0,
                "score": response.riskScore,
                "pii": response.piiScore,
                "engagement": response.engagementScore
            })
            
            print(f"[{i+1}/{len(test_samples)}] ID: {item.get('id')} - Label: {label} - Pred: {results[-1]['predicted']} ({response.riskScore}%)")
            
            # Wait for rate limit (Free tier is extremely limited in this environment)
            await asyncio.sleep(60)
            
        except Exception as e:
            print(f"Error processing sample {i}: {e}")

    end_time = time.time()
    duration = end_time - start_time
    
    # Calculate Metrics
    tp = sum(1 for r in results if r["actual"] == 1 and r["predicted"] == 1)
    fp = sum(1 for r in results if r["actual"] == 0 and r["predicted"] == 1)
    tn = sum(1 for r in results if r["actual"] == 0 and r["predicted"] == 0)
    fn = sum(1 for r in results if r["actual"] == 1 and r["predicted"] == 0)
    
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    accuracy = (tp + tn) / len(results) if results else 0
    
    summary = {
        "dataset": os.path.basename(data_path),
        "samples": len(results),
        "duration_seconds": duration,
        "metrics": {
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1_score": f1,
            "tp": tp, "fp": fp, "tn": tn, "fn": fn
        }
    }
    
    print("\n" + "="*30)
    print("BENCHMARK SUMMARY")
    print("="*30)
    print(json.dumps(summary, indent=2))
    
    with open("benchmarking/results.json", "w") as f:
        json.dump(summary, f, indent=2)

if __name__ == "__main__":
    # Use absolute path to avoid confusion
    PROJECT_ROOT = "/Users/ngovietthanhbinh/Project/AI-Anti-Scam-Guardian"
    DATA_PATH = os.path.join(PROJECT_ROOT, "ai-in-the-loop/data/classification/all_eval_data/zero-shot/ssc_dataset_all_data.chat.json")
    
    if not os.path.exists(DATA_PATH):
        print(f"Error: Dataset not found at {DATA_PATH}")
        sys.exit(1)
        
    asyncio.run(load_and_bench(DATA_PATH, limit=3))
