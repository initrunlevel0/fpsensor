import numpy as np
import skfuzzy as fuzz
import time
import math
import json


# Terima input JSON
json_input = raw_input()
data = json.loads(json_input)


jam = float(data['hours'])

# Jam dan derajat
radianPerJam = math.pi / 24

# Buat input
suhu = np.arange(10, 40, 1)
cahaya = np.arange(10, 40000, 10)
kelembapan = np.arange(0, 100, 10)

# Buat range untuk kategori
pengali = math.sin(radianPerJam * jam) 

# Range suhu
suhu_rendah = fuzz.trapmf(suhu, [20+8*pengali, 20+8*pengali, 22+8*pengali, 24+8*pengali])
suhu_sedang = fuzz.trimf(suhu, [22+8*pengali, 24+8*pengali, 26+8*pengali])
suhu_tinggi = fuzz.trapmf(suhu, [24+8*pengali, 26+8*pengali, 28+8*pengali, 28+8*pengali])

# Range cahaya
cahaya_gelap = fuzz.trapmf(cahaya, [10*pengali, 10*pengali, 10+10*pengali, 20+10*pengali])
cahaya_sedang = fuzz.trimf(cahaya, [20+10*pengali, 30+10*pengali, 40+10*pengali])
cahaya_terang = fuzz.trapmf(cahaya, [20*pengali, 30*pengali, 40+10*pengali, 40+10*pengali])

# Range Kelembapan (Tetap)
kelembapan_rendah = fuzz.trapmf(kelembapan, [30, 30, 40, 50])
kelembapan_sedang = fuzz.trimf(kelembapan, [40, 50, 60])
kelembapan_tinggi = fuzz.trapmf(kelembapan, [60, 70, 100, 100])

# Output
cuaca = np.arange(0, 100, 10)

cuaca_hujan = fuzz.trapmf(cuaca, [0, 0, 30, 50])
cuaca_sejuk = fuzz.trapmf(cuaca, [30, 40, 50, 60])
cuaca_berawan = fuzz.trapmf(cuaca, [40, 50, 60, 70])
cuaca_cerah = fuzz.trapmf(cuaca, [70, 80, 100, 100])


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

# Apply Rule (AND => fmin)
rule = []
imp = []

for i in range(0, 3):
    for j in range(0, 3):
        for k in range(0, 3):
            rule.append(np.fmin(poin_suhu[i], np.fmin(poin_kelembapan[j], poin_cahaya[k])))

imp.append(np.fmin(rule[0], cuaca_hujan))
imp.append(np.fmin(rule[1], cuaca_hujan))
imp.append(np.fmin(rule[2], cuaca_sejuk))

imp.append(np.fmin(rule[3], cuaca_hujan))
imp.append(np.fmin(rule[4], cuaca_hujan))
imp.append(np.fmin(rule[5], cuaca_sejuk))

imp.append(np.fmin(rule[6], cuaca_hujan))
imp.append(np.fmin(rule[7], cuaca_hujan))
imp.append(np.fmin(rule[8], cuaca_sejuk))

imp.append(np.fmin(rule[9], cuaca_sejuk))
imp.append(np.fmin(rule[10], cuaca_sejuk))
imp.append(np.fmin(rule[11], cuaca_berawan))

imp.append(np.fmin(rule[12], cuaca_sejuk))
imp.append(np.fmin(rule[13], cuaca_sejuk))
imp.append(np.fmin(rule[14], cuaca_berawan))

imp.append(np.fmin(rule[15], cuaca_sejuk))
imp.append(np.fmin(rule[16], cuaca_sejuk))
imp.append(np.fmin(rule[17], cuaca_berawan))

imp.append(np.fmin(rule[18], cuaca_berawan))
imp.append(np.fmin(rule[19], cuaca_cerah))
imp.append(np.fmin(rule[20], cuaca_cerah))

imp.append(np.fmin(rule[21], cuaca_berawan))
imp.append(np.fmin(rule[22], cuaca_cerah))
imp.append(np.fmin(rule[23], cuaca_cerah))

imp.append(np.fmin(rule[24], cuaca_berawan))
imp.append(np.fmin(rule[25], cuaca_cerah))
imp.append(np.fmin(rule[26], cuaca_cerah))



agregate_membership = imp[0]
for i in range(1, len(imp)):
    agregate_membership = np.fmax(agregate_membership, imp[i])

centroid = fuzz.defuzz(cuaca, agregate_membership, 'centroid')

# Get cuaca percentage from centroid
poin_hasil = {}
poin_hasil['hujan'] = fuzz.interp_membership(cuaca, cuaca_hujan, centroid)
poin_hasil['sejuk'] = fuzz.interp_membership(cuaca, cuaca_sejuk, centroid)
poin_hasil['berawan'] = fuzz.interp_membership(cuaca, cuaca_berawan, centroid)
poin_hasil['cerah'] = fuzz.interp_membership(cuaca, cuaca_cerah, centroid)

print json.dumps(poin_hasil)


