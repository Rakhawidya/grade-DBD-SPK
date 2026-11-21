data_lama = [
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1]
]

k1 = [1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0]

# --- Panjang vektor K1 = akar(jumlah kuadrat) ---
jumlah_k1 = 0
for nilai in k1:
    jumlah_k1 += nilai ** 2
panjang_k1 = jumlah_k1 ** 0.5
print("Jumlah K1  :", jumlah_k1)
print("Panjang K1 :", round(panjang_k1, 4))
print()

hasil_cosine = []

# Hitung untuk setiap data lama ---
for i in range(len(data_lama)):
    penyakit = data_lama[i]

    # Jumlah & panjang vektor data lama
    jumlah_d = 0
    for nilai in penyakit:
        jumlah_d += nilai ** 2
    panjang_d = jumlah_d ** 0.5

    # Dot product: K1 x data lama
    dot = 0
    for j in range(len(k1)):
        dot += k1[j] * penyakit[j]

    # Cosine similarity
    cosine = dot / (panjang_k1 * panjang_d)
    hasil_cosine.append(cosine)

    print(f"K1 terhadap data lama ke-{i + 1}")
    print(f"  Jumlah      = {jumlah_d}")
    print(f"  Panjang     = {panjang_d:.4f}")
    print(f"  Dot product = {dot}")
    print(f"  Cosine      = {dot} / ({panjang_k1:.4f} x {panjang_d:.4f}) = {cosine:.4f}")
    print()

# --- Cari cosine terbesar ---
terbesar = hasil_cosine[0]
indeks = 0
for i in range(1, len(hasil_cosine)):
    if hasil_cosine[i] > terbesar:
        terbesar = hasil_cosine[i]
        indeks = i

print("Nilai cosine terbesar :", round(terbesar, 4))
print("Paling mirip dengan   : data lama ke-" + str(indeks + 1))