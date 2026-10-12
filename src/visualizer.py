# -*- coding: utf-8 -*-
import os
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns


def plot_sales_overview(df, save_path=None):
    """Satis genel bakis grafikleri: kategori, yil, bolge, teslimat."""
    cols = df.columns.tolist()

    # Dinamik kolon tespiti
    delivery_col = next(
        (c for c in cols if 'day' in c.lower() or 'deliver' in c.lower()),
        None
    )
    year_col = next(
        (c for c in cols if 'year' in c.lower()),
        None
    )

    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(16, 10))

    # 1. Kategoriye gore satis (pasta grafik)
    if 'Category' in cols and 'Sales' in cols:
        sales_by_category = df.groupby('Category')['Sales'].sum()
        axes[0, 0].pie(
            sales_by_category,
            labels=sales_by_category.index,
            autopct='%1.1f%%'
        )
        axes[0, 0].set_title('Kategoriye Gore Satis')
    else:
        axes[0, 0].set_visible(False)

    # 2. Yila gore satis (cizgi grafik)
    if year_col and 'Sales' in cols:
        sales_by_year = df.groupby(year_col)['Sales'].sum()
        axes[0, 1].plot(sales_by_year.index, sales_by_year.values, marker='o')
        axes[0, 1].set_title('Yila Gore Satis')
        axes[0, 1].set_xticks(sales_by_year.index)
        axes[0, 1].set_xticklabels(
            [str(y) for y in sales_by_year.index], rotation=45
        )
        axes[0, 1].set_xlabel('Yil')
        axes[0, 1].set_ylabel('Toplam Satis')
    else:
        axes[0, 1].set_visible(False)

    # 3. Bolgeye gore satis (cubuk grafik)
    if 'Region' in cols and 'Sales' in cols:
        sales_by_region = df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
        axes[1, 0].bar(sales_by_region.index, sales_by_region.values)
        axes[1, 0].set_title('Bolgeye Gore Satis')
        axes[1, 0].tick_params(axis='x', rotation=45)
        axes[1, 0].set_ylabel('Toplam Satis')
    else:
        axes[1, 0].set_visible(False)

    # 4. Teslimat suresi vs Satis (nokta grafik)
    if delivery_col and 'Sales' in cols:
        axes[1, 1].scatter(df[delivery_col], df['Sales'], alpha=0.3, s=10)
        axes[1, 1].set_xlabel(delivery_col)
        axes[1, 1].set_ylabel('Satis')
        axes[1, 1].set_title(f'{delivery_col} vs Satis')
    else:
        axes[1, 1].set_visible(False)

    plt.tight_layout()

    # Dosyaya kaydet
    if save_path:
        save_dir = os.path.dirname(save_path)
        if save_dir:
            os.makedirs(save_dir, exist_ok=True)
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Grafik kaydedildi: {save_path}")

    plt.show()
    plt.close('all')


def plot_outlier_boxplots(df):
    """Aykiri deger kutu grafikleri: Sales, Profit, Quantity, Discount."""
    outlier_columns = [
        c for c in ['Sales', 'Profit', 'Quantity', 'Discount']
        if c in df.columns
    ]

    if not outlier_columns:
        print("Grafik icin uygun kolon bulunamadi.")
        return

    n = len(outlier_columns)
    ncols = 2
    nrows = (n + 1) // 2

    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(14, 5 * nrows))

    # axes her zaman 2D olsun
    if nrows == 1:
        axes = [axes] if ncols == 1 else [axes]
    axes_flat = [ax for row in axes for ax in (row if hasattr(row, '__iter__') else [row])]

    for i, column in enumerate(outlier_columns):
        ax = axes_flat[i]
        data = df[column].dropna().values
        ax.boxplot(data, orientation='vertical')
        ax.set_title(f'{column} Dagilimi')
        ax.set_ylabel(column)

    # Artık eksenleri gizle
    for j in range(n, len(axes_flat)):
        axes_flat[j].set_visible(False)

    plt.tight_layout()
    plt.show()
    plt.close('all')
