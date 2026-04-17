# 🚀 INTEGRATION GUIDE - Add Intelligent Features to Web App

This guide shows how to integrate the intelligent system into your FastAPI backend and React frontend.

---

## Part 1: Backend Integration (main.py)

### Step 1: Import the Intelligent Services

```python
from ml.ml_service_intelligent import run_intelligent_analysis
from ml.preprocessing import prepare_features_for_analysis
```

### Step 2: Create New Enhanced Analysis Endpoint

```python
@app.post("/analyze-intelligent", tags=["Clustering"])
async def analyze_data_intelligent(file: UploadFile = File(...)):
    contents = await file.read()
    df = pd.read_csv(StringIO(contents.decode()))
    results = run_intelligent_analysis(df)
    return results
```

---

## Part 2: Frontend Integration

Create `IntelligentResults.tsx` and update Analysis.tsx to call `/analyze-intelligent`.

---

## Testing

```bash
curl -X POST http://localhost:8000/analyze-intelligent -F "file=@user_behavior_download.csv"
```

See full guide in previous versions or FINAL_SUMMARY.md.

