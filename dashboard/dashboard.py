import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import datetime as dt

# Load the dataset
@st.cache_data
def load_data():
    return pd.read_csv('./main_data.csv')

# Segmentation RFM
def rfm_segment(row):
    if row['RFM_Score'] in ['555', '554', '545', '544']:
        return 'Best Customers'
    elif row['RFM_Score'] in ['511', '522', '533']:
        return 'Loyal Customers'
    elif row['RFM_Score'] in ['311', '322', '333']:
        return 'Potential Loyalists'
    elif row['RFM_Score'][0] == '5':
        return 'Recent Customers'
    elif row['RFM_Score'][1] == '1':
        return 'Churned Customers'
    else:
        return 'Others'

data = load_data()

# Dashboard Title
st.title("E-Commerce Data Dashboard")

# Sidebar Options
st.sidebar.title("Menu")
options = st.sidebar.radio("Go to:", [
    "Overview",
    "Penjualan per State",
    "Metode Pembayaran",
    "Ulasan Produk",
    "Distribusi Penjual",
    "Tren Penjualan",
    "Pendapatan dan Penjualan Produk",
    "Waktu Pengiriman",
    "RFM Analysis",
    "Clustering"
])

# Bagian Overview
if options == "Overview":
    st.title("Dataset Overview")
    st.write("Tampilan komprehensif data e-commerce termasuk penjualan, ulasan pelanggan, dan informasi penjual.")
    st.dataframe(data.head(15))

# Bagian Jumlah Penjualan
elif options == "Penjualan per State":
    st.title("Sales by State")
    state_sales = data['seller_state'].value_counts()
    top_states = state_sales.head(10)
    fig, ax = plt.subplots()
    top_states.plot(kind='bar', color='#3A4F7A', ax=ax)
    ax.set_title("10 Penjualan Tertinggi per State")
    ax.set_xlabel("State")
    ax.set_ylabel("Jumlah Penjualan")
    st.pyplot(fig)
    # Insight
    st.write("**SP (Sao Paulo)** muncul sebagai pasar utama dengan penjualan tertinggi sebesar 837,560 BRL, didukung oleh populasi besar, infrastruktur maju, atau aktivitas ekonomi yang tinggi. **PR (Parana)**, **MG (Minas Gerais)**, dan **RJ (Rio de Janeiro)** menyusul sebagai pusat penjualan utama dengan kontribusi signifikan antara 56,000 hingga 82,000 BRL. **SC (Santa Catarina)** dan **RS (Rio Grande do Sul)** berada di kategori produk menengah dengan kontribusi moderat, sedangkan **MA (Maranhao)**, **PE (Pernambuco)**, **DF (Distrito Federal)**, dan **BA (Bahia)** menunjukkan potensi pasar yang belum tergarap maksimal dengan penjualan di bawah 14,000 BRL.")

# Bagian Metode Pembayaran
elif options == "Metode Pembayaran":
    st.title("Distribusi Metode Pembayaran")
    payment_types = data['payment_type'].value_counts()
    colors = ['#FF90BC', '#FFC0D9', '#F9F9E0', '#8ACDD7']

    fig, ax = plt.subplots()
    payment_types.plot(kind='pie', autopct='%1.1f%%', colors=colors, ax=ax)
    ax.set_ylabel("")
    ax.set_title("Metode Pembayaran")
    st.pyplot(fig)
    st.write("**Credit card** mendominasi metode pembayaran dengan 75.1% transaksi (875,944 transaksi), menunjukkan popularitasnya karena kemudahan, fleksibilitas, dan fasilitas cicilan. **Boleto** tetap relevan dengan 18% transaksi (212,006 transaksi), melayani pelanggan tanpa akses ke **credit card** atau yang lebih memilih pembayaran langsung. **Voucher** dan **debit card** memiliki peran kecil, masing-masing dengan 3.9% (46,015 transaksi) dan 2.8% (32,3219 transaksi), kemungkinan karena keterbatasa penerimaan atau preferensi pelanggan terhadap metode pembayaran lain.")

