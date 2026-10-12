# -*- coding: utf-8 -*-
"""
Otomatik HTML raporu olusturucu.
Kullanim:
    from report_generator import generate_html_report
    generate_html_report(df_clean, output_path='../outputs/rapor.html')
"""

import os
import base64
import io
from datetime import datetime

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')   # Sadece dosyaya kaydetmek icin; notebook displayleri etkilemez
import matplotlib.pyplot as plt
import seaborn as sns


# ---------------------------------------------------------------------------
# Yardimci: grafigi base64 PNG'ye donustur (HTML icine gomme icin)
# ---------------------------------------------------------------------------

def _fig_to_base64(fig) -> str:
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=120, bbox_inches='tight')
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return encoded


# ---------------------------------------------------------------------------
# Grafik uretici fonksiyonlar (base64 dondurur)
# ---------------------------------------------------------------------------

def _sales_overview_b64(df) -> str:
    cols = df.columns.tolist()
    delivery_col = next((c for c in cols if 'day' in c.lower() or 'deliver' in c.lower()), None)
    year_col = next((c for c in cols if 'year' in c.lower()), None)

    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(14, 9))

    if 'Category' in cols and 'Sales' in cols:
        sales_by_category = df.groupby('Category')['Sales'].sum()
        axes[0, 0].pie(sales_by_category, labels=sales_by_category.index, autopct='%1.1f%%')
        axes[0, 0].set_title('Kategoriye Gore Satis')
    else:
        axes[0, 0].set_visible(False)

    if year_col and 'Sales' in cols:
        sales_by_year = df.groupby(year_col)['Sales'].sum()
        axes[0, 1].plot(sales_by_year.index, sales_by_year.values, marker='o', color='steelblue')
        axes[0, 1].set_title('Yila Gore Satis')
        axes[0, 1].set_xlabel('Yil')
        axes[0, 1].set_ylabel('Toplam Satis')
        axes[0, 1].set_xticks(sales_by_year.index)
        axes[0, 1].set_xticklabels([str(y) for y in sales_by_year.index], rotation=45)
    else:
        axes[0, 1].set_visible(False)

    if 'Region' in cols and 'Sales' in cols:
        sales_by_region = df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
        axes[1, 0].bar(sales_by_region.index, sales_by_region.values, color='steelblue')
        axes[1, 0].set_title('Bolgeye Gore Satis')
        axes[1, 0].tick_params(axis='x', rotation=45)
        axes[1, 0].set_ylabel('Toplam Satis')
    else:
        axes[1, 0].set_visible(False)

    if delivery_col and 'Sales' in cols:
        axes[1, 1].scatter(df[delivery_col], df['Sales'], alpha=0.3, s=8, color='steelblue')
        axes[1, 1].set_xlabel(delivery_col)
        axes[1, 1].set_ylabel('Satis')
        axes[1, 1].set_title(f'{delivery_col} vs Satis')
    else:
        axes[1, 1].set_visible(False)

    plt.tight_layout()
    return _fig_to_base64(fig)


def _correlation_b64(df) -> str:
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if len(numeric_cols) < 2:
        return ''
    corr_matrix = df[numeric_cols].corr()
    fig, ax = plt.subplots(figsize=(9, 7))
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='RdYlGn',
                center=0, square=True, linewidths=0.5, ax=ax)
    ax.set_title('Korelasyon Isi Haritasi', fontsize=13, pad=12)
    plt.tight_layout()
    return _fig_to_base64(fig)


