#RFM ile Müşteri Segmentasyonu:
#
#
# Basit, kural tabanlı bir müşteri segmentasyon tekniğidir.
#RFM: Recency, Frequency, Monetary:Bir analiz türüdür.
#Müşterilerin satın alma alışkanlıkları üzerinden gruplara ayrılması ve bu gruplar özelinde stratejiler geliştirebilmesini sağlar.
#CRM Çalışmaları için birçok başlıkta veriye dayalı aksiyon alma imkanı sağlar.

#Recency (Yenilik) Bizzat en son ne zaman alışveriş yaptı durumunu ifade etmektedir.
#Müşterinin sıcaklığını yeniliğini ifade etmektedir. (küçük olan değer daha iyidir.)

#Frequency:Sıklık, müşterinin toplam yaptığı alışveriş sayısıdır, işlem sayısıdır.
#satın alma sıklığı, işlem sıklığıdır. (en büyük değer daha iyidir.)

#Monetary (parasal değer): müşterilerin bize bıraktığı parasal değeri ifade eder.(en büyük değer daha iyidir.)
#metriklerin kendi içinde bir kıyaslama problemi vardır. Küçüklük büyüklük karmaşasını aşmak için buradaki değerleri hem kendi içerisinde hem de birbirleriyle kıyaslanabilir yapmak gerkmektedir.
#Yaaaani;
#FRM Metriklerini RFM skorlarına çevirmemiz gerekmektedir. 1-5 arası puanlarız mesela.
# DİKKAT!! Recency değerinde küçük olması bizim için iyiydi ama metriği skoru oluşturulurken küçüğe büyük değer verilir.

#RFM değerleri yan yana getirildiğinde gerçek manda yan yana getirmek RFM skorunu oluştururuz
#RFM skoru 555 olanlar benim için en değerli müşteridir, En kötü müşteri 111

#RFM skorunun ortaya çıkaracağı çok fazla kombinasyon vardır ve bu kombinasyonlarla uğraşmak oldukça zorlayıcı olurdu.
#RFM skorlarından daha az sayıda bir skor ayrımları mantıksal ve iş bilgisine uygun gruplar/segmentler oluştursun.

#Skorlar Üzerinden Segmentler Oluşturmak
#bir görsel var: x ekseni recency, y ekseni frequency: 2 boyut üzerinden bir sınıflandırma yapmak daha sağlıklı olacaktır.
#CRM analitiği kapsamında frekans/işlem daha önemlidir.

#RFM ile Müşteri Segmentasyonu

#1.İş Problemi
#2.Veriyi Anlama
#3.Veriyi Hazırlama
#4.RFM Metriklerinin Hesaplanması
#5.RFM Skorlaının Hesaplanması
#6.RFM Segmentlerinin Oluşturulması ve Analiz Edilmesi
#7.Tüm Sürecin Fonksiyonlaştırılması (Burada görülen tüm yaklaşımları bir fonksiyonla yazma (tek fonksiyon 2 satır kod)

#1. Business Problem

#Bir e-ticaret şirketi müşterilerini segmentlere ayırıp bu segmentlere göre pazarlama stratejileri belirlemek istiyor.

#Online Retail 2 isimli veri seti İngiltere merkezli online bir satış mağazasının 01/12/2009 - 09/12/2011 tarihleri arasındaki satışlarını içeriyor.
#Bu şirket promosyon hediyelik ürün satmakta ve müşterilerin büyük çoğunluğu toptancıdır.
#Müşterileri aslında kurumsal müşterilerdir.

#Değişkenler:
#
#InvoiceNo: Fatura numarası, her işleme yani faturaya ait eşsiz numara. C ile başlıyosa iptal edilen işlem.
#StockCode: Ürün kodu. Her bir ürün için eşsiz numara.
#Description: Ürün ismi.
#Quantity:Ürün adedi. Faturalardaki ürünlerden kaçar tane satıldığını ifade etmektedir.
#InvoiceDate:Fatura tarihi ve zamanı.
#UnitPrice:Ürün fiyatı. (sterlin cinsinden)
#CustomerID: Eşsiz müşteri numarası
#Country:Ülke ismi. Müşterinin yaşadığı ülke.