# Bagian Ulasan Produk
elif options == "Ulasan Produk":
    st.title("10 Kategori Produk Tertinggi Berdasarkan Rata-Rata Skor Ulasan")
    review_scores = data.groupby('product_category_name')['review_score'].mean().sort_values(ascending=False).head(10)

    fig, ax = plt.subplots()
    review_scores.plot(kind='bar', color='#E98EAD', ax=ax)
    ax.set_title("10 Kategori Produk Tertinggi Berdasarkan Rata-Rata Skor Ulasan")
    ax.set_xlabel("Kategori Produk")
    ax.set_ylabel("Rata-rata Skor Ulasan")
    st.pyplot(fig)
    st.write("Kategori produk seperti *tablets_printing_image*, *fashion_childrens_clothes*, dan *cds_dvds_musicals* mendapatkan skor ulasan sempurna (5.0), menunjukkan kepuasan pelanggan yang luar biasa. Produk fashion seperti *fashion_made_clothing*, *fashion_shoes*, dan *fashion_underwear_beach* mendapatkan skor rata-rata >4.4, mencerminkan kualitas, variasi, atau layanan yang baik. Produk dalam kategori *computers*, *small_appliances_home_oven_and_coffee*, dan *construction_tools_tools* menonjol sebagai produk berkualitas tinggi yang memenuhi ekspektasi pelanggan. Selain itu, *christmas_supplies* memiliki skor tinggi (4.48), mengindikasikan relevansi dan kepuasan pelanggan untuk produk musiman.")

# Bagian Distribusi Penjual
elif options == "Distribusi Penjual":
    st.title("10 Kota Tempat Jumlah Penjual Tertinggi")
    seller_city = data['seller_city'].value_counts().head(10)

    fig, ax = plt.subplots()
    seller_city.plot(kind='bar', color='#FB9AD1', ax=ax)
    ax.set_title("Top 10 Cities by Number of Sellers")
    ax.set_xlabel("Kota")
    ax.set_ylabel("Jumlah Penjual")
    st.pyplot(fig)
    st.write("**Sao Paulo** menempati posisi teratas dengan 300,500 penjual, mencerminkan perannya sebagai pusat ekonomi terbesar di Brasil dengan aktivitas bisnis yang tinggi. Kota **Ibitiinga** mengejutkan di posisi kedua dengan 91,056 penjual, menunjukkan potensi perdagangan yang signifikan meskipun bukan kota metropolitan utama. Kota-kota seperti **Rio de Janeiro**, **Curitiba**, dan **Belo Horizonte**, yang juga merupakan pusat bisnis penting, berada di daftar 10 besar, sementara kota-kota seperti **Guarulhos**, **Ribeirao Preto**, dan **Campinas** menunjukkan aktivitas perdagangan terbesar hingga ke kota-kota yang lebih kecil, menciptakan jaringan ekonomi yang luas.")

# Bagian Tren Penjualan
elif options == "Tren Penjualan":
    st.title("Tren Penjualan")
    data['order_purchase_timestamp'] = pd.to_datetime(data['order_purchase_timestamp'])
    sales_month = data['order_purchase_timestamp'].dt.to_period('M').value_counts().sort_index()
    sales_month.index = sales_month.index.to_timestamp()

    fig, ax = plt.subplots()
    sales_month.plot(kind='line', color='#D2649A', marker='o', ax=ax)
    ax.set_title("Tren Penjualan Bulanans")
    ax.set_xlabel("Bulan dan Tahun")
    ax.set_ylabel("Jumlah Penjualan")
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig)
    st.write("Penjualan mengalami pertumbuhan signifikan dari **Mei 2017** hingga mencapai puncaknya **Mei 2018** dengan 266,061 penjualan, didorong oleh kemungkinan promosi besar atau faktor musiman di **awal 2018**. Setelah puncak tersebut, penjualan mengalami penurunan bertahap pada bulan-bulan berikutnya, yang mungkin mencerminkan efek pasca promosi atau musim penjualan yang lebih lambat. Penjualan terendah terjadi pada **November 2017** dengan hanya 68 penjualan, kemungkinan akibat kurangnya aktivitas promosi atau faktor musiman. Tren ini menunjukkan pentingnya strategi promosi yang konsisten untuk mempertahankan momentum penjualan.")

