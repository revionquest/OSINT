# 🔍 Nickname OSINT

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11%20%7C%203.12-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Version" />
  <img src="https://img.shields.io/badge/License-GPL--3.0-blue.svg?style=for-the-badge" alt="License: GPL-3.0" />
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey?style=for-the-badge&logo=windows" alt="Platform" />
  <img src="https://img.shields.io/badge/OSINT-Reconnaissance-red?style=for-the-badge" alt="OSINT Category" />
</p>

**Nickname OSINT**, hedef bir kullanıcı adını (nickname/handle) 200'den fazla sosyal medya, geliştirici platformu, forum ve web servisinde eşzamanlı olarak araştıran, anti-bot engellerini aşabilen gelişmiş bir açık kaynak istihbarat (OSINT) tarama aracıdır.

Varsayılan olarak **5 paralel headless tarayıcı motoru** kullanarak hızlı, güvenilir ve doğrulanmış profil eşleşmeleri bulur; sonuçları modern ve tek parça bir **HTML raporu** (`index.html`) olarak sunar.

---

## 🚀 Öne Çıkan Özellikler

* **🌐 200+ Geniş Servis Kataloğu:** GitHub, Instagram, Twitter/X, Reddit, TikTok, Telegram, Discord, Chess.com ve 200'ün üzerinde popüler platformda eşzamanlı arama.
* **🤖 Anti-Bot & Cloudflare Koruması:** `undetected-chromedriver` altyapısı sayesinde geleneksel HTTP isteklerinin takıldığı bot korumalarını, CAPTCHA ve Cloudflare kontrollerini aşabilme yeteneği.
* **⚡ Yüksek Performanslı Paralel Mimari:** 5 eşzamanlı çalışan tarayıcı havuzu ile yüzlerce servisi dakikalar içinde tarama.
* **📊 Zengin ve İnteraktif HTML Raporlama:** Her tarama için `reports/` dizininde kendi kendine yeten, filtrelenebilir, bulunan profilleri ve kanıtları özetleyen tek bir `index.html` rapor çıktısı.
* **🧩 İzole Ortam Desteği:** Windows ortamında sistemdeki global Python paketlerini bozmadan `%LOCALAPPDATA%` altında izole sanal ortam oluşturan akıllı `kurulum.py` motoru.
* **🎯 Akıllı Doğrulama:** Yalnızca HTTP durum koduna değil; sayfa başlığı, hata mesajları, yönlendirmeler ve sayfa içeriğindeki kullanıcı adı kanıtlarına bakarak yanlış pozitif (false-positive) oranını en aza indirir.

---

## 📋 Gereksinimler

