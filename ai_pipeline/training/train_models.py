import os
import sys
import json
import joblib
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

# Set UTF-8 output encoding for Windows compatibility
if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8")

def prepare_features(df):
    """Combines sender, subject, and body into a rich text representation."""
    return df['sender_name'].fillna('') + " " + df['sender'] + " " + df['subject'] + " " + df['body']

def train_and_evaluate_all():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
    
    data_dir = os.path.join(project_root, "dataset")
    saved_models_dir = os.path.join(project_root, "ai_pipeline", "saved_models")
    os.makedirs(saved_models_dir, exist_ok=True)
    
    train_path = os.path.join(data_dir, "train_benchmark.csv")
    test_path = os.path.join(data_dir, "test_benchmark.csv")
    
    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)
    
    X_train = prepare_features(train_df)
    X_test = prepare_features(test_df)
    
    print("\n" + "="*75)
    print("  TRAINING & SAVING ALL .PKL MODELS TO ai_pipeline/saved_models/")
    print("="*75)

    # 1. TF-IDF Vectorizer
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        sublinear_tf=True,
        max_features=5000,
        stop_words='english'
    )
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    
    def save_pkl(obj, filename):
        target_path = os.path.join(saved_models_dir, filename)
        joblib.dump(obj, target_path)
        print(f"  [SAVED] {filename:<30} -> {target_path}")

    save_pkl(vectorizer, "tfidf_vectorizer.pkl")

    results = {}

    # 2. Spam Classifier
    y_train_spam = train_df['is_spam'].astype(str)
    y_test_spam = test_df['is_spam'].astype(str)
    clf_spam = LogisticRegression(C=10.0, class_weight='balanced', max_iter=1000)
    clf_spam.fit(X_train_vec, y_train_spam)
    y_pred_spam = clf_spam.predict(X_test_vec)
    acc_spam = accuracy_score(y_test_spam, y_pred_spam)
    prec_spam, rec_spam, f1_spam, _ = precision_recall_fscore_support(y_test_spam, y_pred_spam, average='weighted', zero_division=0)
    results['Spam Detection'] = {"accuracy": acc_spam, "precision": prec_spam, "recall": rec_spam, "f1": f1_spam}
    save_pkl(clf_spam, "spam_classifier.pkl")

    # 3. Category Classifier
    y_train_cat = train_df['category']
    y_test_cat = test_df['category']
    clf_cat = LogisticRegression(C=15.0, class_weight='balanced', max_iter=1000)
    clf_cat.fit(X_train_vec, y_train_cat)
    y_pred_cat = clf_cat.predict(X_test_vec)
    acc_cat = accuracy_score(y_test_cat, y_pred_cat)
    prec_cat, rec_cat, f1_cat, _ = precision_recall_fscore_support(y_test_cat, y_pred_cat, average='weighted', zero_division=0)
    results['Email Classification'] = {"accuracy": acc_cat, "precision": prec_cat, "recall": rec_cat, "f1": f1_cat}
    save_pkl(clf_cat, "category_classifier.pkl")

    # 4. Actionable Classifier
    y_train_act = train_df['is_actionable'].astype(str)
    y_test_act = test_df['is_actionable'].astype(str)
    clf_act = LogisticRegression(C=10.0, class_weight='balanced', max_iter=1000)
    clf_act.fit(X_train_vec, y_train_act)
    y_pred_act = clf_act.predict(X_test_vec)
    acc_act = accuracy_score(y_test_act, y_pred_act)
    prec_act, rec_act, f1_act, _ = precision_recall_fscore_support(y_test_act, y_pred_act, average='weighted', zero_division=0)
    results['Actionable Intent'] = {"accuracy": acc_act, "precision": prec_act, "recall": rec_act, "f1": f1_act}
    save_pkl(clf_act, "actionable_classifier.pkl")

    # 5. Priority Classifier
    y_train_prio = train_df['priority']
    y_test_prio = test_df['priority']
    clf_prio = LogisticRegression(C=12.0, class_weight='balanced', max_iter=1000)
    clf_prio.fit(X_train_vec, y_train_prio)
    y_pred_prio = clf_prio.predict(X_test_vec)
    acc_prio = accuracy_score(y_test_prio, y_pred_prio)
    prec_prio, rec_prio, f1_prio, _ = precision_recall_fscore_support(y_test_prio, y_pred_prio, average='weighted', zero_division=0)
    results['Priority Assignment'] = {"accuracy": acc_prio, "precision": prec_prio, "recall": rec_prio, "f1": f1_prio}
    save_pkl(clf_prio, "priority_classifier.pkl")

    # 6. Approval Classifier
    y_train_appr = train_df['requires_human_approval'].astype(str)
    y_test_appr = test_df['requires_human_approval'].astype(str)
    clf_appr = LogisticRegression(C=10.0, class_weight='balanced', max_iter=1000)
    clf_appr.fit(X_train_vec, y_train_appr)
    y_pred_appr = clf_appr.predict(X_test_vec)
    acc_appr = accuracy_score(y_test_appr, y_pred_appr)
    prec_appr, rec_appr, f1_appr, _ = precision_recall_fscore_support(y_test_appr, y_pred_appr, average='weighted', zero_division=0)
    results['Human-in-the-Loop Approval'] = {"accuracy": acc_appr, "precision": prec_appr, "recall": rec_appr, "f1": f1_appr}
    save_pkl(clf_appr, "approval_classifier.pkl")

    # 7. Action Type Classifier
    y_train_acttype = train_df['action_type']
    y_test_acttype = test_df['action_type']
    clf_acttype = LogisticRegression(C=10.0, class_weight='balanced', max_iter=1000)
    clf_acttype.fit(X_train_vec, y_train_acttype)
    y_pred_acttype = clf_acttype.predict(X_test_vec)
    acc_acttype = accuracy_score(y_test_acttype, y_pred_acttype)
    prec_acttype, rec_acttype, f1_acttype, _ = precision_recall_fscore_support(y_test_acttype, y_pred_acttype, average='weighted', zero_division=0)
    results['Action Type Decision'] = {"accuracy": acc_acttype, "precision": prec_acttype, "recall": rec_acttype, "f1": f1_acttype}
    save_pkl(clf_acttype, "action_type_classifier.pkl")

    print("\n" + "="*75)
    print("  ALL 7 .PKL MODELS SAVED CLEANLY IN ai_pipeline/saved_models/")
    print("="*75 + "\n")

if __name__ == "__main__":
    train_and_evaluate_all()