#Ana odağımız faturalardır. Bir fatura içerisinde birden fazla ürün satılmış olabilir.
#3-5 tane ürün satılmış olabilir bir faturada.


#Veriyi Anlama (Data Understanding):

import datetime as dt
import pandas as pd
pd.set_option('display.max_columns', None) #Yazdırma işlemi yaptığımda bütün sütunların gözükmesini istiyorum bilgisi
# pd.set_option('display.max_rows', None) #Bütün satırları gör bilgisi var, çıktı kalabalık olmasın diye şimdilik tercih etmiyorum.
pd.set_option('display.float_format', lambda x: '%.5f' % x) #Sayısal değişkenlerin virgülden sonra kaç basamağını göstermeliyim ifade eden bir bilgi var.
df_=pd.read_excel('HAFTA 3/online_retail_II.xlsx', sheet_name= "Year 2009-2010")
df1=df_.copy()
df=df_.copy() #copy fonksiyonu ilgili dataframe'in orijinalini bozmadan üzerinde çalışma imkanı sağlar. Bundan yararlanarak ileride bir problem olursa burayı çalıştırarak veri setinin ilk haline dönüş yapmış olucam.
df.head()

#Bu faturadaki bu ürüne toplam kaç para ödenmiştir? pricexquantity
#Bu faturada toplam ne kadar bir fatura bedeli vardır. Her fatura için stock codeları yani ürünlerin toplam bedellerini çıkarıp bunları ürün varlığınca toplarız.

df.shape #veri setinin boyutuna bakalım
# (525461, 8)

#eksik değer var mıdır varsa hangi değişken üzerinde kaçar tane bilgisi
df.isnull().sum()
#Invoice             0
#StockCode           0
#Description      2928
#Quantity            0
#InvoiceDate         0
#Price               0
#Customer ID    107927
#Country             0
#dtype: int64

#veri setindeki eşsiz ürün sayısı nedir?
df["Description"].nunique()
#4681

#Hangi üründen kaçar tane var? Faturalara göre şekillenmiş bir veri, 4681 tane üründen kaçar tane satılmış bilgisi?
# df["Description"].sum # Böyle düşündüm ama bu değilmiş
#<bound method NDFrame._add_numeric_operations.<locals>.sum of 0         15CM CHRISTMAS GLASS BALL 20 LIGHTS
#1                          PINK CHERRY LIGHTS
#2                         WHITE CHERRY LIGHTS
#3                RECORD FRAME 7" SINGLE SIZE
#4              STRAWBERRY CERAMIC TRINKET BOX
 #                        ...
#525456                   FELTCRAFT DOLL ROSIE
#525457           FELTCRAFT PRINCESS LOLA DOLL
#525458         FELTCRAFT PRINCESS OLIVIA DOLL
#525459     PINK FLORAL FELTCRAFT SHOULDER BAG
#525460                 JUMBO STORAGE BAG SUKI
#Name: Description, Length: 525461, dtype: object>

#bu eşsiz ürünler kaçar defa bir faturaya gündem oldu

df["Description"].value_counts().head() #Hepsini değil de birkaç tanesini gösteriyoruz.
#WHITE HANGING HEART T-LIGHT HOLDER    3549 #Bu ürün 3549 kere belli bir faturada geçmiş ama kaç tane geçmiş bilmiyorum. Kaç tane toplamda satın alınmış bilmiyorum.
#REGENCY CAKESTAND 3 TIER              2212
#STRAWBERRY CERAMIC TRINKET BOX        1843
#PACK OF 72 RETRO SPOT CAKE CASES      1466
#ASSORTED COLOUR BIRD ORNAMENT         1457
#Name: Description, dtype: int64

