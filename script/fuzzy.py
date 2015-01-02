import numpy as np
import skfuzzy as fuzz
import time
import math
import json
import sys

poin_hasil = {}
poin_hasil['debug'] = {}


# Terima input JSON
json_input = raw_input()
data = json.loads(json_input)


jam = float(data['hours'])

# Jam dan derajat
radianPerJam = math.pi / 24

# Buat input
suhu = np.arange(15, 38, 1)
cahaya = np.arange(0, 10000, 10)
kelembapan = np.arange(0, 100, 10)

poin_hasil['debug']['suhu'] = suhu.tolist()
poin_hasil['debug']['cahaya'] = cahaya.tolist()
poin_hasil['debug']['kelembapan'] = kelembapan.tolist()

# Buat range untuk kategori
pengali = math.sin(radianPerJam * jam)

# Range suhu
suhu_rendah = fuzz.trapmf(suhu, [0, 0, 22+8*pengali, 24+8*pengali])
suhu_sedang = fuzz.trimf(suhu, [22+8*pengali, 24+8*pengali, 26+8*pengali])
suhu_tinggi = fuzz.trapmf(suhu, [24+8*pengali, 26+8*pengali, 40, 40])


poin_hasil['debug']['suhu_rendah'] = suhu_rendah.tolist()
poin_hasil['debug']['suhu_sedang'] = suhu_sedang.tolist()
poin_hasil['debug']['suhu_tinggi'] = suhu_tinggi.tolist()

# Range cahaya
if pengali >= 0 and pengali < 0.01:
    pengali = 0.01

cahaya_gelap = fuzz.trapmf(cahaya, [0, 0, 1000*pengali, 1000*pengali]);
cahaya_sedang = fuzz.trapmf(cahaya, [1000*pengali, 2500*pengali, 5000*pengali, 7500*pengali]);
cahaya_terang = fuzz.trapmf(cahaya, [5000*pengali, 7500*pengali, 10000*pengali, 10000*pengali]);

poin_hasil['debug']['cahaya_gelap'] = cahaya_gelap.tolist()
poin_hasil['debug']['cahaya_sedang'] = cahaya_sedang.tolist()
poin_hasil['debug']['cahaya_terang'] = cahaya_terang.tolist()

# Range Kelembapan (Tetap)
kelembapan_rendah = fuzz.trapmf(kelembapan, [0, 0, 40, 50])
kelembapan_sedang = fuzz.trimf(kelembapan, [40, 50, 60])
kelembapan_tinggi = fuzz.trapmf(kelembapan, [50, 60, 100, 100])

poin_hasil['debug']['kelembapan_rendah'] = kelembapan_rendah.tolist()
poin_hasil['debug']['kelembapan_sedang'] = kelembapan_sedang.tolist()
poin_hasil['debug']['kelembapan_tinggi'] = kelembapan_tinggi.tolist()

# Output
cuaca = np.arange(0, 100, 10)
poin_hasil['debug']['cuaca'] = cuaca.tolist()

cuaca_hujan = fuzz.trapmf(cuaca, [0, 0, 30, 50])
cuaca_berawan = fuzz.trapmf(cuaca, [30, 40, 50, 60])
cuaca_sejuk = fuzz.trapmf(cuaca, [40, 60, 70, 80])
cuaca_cerah = fuzz.trapmf(cuaca, [70, 80, 100, 100])

poin_hasil['debug']['cuaca_hujan'] = cuaca_hujan.tolist()
poin_hasil['debug']['cuaca_sejuk'] = cuaca_sejuk.tolist()
poin_hasil['debug']['cuaca_berawan'] = cuaca_berawan.tolist()
poin_hasil['debug']['cuaca_cerah'] = cuaca_cerah.tolist()


# Kategorisasi
poin_suhu = []
poin_cahaya = []
poin_kelembapan = []

temperature = float(data['temperature'])
lightIntensity = float(data['lightIntensity'])
humidity = float(data['humidity'])

poin_suhu.append(fuzz.interp_membership(suhu, suhu_rendah, temperature))
poin_suhu.append(fuzz.interp_membership(suhu, suhu_sedang, temperature))
poin_suhu.append(fuzz.interp_membership(suhu, suhu_tinggi, temperature))


poin_cahaya.append(fuzz.interp_membership(cahaya, cahaya_gelap, lightIntensity))
poin_cahaya.append(fuzz.interp_membership(cahaya, cahaya_sedang, lightIntensity))
poin_cahaya.append(fuzz.interp_membership(cahaya, cahaya_terang, lightIntensity))