def _profit_b64(df) -> str:
    cols = df.columns.tolist()
    if 'Sales' not in cols or 'Profit' not in cols:
        return ''

    df = df.copy()
    df['Profit_Margin'] = df.apply(
        lambda row: (row['Profit'] / row['Sales'] * 100) if row['Sales'] != 0 else 0, axis=1
    )

    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(14, 10))

    if 'Category' in cols:
        margin_by_cat = df.groupby('Category')['Profit_Margin'].mean().sort_values(ascending=False)
        colors = ['#2ecc71' if v >= 0 else '#e74c3c' for v in margin_by_cat.values]
        axes[0, 0].bar(margin_by_cat.index, margin_by_cat.values, color=colors)
        axes[0, 0].axhline(y=0, color='black', linewidth=0.8, linestyle='--')
        axes[0, 0].set_title('Kategoriye Gore Ort. Kar Marji (%)')
        axes[0, 0].set_ylabel('Kar Marji (%)')
    else:
        axes[0, 0].set_visible(False)

    if 'Discount' in cols:
        sample = df.sample(min(2000, len(df)), random_state=42)
        axes[0, 1].scatter(sample['Discount'], sample['Profit_Margin'],
                           alpha=0.3, s=12, c='steelblue')
        axes[0, 1].axhline(y=0, color='red', linewidth=0.8, linestyle='--')
        axes[0, 1].set_xlabel('Indirim Orani')
        axes[0, 1].set_ylabel('Kar Marji (%)')
        axes[0, 1].set_title('Indirim vs Kar Marji')
    else:
        axes[0, 1].set_visible(False)

    if 'Sub-Category' in cols:
        profit_by_subcat = df.groupby('Sub-Category')['Profit'].sum().sort_values()
        colors = ['#2ecc71' if v >= 0 else '#e74c3c' for v in profit_by_subcat.values]
        axes[1, 0].barh(profit_by_subcat.index, profit_by_subcat.values, color=colors)
        axes[1, 0].axvline(x=0, color='black', linewidth=0.8, linestyle='--')
        axes[1, 0].set_title('Alt Kategoriye Gore Toplam Kar')
        axes[1, 0].set_xlabel('Toplam Kar')
    else:
        axes[1, 0].set_visible(False)

    if 'Segment' in cols:
        seg_sales = df.groupby('Segment')['Sales'].sum()
        seg_profit = df.groupby('Segment')['Profit'].sum()
        x = np.arange(len(seg_sales))
        w = 0.35
        axes[1, 1].bar(x - w / 2, seg_sales.values, w, label='Satis', color='steelblue')
        axes[1, 1].bar(x + w / 2, seg_profit.values, w, label='Kar', color='#2ecc71')
        axes[1, 1].set_xticks(x)
        axes[1, 1].set_xticklabels(seg_sales.index, rotation=15)
        axes[1, 1].set_title('Segment Bazinda Satis ve Kar')
        axes[1, 1].set_ylabel('Tutar')
        axes[1, 1].legend()
    else:
        axes[1, 1].set_visible(False)

    plt.tight_layout()
    return _fig_to_base64(fig)


# ---------------------------------------------------------------------------
# Ozet istatistikler tablosu icin HTML
# ---------------------------------------------------------------------------

def _summary_html(df) -> str:
    stats = df.describe().T[['count', 'mean', 'std', 'min', 'max']]
    stats = stats.round(2)
    rows = ''
    for col, row in stats.iterrows():
        rows += f"""
        <tr>
          <td>{col}</td>
          <td>{int(row['count'])}</td>
          <td>{row['mean']:.2f}</td>
          <td>{row['std']:.2f}</td>
          <td>{row['min']:.2f}</td>
          <td>{row['max']:.2f}</td>
        </tr>"""
    return f"""
    <table>
      <thead>
        <tr>
          <th>Kolon</th><th>Sayi</th><th>Ortalama</th>
          <th>Std Sapma</th><th>Min</th><th>Max</th>
        </tr>
      </thead>
      <tbody>{rows}</tbody>
    </table>"""


# ---------------------------------------------------------------------------
# Ana rapor uretici
# ---------------------------------------------------------------------------