df["Description"].value_counts()
#WHITE HANGING HEART T-LIGHT HOLDER     3549
#REGENCY CAKESTAND 3 TIER               2212
#STRAWBERRY CERAMIC TRINKET BOX         1843
#PACK OF 72 RETRO SPOT CAKE CASES       1466
#ASSORTED COLOUR BIRD ORNAMENT          1457
#                                       ...
#stock credited from royal yacht inc       1
#VINTAGE METAL CAKE STAND CREAM            1
#BLUE BAROQUE FLOCK CANDLE HOLDER          1
#S/4 HEART CRYSTAL FRIDGE MAGNETS          1
#dotcom email                              1
#Name: Description, Length: 4681, dtype: int64


#en çok sipariş edilen ürün hangisi dersek? Description'a göre groupby'a alıp quantitylerin sum'ını alırsak eğer, Description'lara göre veriyi kır, bak bakalım hangi üründen toplam kaçar tane sipariş verilmiş,

df.groupby("Description").agg({"Quantity": "sum"}).head() #Çıktıya bak , problemli bir durum!!!! Acaba neden? Bu rpoblemi şimdilik görmezden gelelim veri önişlemede bu problemi gideriyor olacağız.
#Toplamda kaçar tane sipariş verildi bilgisi
#                                     Quantity
#Description
#21494                                    -720
#22467                                      -2
#22719                                       2
#  DOORMAT UNION JACK GUNS AND ROSES       179
# 3 STRIPEY MICE FELTCRAFT                 690

#Quantity'lere göre büyükten küçüğe sıralayalım: #Quantity'lere göre azalan şekilde sırala ve ilk 5 gözlem
df.groupby("Description").agg({"Quantity": "sum"}).sort_values("Quantity", ascending=False).head()
#                                    Quantity
#Description
#WHITE HANGING HEART T-LIGHT HOLDER     57733
#WORLD WAR 2 GLIDERS ASSTD DESIGNS      54698
#BROCADE RING PURSE                     47647
#PACK OF 72 RETRO SPOT CAKE CASES       46106
#ASSORTED COLOUR BIRD ORNAMENT          44925

#Her bir üründen toplamda ne kadar sipariş gösterdiği gösteriliyor


df["Description"].nunique() #4681 tane eşsiz ürün var, bu eşsiz ürünler faturalarda kaçar defa bir faturaya gündem oldu?

df["Description"].value_counts().head() #3549 defa bir faturada geçmiş ama kaçar tane geçmiş bilmiyorum. KAç tane toplamda satın alınmış bilmiyorum.
#WHITE HANGING HEART T-LIGHT HOLDER    3549
#REGENCY CAKESTAND 3 TIER              2212
#STRAWBERRY CERAMIC TRINKET BOX        1843
#PACK OF 72 RETRO SPOT CAKE CASES      1466
#ASSORTED COLOUR BIRD ORNAMENT         1457
#Name: Description, dtype: int64

df.groupby("Description").agg({"Quantity": "sum"})#Toplamda kaçar tane sipariş verildi bilgisi için. Şuanda bir hata var - değer verdiği için, veri önişlemede bu sorunu çözeceğiz.
#Toplam kaç tane eşsiz fatura kesilmiş?
df["Invoice"].nunique()

#Fatura başına toplam kaç para kazanılmış, toplam bedeli ne bunu bilmiyorum, ürün var, ürünün birim fiyatı ve kaç tane alındığı
#Fiyat ile quantity çarpcaz:

