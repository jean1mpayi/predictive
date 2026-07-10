def create_features(df):
    df["stress_index"] = df["vibration"] * df["temperature"]
    df["pressure_ratio"] = df["pressure"] / (df["torque"] + 1)

    return df