def generate_html_report(df: pd.DataFrame, output_path: str = 'rapor.html') -> str:
    """
    DataFrame'den tam HTML raporu olusturur ve dosyaya kaydeder.

    Parametreler
    ----------
    df          : Temizlenmis DataFrame
    output_path : Kaydedilecek .html dosyasinin yolu

    Dondurur
    --------
    str : Kaydedilen dosyanin yolu
    """
    now = datetime.now().strftime('%d %B %Y, %H:%M')
    n_rows, n_cols = df.shape

    # Grafikleri base64 olarak hazirla
    img_sales = _sales_overview_b64(df)
    img_corr  = _correlation_b64(df)
    img_profit = _profit_b64(df)
    summary_tbl = _summary_html(df)

    def img_tag(b64, alt='grafik'):
        return f'<img src="data:image/png;base64,{b64}" alt="{alt}">' if b64 else '<p><em>Grafik olusturulamadi.</em></p>'

    html = f"""<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Veri Pipeline Raporu</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Segoe UI', Arial, sans-serif;
      font-size: 15px;
      color: #222;
      background: #f5f6fa;
      padding: 0 0 40px;
    }}
    header {{
      background: linear-gradient(135deg, #1a1a2e 0%, #16213e 60%, #0f3460 100%);
      color: #fff;
      padding: 36px 40px 28px;
    }}
    header h1 {{ font-size: 2rem; margin-bottom: 6px; }}
    header p  {{ opacity: .75; font-size: .95rem; }}
    .badge {{
      display: inline-block;
      background: rgba(255,255,255,.15);
      border-radius: 4px;
      padding: 2px 10px;
      font-size: .8rem;
      margin-top: 10px;
    }}
    main {{ max-width: 1100px; margin: 32px auto; padding: 0 20px; }}
    section {{
      background: #fff;
      border-radius: 10px;
      box-shadow: 0 2px 8px rgba(0,0,0,.06);
      padding: 28px 32px;
      margin-bottom: 28px;
    }}
    h2 {{
      font-size: 1.2rem;
      color: #0f3460;
      border-left: 4px solid #0f3460;
      padding-left: 12px;
      margin-bottom: 18px;
    }}
    .kpi-row {{
      display: flex;
      gap: 16px;
      flex-wrap: wrap;
      margin-bottom: 6px;
    }}
    .kpi {{
      flex: 1;
      min-width: 140px;
      background: #f0f4ff;
      border-radius: 8px;
      padding: 18px 20px;
      text-align: center;
    }}
    .kpi .val {{ font-size: 1.9rem; font-weight: 700; color: #0f3460; }}
    .kpi .lbl {{ font-size: .8rem; color: #666; margin-top: 4px; }}
    img {{ max-width: 100%; border-radius: 6px; display: block; margin: 0 auto; }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: .88rem;
    }}
    th, td {{
      padding: 9px 12px;
      text-align: right;
      border-bottom: 1px solid #eee;
    }}
    th {{ background: #f0f4ff; color: #0f3460; font-weight: 600; text-align: right; }}
    td:first-child, th:first-child {{ text-align: left; }}
    tr:hover td {{ background: #fafbff; }}
    footer {{
      text-align: center;
      color: #999;
      font-size: .8rem;
      margin-top: 10px;
    }}
  </style>
</head>
<body>
<header>
  <h1>📊 Veri Pipeline Raporu</h1>
  <p>Superstore Satis Veri Seti — Otomatik Analiz</p>
  <span class="badge">Olusturma tarihi: {now}</span>
</header>

<main>

  <!-- 1. Genel Ozet -->
  <section>
    <h2>1. Genel Ozet</h2>
    <div class="kpi-row">
      <div class="kpi">
        <div class="val">{n_rows:,}</div>
        <div class="lbl">Toplam Satir</div>
      </div>
      <div class="kpi">
        <div class="val">{n_cols}</div>
        <div class="lbl">Kolon Sayisi</div>
      </div>
      {''.join(f"""
      <div class="kpi">
        <div class="val">{df[col].sum():,.0f}</div>
        <div class="lbl">Toplam {col}</div>
      </div>""" for col in ['Sales', 'Profit'] if col in df.columns)}
    </div>
  </section>

  <!-- 2. Istatistiksel Ozet -->
  <section>
    <h2>2. Istatistiksel Ozet</h2>
    {summary_tbl}
  </section>

  <!-- 3. Satis Genel Bakis -->
  <section>
    <h2>3. Satis Genel Bakis</h2>
    {img_tag(img_sales, 'Satis genel bakis grafikleri')}
  </section>

  <!-- 4. Korelasyon Analizi -->
  <section>
    <h2>4. Korelasyon Analizi</h2>
    {img_tag(img_corr, 'Korelasyon isi haritasi')}
  </section>

  <!-- 5. Kar Analizi -->
  <section>
    <h2>5. Kar ve Kar Marji Analizi</h2>
    {img_tag(img_profit, 'Kar analizi grafikleri')}
  </section>

</main>

<footer>
  <p>Bu rapor otomatik olarak olusturulmustur &mdash; Veri Pipeline Projesi</p>
</footer>
</body>
</html>"""

    # Kaydet
    out_dir = os.path.dirname(output_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"HTML raporu kaydedildi: {output_path}")
    return output_path