df["TotalPrice"] = df["Quantity"] * df["Price"] #bu şuan ürünlerin toplam kazancı oldu
df.head()
#  Invoice StockCode                          Description  Quantity  \
##0  489434     85048  15CM CHRISTMAS GLASS BALL 20 LIGHTS        12
#1  489434    79323P                   PINK CHERRY LIGHTS        12
#2  489434    79323W                  WHITE CHERRY LIGHTS        12
#3  489434     22041         RECORD FRAME 7" SINGLE SIZE         48
#4  489434     21232       STRAWBERRY CERAMIC TRINKET BOX        24
#          InvoiceDate   Price  Customer ID         Country  TotalPrice
#0 2009-12-01 07:45:00 6.95000  13085.00000  United Kingdom    83.40000
#1 2009-12-01 07:45:00 6.75000  13085.00000  United Kingdom    81.00000
#2 2009-12-01 07:45:00 6.75000  13085.00000  United Kingdom    81.00000
#3 2009-12-01 07:45:00 2.10000  13085.00000  United Kingdom   100.80000
#4 2009-12-01 07:45:00 1.25000  13085.00000  United Kingdom    30.00000

#fatura başına toplam kazanç için ne yapıcaz?

df.groupby("Invoice").agg({"TotalPrice": "sum"}).head() #Şimdi invoice başına toplam kaç para ödendiğini bulmuş olduk.
#         TotalPrice
#Invoice
#489434    505.30000
#489435    145.80000
#489436    630.33000
#489437    310.75000
#489438   2286.24000

#3.Veri Hazırlama (Data Preparation)


df.shape
#(525461, 9)
df.isnull().sum()
#Invoice             0
#StockCode           0
#Description      2928
#Quantity            0
#InvoiceDate         0
#Price               0
#Customer ID    107927
#Country             0
#TotalPrice          0
#dtype: int64

df.dropna(inplace=True) #dropna ifadesi eksik değerleri silmek için kullanılır
df.shape
#(417534, 9)


# Rfm'de outlier temizliği yapmalı mıyız? Yapılabilir,
# ama burada outlier bizim için 5 skoruna denk geleceği için ve aykırı değer baskılamasında yine aynı değere denk geleceği için aykırı değer incelemesi yapmamayı tercih edebiliriz.

#Veri setinin hikayesinde invoice'ta başında c olan ifadeler vardı bu başında c olan ifadeler iadeleri ifade etmektedir.
#Bu iadelerin de sonucu veriyi anlama bölümünde gördüğümüz bazı eksi değerlerin gelmesin sebep olmaktaydı.

df.describe().T
#                   count        mean        std          min         25%  \
#Quantity    417534.00000    12.75881  101.22042  -9360.00000     2.00000
#Price       417534.00000     3.88755   71.13180      0.00000     1.25000
#Customer ID 417534.00000 15360.64548 1680.81132  12346.00000 13983.00000
#TotalPrice  417534.00000    19.99408   99.91586 -25111.09000     4.25000
#                    50%         75%         max
#Quantity        4.00000    12.00000 19152.00000
#Price           1.95000     3.75000 25111.09000
#Customer ID 15311.00000 16799.00000 18287.00000
#TotalPrice     11.25000    19.35000 15818.40000



#Aykırı değerlerin skorlaştıracağımız zaman önemi kalmayacakmış. Fakat iade olan faturaları veri setinden bir çıkaralım bakalım durum nasıl değişecek. Quantity ve price değişkenlerinde çeşitli problemlere sebep olmuş.
#Öyle bir şey yapmalıyız ki iade edilen faturaları veri setinden çıkarmamız lazım.

df=df[~df["Invoice"].str.contains("C", na=False)] #Invoice değerlerinde başında C olan değerleri kaldırdı.

#RFM Metriklerinin Hesaplanması

#Her bir müşteri özelinde Recency, Frequency, Monetary hesaplamak

#Recency: Müşterinin yeniliği-sıcaklığı: "Analizin yapıldığı tarih" - "İlgili müşterinin son satın alma yaptığı tarih"
#Frequency: Müşterinin yaptığı toplam satın almadır
#Monetary: Müşterinin yaptığı satın almalar neticesinde bıraktığı parasal değerdir.


df.head() #Veri setini yine bir hatırlayalım

