# SEIR Hastalık Yayılım Simülasyonu

Bu proje, SEIR (Susceptible-Exposed-Infectious-Recovered) epidemiyolojik modelini Python ile simüle eder ve sonuçları görselleştirir.

## Özellikler

- Deterministik SEIR modeli (Euler integrasyonu)
- Zaman adımı (`dt`) ve toplam gün sayısı yapılandırılabilir
- Başlangıç popülasyonu ve başlangıç koşulları yapılandırılabilir
- Zamanla değişen temas oranı `beta(t)` için müdahale desteği
- Çıktıları CSV olarak kaydetme ve grafik çizimi

## Model Denklemleri

Toplam nüfus N = S + E + I + R sabit varsayılır.

```
S' = -β(t) * S * I / N
E' =  β(t) * S * I / N - σ * E
I' =  σ * E - γ * I
R' =  γ * I
```

Burada:
- β: temas/bulaşma oranı
- σ: kuluçkadan bulaştırıcılığa geçiş hızı
- γ: iyileşme/izolasyon hızı

## Kurulum

```bash
pip install -r requirements.txt
```

## Kullanım

### Temel Simülasyon

```bash
python main.py --population 1000000 --beta 0.3 --sigma 0.2 --gamma 0.1 \
  --exposed0 10 --infected0 5 --recovered0 0 --days 160 --dt 0.25 \
  --plot --save_csv outputs/seir.csv --save_plot outputs/seir.png
```

### Müdahale ile Simülasyon

30. günden itibaren temas %40 azaltılsın:

```bash
python main.py --population 1000000 --beta 0.3 --sigma 0.2 --gamma 0.1 \
  --exposed0 10 --infected0 5 --days 160 --dt 0.25 \
  --intervention_day 30 --intervention_reduction 0.4 \
  --plot --save_csv outputs/seir_intervention.csv
```

### Örnek Betik

```bash
python -m examples.run_example
```

## Çıktılar

- **CSV**: Zaman serileri (t, S, E, I, R)
- **Grafik**: SEIR eğrileri

## Proje Yapısı

```
epidemiyoloji/
├── seir/
│   ├── __init__.py
│   ├── model.py          # SEIR modeli ve simülasyon
│   └── plotting.py       # Grafik çizimi
├── examples/
│   └── run_example.py    # Örnek kullanım
├── main.py               # Komut satırı arayüzü
├── requirements.txt      # Python bağımlılıkları
└── README.md            # Bu dosya
```

## Lisans

MIT
