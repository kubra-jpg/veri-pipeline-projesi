\# Veri Temizleme ve Analiz Pipeline'ı



Superstore satış veri seti üzerinde uçtan uca ETL pipeline'ı.



\## Proje Yapısı



veri-pipeline-projesi/

├── data/raw/          <- Ham veri

├── data/processed/    <- Grafikler

├── notebooks/         <- Jupyter notebook

├── outputs/           <- HTML raporu

├── src/               <- Python modülleri

├── tests/             <- Unit testler

├── logs/              <- Pipeline logları

└── requirements.txt



\## Kurulum



python -m venv venv

venv\\Scripts\\activate

pip install -r requirements.txt



\## Kullanım



jupyter lab



\## Testler



pytest tests/ -v



\## Özellikler



\- Veri temizleme: tarih dönüşümü, eksik değer doldurma

\- Aykırı değer tespiti: IQR yöntemi

\- Görselleştirme: 4 panel satış analizi, korelasyon haritası

\- Otomatik HTML raporu

\- Logging sistemi

\- 4 unit test, hepsi başarılı



\## Veri Seti



Superstore Sales Dataset - 9800 satır, 18 kolon



\## Teknolojiler



Python 3.12 - pandas - matplotlib - seaborn - pytest - Jupyter