#Analizi yaptığınız günü belirlemek gerekiyor. İlgili hesaplamaların yapılması için analizin yapıldığı günü tanımlamamız gerekiyor.

#Örneğin bunu nasıl yapabiliriz?
#Veri seti içindeki tarih en son hangi tarih ise, örneğin bu tarih üzerine iki gün koyarız ve bu tarih üzerinden recency hesaplarız.

df["InvoiceDate"].max()
#Timestamp('2010-12-09 20:01:00')
today_date=dt.datetime(2010,12,11) #Ben bir tarih girdim, bu tarihi girdiğimde today_date değişkeni ile tutucam. Sen bunu zaman değişkeni formunda oluştur. talebinde bulunuyoruz bu kod ile.
type(today_date)
# datetime.datetime ;yani bu değişken zaman formunda bir değişken, ki bu bize birazdan yapacağımız işlemlerde zaman açısından fark alabilme imkanı sağlıyor.
#bugünün tarihini yani analizi yaptığımız gün olarak varsaydığımız günü oluşturduk. Şimdi ne yapacağız peki?

#Aslında rfm analizinin temeli basit bir pandas operasyonudur. Buradaki bütün müşterilere göre group by'a alıcaz. Recency, Frequency, Monetary'i kolay bir şekilde hesaplıcaz.

#Recency'i bulmak için ne yapmamız lazım: today_date'ten group by'a aldıktan sonra her bir müşterinin max tarihini bulmamız lazım.
#Today_date'ten çıkardığımızda recency'i bulucaz.

# Ve yine benzer şekilde customer_id'i group by'a aldıktan sonra her bir müşterinin eşsiz fatura sayısına gidersek
# böylece her müşterinin kaç tane eşsiz işlem yaptığını bulmuş oluruz.=Frequency

#Ve yine benzer şekilde customer_id'e göre group by yaptıktan sonra total_price'ların sum'ını aldıktan sonra
#Her bir müşterinin toplam ne kadar para bıraktığını görmüş oluruz. =Monetary


rfm=df.groupby('Customer ID').agg({'InvoiceDate': lambda date: (today_date - date.max()).days,
                                   'Invoice': lambda num: num.nunique(),
                                   'TotalPrice': lambda TotalPrice: TotalPrice.sum()})

rfm.head()
#             InvoiceDate  Invoice  TotalPrice
#Customer ID
#12346.00000          165       11   372.86000
#12347.00000            3        2  1323.32000
#12348.00000           74        1   222.16000
#12349.00000           43        3  2671.14000
#12351.00000           11        1   300.93000

rfm.columns=['recency', 'frequency', 'monetary']

#             recency  frequency   monetary
#Customer ID
#12346.00000      165         11  372.86000
#12347.00000        3          2 1323.32000
#12348.00000       74          1  222.16000
#12349.00000       43          3 2671.14000
#12351.00000       11          1  300.93000

rfm.describe().T #Bir betimleyelim ne durumdayız

rfm[rfm["monetary"] > 0]
rfm=rfm[rfm["monetary"] > 0]#monetary min değerinin sıfır olması istediğimiz durum değil, bunu uçurmamız lazım

rfm.describe().T

#Sonuç: Faturalarda çeşitli ürünler vardı, faturalar toplam bedeli ifade edecek şekilde bizim tarafımızdan dönüştürüldü, yapısallaştırıldı.

#Artık yeni veri setimiz bu, yeni veri setimizdeki müşteri sayımız da:
rfm.shape
#(4312, 3)

#5. RFM Skorlarının Hesaplanması

#Önemli!! Recency ters, frequency ve monetary düz bir şekilde büyüklük küçüklük algısı var.

#qcut fonksiyonu çeyrek değerlere göre bölme işlemi yapan bir fonksiyondur. Burada işimizi görecektir. Bir methodtur
#quantile fonk. der ki bana bir değişken ver, bu değişkeni kaç parçaya bölmek istediğini söyle ve bölme işlemi sonrasında labelları/etiketleri söyle der.

