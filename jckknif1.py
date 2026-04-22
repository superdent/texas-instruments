values = []

print("Werte eingeben, leer = Ende")
while True:
    s = input("Wert: ")
    if s == "":
        break
    values.append(float(s))

n = len(values)
mean_all = sum(values) / n

# Leave-one-out Mittelwerte
loo_means = []
for i in range(n):
    loo = values[:i] + values[i+1:]
    loo_means.append(sum(loo) / (n - 1))

jk_mean = sum(loo_means) / n
bias = (n - 1) * (jk_mean - mean_all)

# SE nach Musterlösung (Originalwerte)
se_orig = 0
for x in values:
    se_orig += (x - mean_all) ** 2
se_orig = ((n - 1) / n * se_orig) ** 0.5

# Jackknife-SE (Leave-one-out)
se_jk = 0
for m in loo_means:
    se_jk += (m - jk_mean) ** 2
se_jk = ((n - 1) / n * se_jk) ** 0.5

def pause():
    input()

print()
for i, m in enumerate(loo_means, start=1):
    print("Ohne Wert", i, ": Mittelwert =", m)
    pause()

print()
print("n =", n)
pause()
print("Mittelwert (gesamt) =", mean_all)
pause()
print("Jackknife-Mittelwert =", jk_mean)
pause()
print("Bias-Schaetzung =", bias)
pause()
print("Standardfehler (Originalwerte) =", se_orig)
pause()
print("Standardfehler (Jackknife) =", se_jk)
