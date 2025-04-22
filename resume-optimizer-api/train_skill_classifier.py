import csv
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import MultiLabelBinarizer
from joblib import dump

# === Define skill graph (you can expand this) ===
skill_graph = {
    "Java": ["Spring Boot", "JSF", "JSP"],
    "JavaScript": ["React.js", "Redux", "Node.js"],
    "Python": ["Flask", "Django", "Pandas"],
    "React.js": ["Redux"]
}

# === Full list of skills ===
skill_list = sorted(set([k for k in skill_graph] + [s for subs in skill_graph.values() for s in subs]))

# === Generate training data from skill graph ===
data = []
for base_skill, related_skills in skill_graph.items():
    for i in range(len(related_skills)):
        input_skills = [base_skill] + related_skills[:i]
        suggested = [related_skills[i]]
        data.append({"input_skills": input_skills, "suggested_skills": suggested})

# === Save dataset as CSV ===
rows = []
for entry in data:
    rows.append({
        "input_skills": ",".join(entry["input_skills"]),
        "suggested_skills": ",".join(entry["suggested_skills"])
    })
pd.DataFrame(rows).to_csv("skill_training_data.csv", index=False)

# === Load dataset and prepare binary vectors ===
df = pd.read_csv("skill_training_data.csv")
mlb = MultiLabelBinarizer(classes=skill_list)

X = mlb.fit_transform(df["input_skills"].str.split(","))
y = mlb.transform(df["suggested_skills"].str.split(","))

# === Train/Test split ===
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# === Train classifier ===
base_clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf = MultiOutputClassifier(base_clf)
clf.fit(X_train, y_train)

# === Evaluate ===
y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred, target_names=mlb.classes_))

# === Save model and label binarizer ===
dump(clf, "skill_classifier.joblib")
dump(mlb, "skill_mlb.joblib")

print("\nModel and label binarizer saved successfully.")
