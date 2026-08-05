import streamlit as st
import pandas as pd
import joblib
import os

from pandas.api.types import is_numeric_dtype

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.impute import SimpleImputer

from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

from sklearn.metrics import accuracy_score, r2_score, mean_squared_error


def machine_learning(df):

    st.title(" Machine Learning")

    if df is None:
        st.warning("Please upload a dataset first.")
        return

    target = st.selectbox(" Select Target Column", df.columns)

    if st.button(" Train Models"):

        X = df.drop(columns=[target]).copy()
        y = df[target].copy()

        st.write("Target:", target)
        st.write("Datatype:", y.dtype)
        st.write("Unique Values:", y.nunique())

        # -------------------------
        # Detect Problem Type
        # -------------------------

        if (not is_numeric_dtype(y)) or (y.nunique() <= 20):
            problem = "classification"
        else:
            problem = "regression"

        # -------------------------
        # Encode Target (Classification)
        # -------------------------

        if problem == "classification":

            le = LabelEncoder()

            y = y.astype(str)
            y = le.fit_transform(y)

        # -------------------------
        # Features
        # -------------------------

        numeric_cols = X.select_dtypes(include=["number"]).columns.tolist()
        categorical_cols = X.select_dtypes(exclude=["number"]).columns.tolist()

        numeric_transformer = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="median"))
            ]
        )

        categorical_transformer = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("encoder", OneHotEncoder(handle_unknown="ignore"))
            ]
        )

        preprocessor = ColumnTransformer(
            transformers=[
                ("num", numeric_transformer, numeric_cols),
                ("cat", categorical_transformer, categorical_cols)
            ]
        )

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42
        )

        # =====================================================
        # CLASSIFICATION
        # =====================================================

        if problem == "classification":

            st.subheader("Problem Type : Classification")

            models = {
                "Logistic Regression": LogisticRegression(max_iter=1000),
                "Decision Tree": DecisionTreeClassifier(random_state=42),
                "Random Forest": RandomForestClassifier(random_state=42)
            }

            results = []

            best_score = 0
            best_model = None

            for name, model in models.items():

                pipe = Pipeline([
                    ("preprocessor", preprocessor),
                    ("model", model)
                ])

                pipe.fit(X_train, y_train)

                pred = pipe.predict(X_test)

                score = accuracy_score(y_test, pred)

                results.append(
                    {
                        "Model": name,
                        "Accuracy": round(score, 4)
                    }
                )

                if score > best_score:
                    best_score = score
                    best_model = pipe

            st.dataframe(pd.DataFrame(results))

            st.success(f" Best Accuracy : {best_score:.2%}")

        # =====================================================
        # REGRESSION
        # =====================================================

        else:

            st.subheader(" Problem Type : Regression")

            models = {
                "Linear Regression": LinearRegression(),
                "Decision Tree": DecisionTreeRegressor(random_state=42),
                "Random Forest": RandomForestRegressor(random_state=42)
            }

            results = []

            best_score = float("-inf")
            best_model = None

            for name, model in models.items():

                pipe = Pipeline([
                    ("preprocessor", preprocessor),
                    ("model", model)
                ])

                pipe.fit(X_train, y_train)

                pred = pipe.predict(X_test)

                r2 = r2_score(y_test, pred)

                rmse = mean_squared_error(y_test, pred) ** 0.5

                results.append(
                    {
                        "Model": name,
                        "R² Score": round(r2, 4),
                        "RMSE": round(rmse, 4)
                    }
                )

                if r2 > best_score:
                    best_score = r2
                    best_model = pipe

            st.dataframe(pd.DataFrame(results))

            st.success(f" Best R² Score : {best_score:.4f}")

        # -------------------------
        # Save Model
        # -------------------------

        os.makedirs("models", exist_ok=True)

        joblib.dump(best_model, "models/best_model.pkl")

        st.success(" Best model saved successfully.")

        with open("models/best_model.pkl", "rb") as f:

            st.download_button(
                "⬇ Download Best Model",
                data=f,
                file_name="best_model.pkl"
            )