rfm["recency_score"]=pd.qcut(rfm['recency'], 5, labels=[5,4,3,2,1])
#Quantile fonksiyonu bir değişkeni küçükten büyüğe sıralar. Belirli parçalara göre bunu böler. Verilen labellarla parçaları/aralıktaki değerleri eşleştiriyor.
#0-100 , 0-20, 20-40, 40-60, 60-80, 80-100

rfm
#iyi olana 5, kötü olana 1 şeklinde bir puanlama sağladı.
#             recency  frequency   monetary recency_score
#Customer ID
#12346.00000      165         11  372.86000             2
#12347.00000        3          2 1323.32000             5
#12348.00000       74          1  222.16000             2
#12349.00000       43          3 2671.14000             3
#12351.00000       11          1  300.93000             5
#              ...        ...        ...           ...
#18283.00000       18          6  641.77000             4
#18284.00000       67          1  461.68000             3
#18285.00000      296          1  427.00000             1
#18286.00000      112          2 1296.43000             2
#18287.00000       18          4 2345.71000             4

rfm["monetary_score"]=pd.qcut(rfm['monetary'], 5, labels=[1,2,3,4,5])

rfm
#             recency  frequency   monetary recency_score monetary_score
#Customer ID
#12346.00000      165         11  372.86000             2              2
#12347.00000        3          2 1323.32000             5              4
#12348.00000       74          1  222.16000             2              1
#12349.00000       43          3 2671.14000             3              5
#12351.00000       11          1  300.93000             5              2
#              ...        ...        ...           ...            ...
#18283.00000       18          6  641.77000             4              3
#18284.00000       67          1  461.68000             3              2
#18285.00000      296          1  427.00000             1              2
#18286.00000      112          2 1296.43000             2              4
#18287.00000       18          4 2345.71000             4              5
#[4312 rows x 5 columns]

#frequency'de bir miktar değişiklik var diye önce monetary hesapladık.

#hata alıyor value hatası, oluşturulan aralıkta unique değerler yer almamaktadır diyor: o kadar fazla tekrar eden bir frekans var ki küçükten büyüğe sıralandığında çeyrek değerlere düşen değerler aynı olmuş. Daha fazla sayıda aralığa hep aynı değerler denk gelecek şekilde ilerlemiş.
#işte bu sorunu çözmek için rank methodunu kullanıyoruz, method first diyerek ilk gördüğünü ilk sınıfa ata bilgisini  vermiş oluyoruz.

rfm["frequency_score"]=pd.qcut(rfm['frequency'].rank(method="first"), 5, labels=[1,2,3,4,5])
rfm


#şimdi bu değerler üzerinden SKOR BİLEŞENİ oluşturmamız gerekiyor. monetary'i sadece gözlemlemek adına hesapladık.

rfm["RFM_SCORE"] = (rfm['recency_score'].astype(str) +
                    rfm['frequency_score'].astype(str))

rfm

rfm.describe().T
#label oluştururken de bunlar string tipte olduğundan dolayı rfm.describe().T fonksiyonunda yeni oluşturduğum değişkenler gelmez. Sayısal değişkenler gibi analiz edilmedi.

rfm[rfm["RFM_SCORE"] == "55"] #GÖRMÜŞ OLDUĞUNUZ MÜŞTERİLER CHAMPİON MÜŞTERİLERİMİZ.frequency_score

rfm[rfm["RFM_SCORE"] == "11"]

#6. RFM SEGMENTLERİNİN OLUŞTURULMASI VE ANALİZ EDİLMESİ (Creating & Analysing RFM Segments)

#regex: regular expression: R'sinde 5 F'sinde 5 gördüğüne champion yaz... tarzında bir amaç için kullanıcaz. Programcılıkta olan bir kavram.

#RFM İsimlendirmesi

seg_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_Risk',
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}

