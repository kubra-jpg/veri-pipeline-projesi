# visualizer.py

import matplotlib.pyplot as plt
import seaborn as sns

def plot_sales_overview(df, save_path=None):
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(16, 10))

    sales_by_category = df.groupby('Category')['Sales'].sum()
    axes[0, 0].pie(sales_by_category, labels=sales_by_category.index, autopct='%1.1f%%')
    axes[0, 0].set_title('Sales by Category')

    sales_by_year = df.groupby('Order Year')['Sales'].sum()
    axes[0, 1].plot(sales_by_year.index, sales_by_year.values)
    axes[0, 1].set_title('Sales by Year')
    axes[0, 1].set_xticks(sales_by_year.index)
    axes[0, 1].set_xticklabels(sales_by_year.index, rotation=45)

    sales_by_region = df.groupby('Region')['Sales'].sum()
    sns.barplot(x=sales_by_region.index, y=sales_by_region.values, ax=axes[1, 0])
    axes[1, 0].set_title('Sales by Region')

    sns.scatterplot(data=df, x='Ship Days', y='Sales', ax=axes[1, 1])
    axes[1, 1].set_title('Ship Days vs Sales')

    plt.tight_layout()

    if save_path:
        import os
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Grafik kaydedildi: {save_path}")

    plt.show()

def plot_outlier_boxplots(df):
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(16, 10))

    outlier_columns = ['Sales', 'Profit', 'Quantity', 'Discount']
    for i, column in enumerate(outlier_columns):
        ax = axes[i // 2, i % 2]
        sns.boxplot(data=df, x=column, ax=ax)
        ax.set_title(f'{column} Değişkeni için Aykırı Değerler')
    
    plt.tight_layout()
    plt.show()