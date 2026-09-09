import os
import sys
import joblib

# Set UTF-8 output encoding for Windows compatibility
if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8")

def verify_all_models():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
    models_dir = os.path.join(project_root, "ai_pipeline", "saved_models")
    
    expected_files = [
        "tfidf_vectorizer.pkl",
        "spam_classifier.pkl",
        "category_classifier.pkl",
        "actionable_classifier.pkl",
        "priority_classifier.pkl",
        "approval_classifier.pkl",
        "action_type_classifier.pkl"
    ]
    
    print("\n" + "="*70)
    print("  VERIFYING ALL .PKL MODEL ARTIFACTS")
    print("="*70)
    print(f"Checking Directory: {models_dir}\n")
    
    all_ok = True
    for fname in expected_files:
        fpath = os.path.join(models_dir, fname)
        if os.path.exists(fpath):
            size_kb = os.path.getsize(fpath) / 1024.0
            model_obj = joblib.load(fpath)
            model_type = type(model_obj).__name__
            print(f"  {fname:<30} | Size: {size_kb:>6.1f} KB | Loaded: {model_type}")
        else:
            print(f"  {fname:<30} | NOT FOUND")
            all_ok = False
            
    print("="*70)
    if all_ok:
        print("  ALL 7 .PKL MODELS ARE PRESENT, VALID, AND LOADABLE!")
    else:
        print("  SOME MODELS ARE MISSING.")
    print("="*70 + "\n")

if __name__ == "__main__":
    verify_all_models()
