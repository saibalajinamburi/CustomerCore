import os
import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_curve, auc, confusion_matrix, accuracy_score, f1_score, recall_score, precision_score
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt

def train():
    print("Pre-training steps...")
    print("Generating synthetic customer churn data...")
    
    # Generate synthetic dataset
    np.random.seed(42)
    n_samples = 1000
    
    usage_frequency = np.random.randint(1, 31, n_samples)
    support_tickets = np.random.poisson(lam=2, size=n_samples)
    active_users = np.random.randint(1, 10, n_samples)
    contract_months = np.random.choice([1, 12, 24], size=n_samples)
    monthly_spend = np.random.normal(loc=100, scale=30, size=n_samples)
    
    # Calculate churn probability based on features
    churn_prob = (
        0.3 * (support_tickets / 5.0) 
        - 0.2 * (usage_frequency / 30.0) 
        - 0.1 * active_users 
        - 0.4 * (contract_months / 24.0) 
        + 0.1 * (monthly_spend / 100.0)
    )
    # Add noise
    churn_prob += np.random.normal(loc=0, scale=0.2, size=n_samples)
    churn = (churn_prob > 0).astype(int)
    
    df = pd.DataFrame({
        "usage_frequency": usage_frequency,
        "support_tickets_opened": support_tickets,
        "active_users": active_users,
        "contract_months": contract_months,
        "monthly_spend": monthly_spend,
        "churn": churn
    })
    
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/churn_dataset.csv", index=False)
    print("Saved synthetic dataset to data/churn_dataset.csv")
    
    X = df.drop(columns=["churn"])
    y = df["churn"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training Random Forest Churn Predictor...")
    clf = RandomForestClassifier(random_state=42)
    clf.fit(X_train, y_train)
    
    y_pred = clf.predict(X_test)
    y_proba = clf.predict_proba(X_test)[:, 1]
    
    # Compute metrics
    fpr, tpr, _ = roc_curve(y_test, y_proba)
    roc_auc = auc(fpr, tpr)
    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    
    metrics = {
        "auc": round(float(roc_auc), 3),
        "accuracy": round(float(acc), 3),
        "f1_score": round(float(f1), 3),
        "recall": round(float(rec), 3),
        "precision": round(float(prec), 3)
    }
    
    print("Evaluated Metrics:", metrics)
    
    os.makedirs("data", exist_ok=True)
    with open("data/metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)
        
    # Generate Plots
    print("Generating ROC Curve...")
    plt.figure(figsize=(6, 5))
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.3f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic (ROC)')
    plt.legend(loc="lower right")
    plt.tight_layout()
    plt.savefig("data/roc_curve.png", dpi=150)
    plt.close()
    
    print("Generating Confusion Matrix...")
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(5, 4))
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title('Confusion Matrix')
    plt.colorbar()
    tick_marks = np.arange(2)
    plt.xticks(tick_marks, ['No Churn', 'Churn'])
    plt.yticks(tick_marks, ['No Churn', 'Churn'])
    
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            plt.text(j, i, format(cm[i, j], 'd'),
                     ha="center", va="center",
                     color="white" if cm[i, j] > thresh else "black")
                     
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.tight_layout()
    plt.savefig("data/confusion_matrix.png", dpi=150)
    plt.close()

    print("Generating Feature Importance Plot...")
    importances = clf.feature_importances_
    indices = np.argsort(importances)
    plt.figure(figsize=(6, 4))
    plt.title('Feature Importances')
    plt.barh(range(len(indices)), importances[indices], color='b', align='center')
    plt.yticks(range(len(indices)), [X.columns[i] for i in indices])
    plt.xlabel('Relative Importance')
    plt.tight_layout()
    plt.savefig("data/feature_importance.png", dpi=150)
    plt.close()
    
    print("Training completed successfully!")

if __name__ == "__main__":
    train()
