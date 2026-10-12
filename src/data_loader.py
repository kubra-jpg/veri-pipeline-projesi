"""Veri yükleme fonksiyonları."""
import pandas as pd


def load_raw_data(filepath):
    """Ham CSV dosyasını yükler."""
    df = pd.read_csv(filepath, encoding='latin-1')
    print(f"Veri yüklendi: {df.shape[0]} satır, {df.shape[1]} sütun")
    return df
    