# Bagian Pendapatan dan Penjualan Produk
elif options == "Pendapatan dan Penjualan Produk":
    st.title("Pendapatan dan Penjualan Kategori Produk Tertinggi")
    bestsellers = data['product_category_name'].value_counts().head(10)
    income_category = data.groupby('product_category_name')['price'].sum().sort_values(ascending=False).head(10)

    st.subheader("Kategori Produk Paling Laris")
    fig1, ax1 = plt.subplots()
    bestsellers.plot(kind='bar', color='#325288', ax=ax1)
    ax1.set_title("Top 10 Categories by Sales")
    ax1.set_xlabel("Kategori Produk")
    ax1.set_ylabel("Jumlah Penjualan")
    st.pyplot(fig1)

    st.subheader("Kategori Produk dengan Income Tertinggi")
    fig2, ax2 = plt.subplots()
    income_category.plot(kind='bar', color='#D96098', ax=ax2)
    ax2.set_title("10 Kategori Produk dengan Income Tertinggi")
    ax2.set_xlabel("Kategori Produk")
    ax2.set_ylabel("Jumlah Income")
    st.pyplot(fig2)
    st.write("Kategori produk **bed_bath_table**, **health_beauty**, dan **housewares** mendominasi penjualan, dengan masing-masing lebih dari 100,000 penjualan, menunjukkan popularitasnya sebagai kebutuhan sehari-hari. **watches_gifts** memberikan kontribusi *income* terbesar (16,435,693 BRL), meskipun penjualannya lebih rendah dibanding kategori teratas, tetapi menandakan bahwa produk dengan harga tinggi dapat menghasilkan pendapatan signifikan. Kategori seperti **auto** dan **computers_accessories** juga menunjukkan tren serupa, dimana jumlah penjualan yang lebih rendah tetap menghasilkan *income* besar. Hal ini menyoroti pentingnya strategi untuk memaksimalkan pendapatan dari kategori produk bernilai tinggi.")

# Bagian Waktu Pengiriman
elif options == "Waktu Pengiriman":
    st.title("Distribusi Waktu Pengiriman")
    data['del_time'] = (pd.to_datetime(data['order_delivered_customer_date']) - pd.to_datetime(data['order_purchase_timestamp'])).dt.days

    fig, ax = plt.subplots()
    data['del_time'].dropna().plot(kind='hist', bins=20, color='#F999B7', ax=ax)
    ax.set_title("Distribusi Waktu Pengiriman")
    ax.set_xlabel("Waktu Pengiriman (Hari)")
    ax.set_ylabel("Frekuensi")
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig)
    # Menghitung rata-rata waktu pengiriman
    avg_del_time = data['del_time'].mean()
    print(f'Rata-rata waktu pengiriman: {avg_del_time:.2f} hari')
    st.write("Sebagian besar pengiriman memerlukan waktu antara **5-15 hari**, dengan rata-rata waktu pengiriman sekitar **9.75 hari**, yang menunjukkan waktu pengiriman relatif stabil **di bawah 10 hari** untuk sebagian besar pesanan. Meskipun ada beberapa kasus pengiriman yang lebih lama, hal ini jarang terjadi. Waktu pengiriman ini kemungkinan dipengaruhi oleh lokasi pelanggan dan penjual, dimana pengiriman antar kota atau antar negara bagian (state) dapat memakan waktu lebih lama.")

# Bagian RFM Analysis
elif options == "RFM Analysis":
    st.title("RFM Analysis")
    # RFM Implementation
    rfm_df = data[['customer_id', 'order_purchase_timestamp', 'price']].copy()
    rfm_df['order_purchase_timestamp'] = pd.to_datetime(rfm_df['order_purchase_timestamp'])
    reference_date = rfm_df['order_purchase_timestamp'].max() + dt.timedelta(days=1)
    st.write(f"Hari Referensi: {reference_date.date()}")
    rfm = rfm_df.groupby('customer_id').agg({
        'order_purchase_timestamp': lambda x: (reference_date - x.max()).days,
        'customer_id': 'count',
        'price': 'sum'
    })
    rfm.columns = ['Recency', 'Frequency', 'Monetary']
    # Scoring
    rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5, 4, 3, 2, 1])
    rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
    rfm['M_Score'] = pd.qcut(rfm['Monetary'], 5, labels=[1, 2, 3, 4, 5])
    rfm['RFM_Score'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)
    # Tampilan RFM DataFrame
    st.write("Data RFM:")
    st.dataframe(rfm.head())
    # Plot RFM Segments
    rfm = data[['customer_id', 'order_purchase_timestamp', 'price']].copy()
    rfm['order_purchase_timestamp'] = pd.to_datetime(rfm['order_purchase_timestamp'])
    reference_date = rfm['order_purchase_timestamp'].max() + dt.timedelta(days=1)
    rfm = rfm.groupby('customer_id').agg({
        'order_purchase_timestamp': lambda x: (reference_date - x.max()).days,
        'customer_id': 'count',
        'price': 'sum'
    })
    rfm.columns = ['Recency', 'Frequency', 'Monetary']
    rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5, 4, 3, 2, 1])
    rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
    rfm['M_Score'] = pd.qcut(rfm['Monetary'], 5, labels=[1, 2, 3, 4, 5])
    rfm['RFM_Score'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)
    rfm['segment'] = rfm.apply(rfm_segment, axis=1)
    segment_counts = rfm['segment'].value_counts()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=segment_counts.index, y=segment_counts.values, palette="viridis", ax=ax)
    ax.set_title("Distribusi Segmen Pelanggan Berdasarkan Analisis RFM")
    ax.set_xlabel("Segmen")
    ax.set_ylabel("Jumlah Pelanggan")
    plt.xticks(rotation=45)
    st.pyplot(fig)
    st.write("Sebagian besar pelanggan (5,856) berada dalam segmen **Others**, menunjukkan mayoritas belum memiliki karakteristik yang menonjol, sementara segmen **Churned Customers** (1,329) memerlukan perhatian untuk retensi. Segmen **Recent Customers** (870) memiliki potensi untuk dikembangkan menjadi pelanggan loyal, dan segmen penting seperti **Best Customers** (557) serta **Loyal Customers** (510) harus dipertahankan melalui program loyalitas. Selain itu, **Potential Loyalists** (430) menawarkan peluang untuk dikonversi menjadi pelanggan setia dengan strategi yang tepat.")

