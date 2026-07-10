from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

from dataset import generate_dataset
from features import create_features

# dataset
df = generate_dataset(2000)
df = create_features(df)

X = df.drop("label", axis=1)
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = XGBClassifier(
    n_estimators=100,
    max_depth=4,
    learning_rate=0.1
)

model.fit(X_train, y_train)

# evaluation
pred = model.predict(X_test)
acc = accuracy_score(y_test, pred)

print("Accuracy:", acc)

# save model
joblib.dump(model, "ml/model.pkl")