import numpy as np
import matplotlib.pyplot as plt


def to_float(x):
    try:
        return float(x)
    except ValueError:
        return np.nan


def ucitavanje_podataka(fajl):
    data = np.loadtxt(fajl, dtype=str, ndmin=2)

    image = data[:, 0]
    vreme = data[:, 1]

    # IRAF upise  INDEF ako qphot nije uspeo da izmeri vrednost
    mag = np.array([to_float(x) for x in data[:, 4]])
    merr = np.array([to_float(x) for x in data[:, 5]])

    return image, vreme, mag, merr


## X/Y offset ###################

# citamo slike redom iz qatar.list
with open("qatar.list", "r") as f:
    slike = [line.strip() for line in f if line.strip()]

x_values = []
y_values = []

for slika in slike:
    coo_file = slika.replace(".fit", ".coo")
    data = np.loadtxt(coo_file, ndmin=2)

    # prva zvezda u .coo fajlu je target zvezda Qatar-2
    x_values.append(data[0, 0])
    y_values.append(data[0, 1])

x_values = np.array(x_values)
y_values = np.array(y_values)

# pomeraj u odnosu na prvi frejm
dx = x_values[0] - x_values
dy = y_values[0] - y_values

frames_offset = np.arange(1, len(slike) + 1)

plt.figure(figsize=(9, 5))
plt.plot(frames_offset, dx, "-", label="X-Shifts (Drift teleskopa)")
plt.plot(frames_offset, dy, "-", label="Y-Shifts (Korekcija polja)")
plt.xlabel("Broj frejma")
plt.ylabel("Pomeraj u pikselima")
plt.title("Pomeraji piksela u odnosu na referentni frejm")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

## Kontrolna i poredbena zvezda ############################

img_t, time, mag_t, err_t = ucitavanje_podataka("target.dat")
img_c, _, mag_comp, err_comp = ucitavanje_podataka("comparison.dat")
img_ch, _, mag_check, err_check = ucitavanje_podataka("check.dat")

frames = np.arange(1, len(mag_t) + 1)


## Grafik: posmatrana - poredbena ############################

# minus stavljamo da tranzit izgleda kao pad krive sjaja
diff_target_comp = -(mag_t - mag_comp)

# uklanjamo tacke gde je qphot vratio INDEF
valid_target = np.isfinite(diff_target_comp)

plt.figure(figsize=(9, 5))
plt.plot(
    frames[valid_target],
    diff_target_comp[valid_target],
    "o-",
    markersize=3,
    linewidth=1
)
plt.xlabel("Redni broj slike")
plt.ylabel("Magnituda poredbene umanjena za magnitudu posmatrane zvezde")
plt.title("Razlika magnituda: posmatrana - poredbena zvezda")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()


## Grafik: kontrolna - poredbena ############################

# kontrolna zvezda sluzi kao provera stabilnosti merenja
diff_check_comp = -(mag_check - mag_comp)

# uklanjamo tacke gde je qphot vratio INDEF
valid_check = np.isfinite(diff_check_comp)

plt.figure(figsize=(9, 5))
plt.plot(
    frames[valid_check],
    diff_check_comp[valid_check],
    "o-",
    markersize=3,
    linewidth=1
)
plt.xlabel("Redni broj slike")
plt.ylabel("Magnituda poredbene umanjena za magnitudu kontrolne zvezde")
plt.title("Kontrolna provera: kontrolna - poredbena zvezda")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()


## Rezultati ###############################

print("Broj analiziranih frejmova:", len(frames))

print("\nPosmatrana - poredbena:")
print("Broj izbacenih tacaka:", len(frames) - np.sum(valid_target))
print("Srednja razlika magnituda:", np.nanmean(diff_target_comp))
print("Standardna devijacija:", np.nanstd(diff_target_comp))

print("\nKontrolna - poredbena:")
print("Broj izbacenih tacaka:", len(frames) - np.sum(valid_check))
print("Srednja razlika magnituda:", np.nanmean(diff_check_comp))
print("Standardna devijacija:", np.nanstd(diff_check_comp))