# Bagian Clustering
elif options == "Clustering":
    st.title("Clustering")
    st.header("Manual Grouping")
    st.subheader("Mengelompokkan Pelanggan Berdasarkan Total Transaksi")
    # Mengelompokkan pelanggan berdasarkan total transaksi
    customer_spend = data.groupby('customer_unique_id')['price'].sum().reset_index()
    customer_spend.columns = ['customer_unique_id', 'total_spent']
    def categorize_spending(spent):
        if spent < 500:
            return 'Low Spender'
        elif 500 <= spent < 2000:
            return 'Medium Spender'
        else:
            return 'High Spender'
    customer_spend['spender_category'] = customer_spend['total_spent'].apply(categorize_spending)
    spender_counts = customer_spend['spender_category'].value_counts()
    st.write("Distribusi Kategori Pelanggan:")
    st.bar_chart(spender_counts)
    st.write("Pelanggan dikelompokkan menjadi tiga kategori berdasarkan total pengeluaran mereka. Strategi pemasaran dapat difokuskan pada **High Spenders**.")
    
    st.header("Binning")
    st.subheader("Membagi Produk Berdasarkan Rentang Harga")
    # Membagi produk berdasarkan rentang harga
    bins_binning = [0, 50, 200, data['price'].max()]
    labels_binning = ['Low Price', 'Medium Price', 'High Price']
    data['price_category'] = pd.cut(data['price'], bins=bins_binning, labels=labels_binning, include_lowest=True)
    price_distribution = data['price_category'].value_counts()
    st.write("Distribusi Produk Berdasarkan Kategori Harga:")
    st.bar_chart(price_distribution)
    # Insight
    st.write("Kategori produk dengan harga rendah mendominasi jumlah produk, tetapi kategori harga tinggi berkontribusi lebih besar terhadap pendapatan.")
    
    st.header("Gabungan Clustering")
    st.subheader("Menggabungkan Kategori Pelanggan dan Produk")
    # Menggabungkan data pelanggan dan produk
    customer_spend = data.groupby('customer_unique_id')['price'].sum().reset_index()
    customer_spend.columns = ['customer_unique_id', 'total_spent']
    customer_spend['spender_category'] = customer_spend['total_spent'].apply(categorize_spending)
    customer_product = data.merge(customer_spend, on='customer_unique_id', how='inner')
    # Membuat pivot table
    pivot_table = customer_product.pivot_table(
        index='spender_category',
        columns='price_category',
        values='order_id',
        aggfunc='count',
        fill_value=0
    )
    # Tampilan pivot table
    st.write("Pivot Table - Pola Belanja Pelanggan:")
    st.dataframe(pivot_table)
    # Visualisasi heatmap
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(pivot_table, annot=True, fmt='d', cmap='Blues', ax=ax)
    ax.set_title('Pola Belanja Pelanggan Berdasarkan Kategori Produk dan Pengeluaran')
    ax.set_xlabel('Kategori Harga Produk')
    ax.set_ylabel('Kategori Pelanggan')
    st.pyplot(fig)
    # Insight
    st.write("Pelanggan **High Spender** cenderung membeli produk dari kategori **Medium Price** dan **High Price**. Strategi pemasaran seperti bundling produk dapat ditargetkan berdasarkan pola ini.")
    