#Bunu veri setine nasıl uyguluycaz? string methodu olan replace methodunu kullanarak. argüman olarak regex ifadesini vericez.
#Böylece skorları birleştirmiş olucaz.
rfm['segment']=rfm['RFM_SCORE'].replace(seg_map, regex=True)
rfm

#Bu segmentleri oluşturdum şimdi ne yapıcam?
#Öncelikle bu segmentlerin bir analizini yapmak lazım. Bu işle ilgilenenler(takım lideri, direktör, diğer departmanlar vs) burada bi bilgilendirmeli.
#Bizim şu sınıflarımız var. Şu sınıların özellikleri de bunlardır gibi denmeli. Ne gibi özellikler?

#örneğin bu sınıflardaki kişilerin recency ortalamaları ne? frequency ortalamaları ne?

rfm[["segment", "recency", "frequency", "monetary"]].groupby("segment").agg(["mean", "count"])
#                      recency       frequency         monetary
#                         mean count      mean count       mean count
#segment
#about_to_sleep       53.81924   343   1.20117   343  441.32000   343
#at_Risk             152.15876   611   3.07365   611 1188.87832   611
#cant_loose          124.11688    77   9.11688    77 4099.45000    77
#champions             7.11916   663  12.55354   663 6852.26417   663
#hibernating         213.88571  1015   1.12611  1015  403.97784  1015
#loyal_customers      36.28706   742   6.83019   742 2746.06735   742
#need_attention       53.26570   207   2.44928   207 1060.35700   207
#new_customers         8.58000    50   1.00000    50  386.19920    50
#potential_loyalists  18.79304   517   2.01741   517  729.51099   517
#promising            25.74713    87   1.00000    87  367.08678    87

#Müşterilerin need attention kısmına odaklanmak istiyoruz diyor pazarlama departmanı

rfm[rfm["segment"] == "need_attention"].head()

rfm[rfm["segment"] == "cant_loose"].head()

rfm[rfm["segment"] == "cant_loose"].head()
rfm[rfm["segment"] == "new_customers"].index #bu müşterilerin ID'lerini ifade ediyor.

new_df = pd.DataFrame()
new_df["new_customer_id"]=rfm[rfm["segment"] == "new_customers"].index
new_df["new_customer_id"]= new_df["new_customer_id"].astype(int) #ondalıklardan kurtulmak için astype int
new_df

new_df.to_csv("new_customers.csv")

rfm.to_csv("rfm.csv")

#Tüm Sürecin Fonksiyonlaştırılması (Functionalization)


#=Tüm sürecin bir scripte çevrilmesi
#Bir fonksiyon yazdığınızda bu fonksiyonun temel programlama prensiplerince taşıması gereken bazı özellikler olur :
# do one thing= sadece bir şeyi yap
# don't repeat yourself=kendini tekrar edecek işlemler için bir fonk. yaz
# modüler olması

#RFM analizinde yaptığımız bir çok işlem var, normalde buradaki tüm işlemler için ayrı ayrı fonksiyon yazmak fonksiyon yazma çerçevesinde daha verimli olabilir.
#Fakat bizim buradaki temel değerlendirme yaklaşımımız şu olucak:
#Biz bir script yazıyoruz ve özellikle bunu bir fonksiyonla temsil ediyoruz. Dolayısıyla Bu fonksiyonu çağırdığımızda ve bu fonksiyone
#belirli bir dataframe'i sorduğumuzda çok seri bir şekilde bütün analiz işlemleri tamamlansın ve bir sonuç yazılsın istiyoruz.