* **İşletim Sistemi:** Windows 10/11 (64-bit) veya Linux.
* **Python:** 64-bit **Python 3.11** veya **3.12**.
  *(Resmi Python sitesinden indirilebilir: [python.org/downloads](https://www.python.org/downloads/))*
* **Web Tarayıcısı:** Google Chrome (arka planda çalışan undetected-chromedriver için güncel Chrome kurulu olmalıdır).
* **İnternet Bağlantısı:** İlk kurulum ve tarama işlemleri için kararlı bir internet erişimi.

---

## 🛠️ Kurulum ve Kullanım

### Yöntem 1: Windows İçin Tek Tıkla Kullanım (Önerilen)

Windows kullanıcıları için hiçbir komut satırı deneyimi gerekmez:

1. Depoyu indirin veya klonlayın:
   ```bash
   git clone https://github.com/revionquest/OSINT.git
   cd OSINT
   ```
2. **`kurulum.bat`** dosyasını çalıştırın:
   * Sisteminizdeki uygun 64-bit Python 3.11/3.12 sürümünü otomatik tespit eder.
   * Gerekli tüm kütüphaneleri (`undetected-chromedriver`, `selenium`, `beautifulsoup4` vb.) izole bir sanal ortama yükler.
3. **`baslat.bat`** dosyasını çalıştırın:
   * Konsol ekranı açılır ve sizden taranacak kullanıcı adını ister.
   * Tarama tamamlandığında konsolda oluşturulan rapor yolu gösterilir.
4. Çıktı olarak verilen `reports/.../index.html` dosyasını tarayıcınızda açıp sonuçları inceleyin!

> **Not:** `baslat.bat` doğrudan çalıştırıldığında da eksik ortam varsa `kurulum.py` üzerinden kurulumu kendiliğinden tamamlar.

---

### Yöntem 2: Manuel / Komut Satırı ile Çalıştırma

Projeyi terminal üzerinden çalıştırmak isterseniz:

1. Sanal ortamınızı oluşturun ve etkinleştirin:
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Linux/macOS:
   source .venv/bin/activate
   ```
2. Bağımlılıkları yükleyin:
   ```bash
   pip install -r requirements.txt
   ```
3. Taramayı başlatın:
   ```bash
   python nickscan.py <hedef_kullanici_adi>
   ```

---

## 📁 Proje Yapısı

```plaintext
nickname_osint/
├── baslat.bat          # Windows için tek tıkla tarama başlatıcı
├── kurulum.bat         # Windows için otomatik ortam hazırlayıcı
├── kurulum.py          # Akıllı ortam denetleyicisi ve bağımlılık yöneticisi
├── nickscan.py         # Ana OSINT tarama motoru ve profil dedektörü
├── requirements.txt    # Python paket bağımlılıkları
├── LICENSE             # GNU GPL-3.0 Lisans metni
├── LISANSLAR.txt       # Üçüncü taraf lisans ve kaynak bildirimleri
├── .gitignore          # Raporlar ve yerel dosyalar için filtreler
└── reports/            # Oluşturulan HTML raporların saklandığı klasör (Git dışı)
```

---

## 📊 Raporlama

Tarama sona erdiğinde proje kökündeki `reports/` dizini altında tarih ve saat damgasıyla bir klasör oluşturulur:

```plaintext
reports/
└── <kullanici_adi>_<tarih_saat>/
    └── index.html
```

Bu `index.html` dosyasını herhangi bir web tarayıcısında (Chrome, Brave, Firefox, Edge) çift tıklayarak açabilirsiniz:
* **Bulunan Hesaplar:** Kullanıcı adının kesin olarak aktif olduğu platformların doğrudan profil bağlantıları.
* **Belirsiz Durumlar:** CAPTCHA engeli, rate-limit veya özel profil kısıtlaması olan servislerin dökümü.
* **Bulunamayanlar:** Kullanıcı adının boşta olduğu servisler.

---

## ⚖️ Yasal Uyarı ve Etik Kullanım (Disclaimer)

> [!WARNING]
> **Bu araç yalnızca yasal ve etik açık kaynak istihbarat (OSINT) araştırmaları, siber güvenlik farkındalığı ve yetkili güvenlik testleri amacıyla geliştirilmiştir.**
> 
> * Yalnızca kamuya açık olan (herkese açık) profil sayfaları taranır.
> * Herhangi bir şifre kırma, yetkisiz erişim veya sisteme sızma işlemi gerçekleştirilmez.
> * Aynı kullanıcı adının bulunmuş olması, profillerin mutlak surette aynı kişiye ait olduğunu kanıtlamaz.
> * Bu aracın kullanımından doğabilecek her türlü hukuki ve yasal sorumluluk tamamen kullanıcıya aittir. Geliştiriciler sorumluluk kabul etmez.

---

## 📜 Lisans

Bu proje **GNU General Public License v3.0 (GPL-3.0-only)** ile lisanslanmıştır. Tam lisans şartları için [LICENSE](LICENSE) dosyasına göz atabilirsiniz.

Proje bünyesinde yer alan üçüncü taraf kütüphanelerin ve Sherlock veritabanının telif ve lisans bildirimleri için [LISANSLAR.txt](LISANSLAR.txt) dosyasını inceleyebilirsiniz.


(Revion.quest adına geliştirilmiştir)