poin_kelembapan.append(fuzz.interp_membership(kelembapan, kelembapan_rendah, humidity))
poin_kelembapan.append(fuzz.interp_membership(kelembapan, kelembapan_sedang, humidity))
poin_kelembapan.append(fuzz.interp_membership(kelembapan, kelembapan_tinggi, humidity))

poin_hasil['debug']['poin_suhu'] = poin_suhu
poin_hasil['debug']['poin_cahaya'] = poin_cahaya
poin_hasil['debug']['poin_kelembapan'] = poin_kelembapan

# Apply Rule (AND => fmin)
rule = []
rule_text = []
imp = []
imp_text = []

for i in range(0, 3):
    for j in range(0, 3):
        for k in range(0, 3):
            rule.append(np.fmin(poin_suhu[i], np.fmin(poin_kelembapan[j], poin_cahaya[k])))
            rule_text.append([i, j, k])

imp.append(np.fmin(rule[0], cuaca_hujan))
imp.append(np.fmin(rule[1], cuaca_hujan))
imp.append(np.fmin(rule[2], cuaca_sejuk))

imp_text.append("hujan")
imp_text.append("hujan")
imp_text.append("sejuk")

imp.append(np.fmin(rule[3], cuaca_hujan))
imp.append(np.fmin(rule[4], cuaca_berawan))
imp.append(np.fmin(rule[5], cuaca_sejuk))

imp_text.append("hujan")
imp_text.append("berawan")
imp_text.append("sejuk")

imp.append(np.fmin(rule[6], cuaca_hujan))
imp.append(np.fmin(rule[7], cuaca_hujan))
imp.append(np.fmin(rule[8], cuaca_sejuk))

imp_text.append("hujan")
imp_text.append("hujan")
imp_text.append("sejuk")

imp.append(np.fmin(rule[9], cuaca_sejuk))
imp.append(np.fmin(rule[10], cuaca_sejuk))
imp.append(np.fmin(rule[11], cuaca_sejuk))

imp_text.append("sejuk")
imp_text.append("sejuk")
imp_text.append("sejuk")

imp.append(np.fmin(rule[12], cuaca_hujan))
imp.append(np.fmin(rule[13], cuaca_berawan))
imp.append(np.fmin(rule[14], cuaca_sejuk))

imp_text.append("hujan")
imp_text.append("berawan")
imp_text.append("sejuk")

imp.append(np.fmin(rule[15], cuaca_hujan))
imp.append(np.fmin(rule[16], cuaca_berawan))
imp.append(np.fmin(rule[17], cuaca_sejuk))

imp_text.append("hujan")
imp_text.append("berawan")
imp_text.append("sejuk")

imp.append(np.fmin(rule[18], cuaca_sejuk))
imp.append(np.fmin(rule[19], cuaca_cerah))
imp.append(np.fmin(rule[20], cuaca_cerah))

imp_text.append("sejuk")
imp_text.append("cerah")
imp_text.append("cerah")

imp.append(np.fmin(rule[21], cuaca_berawan))
imp.append(np.fmin(rule[22], cuaca_cerah))
imp.append(np.fmin(rule[23], cuaca_cerah))

imp_text.append("berawan")
imp_text.append("cerah")
imp_text.append("cerah")

imp.append(np.fmin(rule[24], cuaca_berawan))
imp.append(np.fmin(rule[25], cuaca_sejuk))
imp.append(np.fmin(rule[26], cuaca_cerah))

imp_text.append("berawan")
imp_text.append("sejuk")
imp_text.append("cerah")

poin_hasil['debug']['rule'] = []
poin_hasil['debug']['imp'] = []

for i in rule:
    poin_hasil['debug']['rule'].append(i.tolist())

for i in imp:
    poin_hasil['debug']['imp'].append(i.tolist())


poin_hasil['debug']['rule_text'] = rule_text
poin_hasil['debug']['imp_text'] = imp_text

agregate_membership = imp[0]
for i in range(1, len(imp)):
    agregate_membership = np.fmax(agregate_membership, imp[i])

poin_hasil['debug']['agregate_membership'] = agregate_membership.tolist()

centroid = fuzz.defuzz(cuaca, agregate_membership, 'centroid')
poin_hasil['debug']['centroid'] = centroid

# Get cuaca percentage from centroid
poin_hasil['hujan'] = fuzz.interp_membership(cuaca, cuaca_hujan, centroid)
poin_hasil['sejuk'] = fuzz.interp_membership(cuaca, cuaca_sejuk, centroid)
poin_hasil['berawan'] = fuzz.interp_membership(cuaca, cuaca_berawan, centroid)
poin_hasil['cerah'] = fuzz.interp_membership(cuaca, cuaca_cerah, centroid)

print json.dumps(poin_hasil)