def create_rfm(dataframe, csv=True):

    #VERIYI HAZIRLAMA
   dataframe["TotalPrice"] = dataframe["Quantity"] * dataframe["Price"] #Totalprice hesaplanmış
   dataframe.dropna(inplace=True) #eksik değerler uçurulmuş
   dataframe=dataframe[~dataframe["Invoice"].str.contains("C", na=False)] #c barındıran ifadeler uçurulmuş

   #RFM METRİKLERİNİN HESAPLANMASI
   today_date=dt.datetime(2011,12,11)
   rfm=dataframe.groupby('Customer ID').agg({'InvoiceDate': lambda date: (today_date - date.max()).days,
                                            'Invoice': lambda num: num.nunique(),
                                            'TotalPrice': lambda price: price.sum()})
   rfm.columns = ['recency', 'frequency', 'monetary']
   rfm = rfm[(rfm['monetary'] > 0)]

   #RFM SKORLARININ HESAPLANMASI
   rfm["recency_score"] = pd.qcut(rfm['recency'], 5, labels=[5,4,3,2,1])
   rfm["frequency_score"] = pd.qcut(rfm["frequency"].rank(method='first'), 5,  labels= [1,2,3,4,5])
   rfm["monetary_score"]=pd.qcut(rfm['monetary'], 5, labels=[1,2,3,4,5])

   #bu skorları hesaplarken bir string dönüşüm gerçekleştirmiştik. Bu string dönüşümler gerçekleştirilmiş rfm skorları R ve F değerleri üzerinden oluşturulmuş:
   #cltv_df skorları kategorik değere dönüştürülüp df'e eklendi.
   rfm["RFM_SCORE"] = (rfm['recency_score'].astype(str)+
                       rfm['frequency_score'].astype(str))

    #SEGMENTLERİN İSİMLENDİRİLMESİ
    seg_map = {
        r'[1-2][1-2]': 'hibernating',
        r'[1-2][3-4]': 'at_risk',
        r'[1-2]5': 'cant_loose',
        r'3[1-2]': 'about_to_sleep',
        r'33': 'need_attention',
        r'[3-4][4-5]': 'loyal_customers',
        r'41': 'promising',
        r'51': 'new_customers',
        r'[4-5][2-3]': 'potential_loyalists',
        r'5[4-5]': 'champions'
    }

    rfm['segment'] = rfm['RFM_SCORE'].replace(seg_map, regex=True)
    rfm=rfm[["recency", "frequency", "monetary", "segment"]]
    rfm.index=rfm.index.astype(int) #Custormer_ID'leri integer olarak gelmesi için

    if csv:
        rfm.to_csv("rfm.csv")

    return rfm



df=df_.copy() #veri setinin ilk haline geri dönelim
df #veri setinin ilk hali

rfm_new = create_rfm(df)
rfm_new


#çıktımızın csv'sini de mi oluştursak:
# rfm.to_csv("rfm.csv") #bölümünü fonksiyonumuza bi özellik olarak ekleyelim

#Artık sadece bu fonksiyonu tanımlarım, bu fonksiyonu tanımladıktan sonra veri setimi okuturum, rfm_new = create_rfm(df) bu satırı çalıştırınca hem nihai dataframe hem de csv dosyasının oluşmuş olmasını bekleim.


#Alt özellikler için fonksiyondaki ayrı ayrı fonksiyonlar yazabilirim, ayrı ayrı yazdıktan sonra ara işlemlere müdahale etme hakkı buluruz.

#Bu analiz dönem dönem tekrar edilebilir. Belirli bir yılın belirli bir ayında bu segmentleri oluşturduğumuzda segmentlerin içerisinde yer alan müşteriler birkaç ay sonra alışveriş yapış şekillerine göre alında segmentlerinde değişiklik gösterilmesi gerekecektir.
#Buradaki değişimleri gözlemlemek oldukça kritiktir. Her ay çalıştırılmalı ve belirli departmanlara çalışma sonucunu rapor etmek mühimdir.

#verilen aksiyon tavsiyelerinin sonucunu da devam ettirmek elzemdir. Bir ayağı hep burada kalması gerekir.
#segmentler arasında yapılan aksiyonlara göre değişim var mı?  değişim vadeden segmentler kimlerdir? yeni aksiyonlar neler olabilir? Başarılı olduk mu?











