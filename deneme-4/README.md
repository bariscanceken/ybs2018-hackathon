# Destek Sistemi

Bu proje, müşteri ve teknik personel arasındaki destek taleplerini yönetmek için geliştirilmiş bir masaüstü uygulamasıdır.

## Özellikler

- Müşteri ve personel kayıt sistemi
- Destek talebi oluşturma ve takip etme
- Talep durumu güncelleme
- Arama ve filtreleme özellikleri
- Güvenli şifre yönetimi

## Kurulum

1. Python 3.8 veya daha yüksek bir sürümü yükleyin.

2. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

3. MySQL veritabanını kurun ve çalıştırın.

4. Veritabanı kurulumunu yapın:
```bash
python database_setup.py
```

5. Uygulamayı başlatın:
```bash
python main.py
```

## Kullanım

1. İlk kullanımda müşteri veya personel olarak kayıt olun.
2. Giriş yapın.
3. Müşteriler destek talebi oluşturabilir ve mevcut taleplerini görüntüleyebilir.
4. Personel tüm talepleri görüntüleyebilir, durumlarını güncelleyebilir ve yönetebilir.

## Veritabanı Yapılandırması

Veritabanı bağlantı ayarlarını `main.py` dosyasında bulabilirsiniz. Varsayılan ayarlar:

- Host: localhost
- User: root
- Password: (boş)
- Database: destek_db

Bu ayarları kendi MySQL kurulumunuza göre değiştirin. 