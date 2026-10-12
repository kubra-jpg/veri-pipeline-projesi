"""Veri temizleme ve dönüştürme fonksiyonları."""
import pandas as pd


def clean_dates(df):
    """Tarih sütunlarını datetime formatına çevirir."""
    df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)
    df['Ship Date'] = pd.to_datetime(df['Ship Date'], dayfirst=True)
    return df


def fill_missing_postal_codes(df):
    """Eksik posta kodlarını medyan ile doldurur."""
    df['Postal Code'] = df['Postal Code'].fillna(df['Postal Code'].median())
    df['Postal Code'] = df['Postal Code'].astype(int)
    return df


def add_derived_columns(df):
    """Teslimat süresi, yıl, ay gibi türetilmiş sütunlar ekler."""
    df['Delivery Days'] = (df['Ship Date'] - df['Order Date']).dt.days
    df['Order Year'] = df['Order Date'].dt.year
    df['Order Month'] = df['Order Date'].dt.month
    return df


def detect_outliers_iqr(df, column):
    """IQR yöntemiyle aykırı değerleri tespit eder."""
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
    return outliers, lower_bound, upper_bound


def clean_pipeline(df):
    """Tüm temizleme adımlarını sırayla uygular."""
    df = clean_dates(df)
    df = fill_missing_postal_codes(df)
    df = add_derived_columns(df)
    print("Temizleme pipeline'ı tamamlandı.")
    return df
    