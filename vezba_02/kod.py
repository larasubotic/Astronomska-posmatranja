
import numpy as np
import matplotlib.pyplot as plt

# Učitavanje podataka
# kolone: image, otime, xcenter, ycenter, mag, merr
target = np.loadtxt("target.dat", dtype=str)
comparison = np.loadtxt("comparison.dat", dtype=str)
check = np.loadtxt("check.dat", dtype=str)

# Magnitude su 5. kolona
mag_target = target[:, 4].astype(float)
mag_comparison = comparison[:, 4].astype(float)
mag_check = check[:, 4].astype(float)

# Redni broj slike
x = np.arange(len(mag_target))

# Razlike magnituda
diff_target_comp = mag_target - mag_comparison
diff_target_check = mag_target - mag_check
diff_comp_check = mag_comparison - mag_check

# Grafik: posmatrana - poredbena
plt.figure(figsize=(9, 5))
plt.plot(x, diff_target_comp, ".",color='red', markersize=4)
plt.xlabel("Redni broj slike")
plt.ylabel("m_target - m_comparison")
plt.title("Razlika magnituda: posmatrana i poredbena zvezda")
plt.grid(True)
plt.savefig("target_comparison.png", dpi=300)
plt.show()

# Grafik: posmatrana - kontrolna
plt.figure(figsize=(9, 5))
plt.plot(x, diff_target_check, ".",color='green', markersize=4)
plt.xlabel("Redni broj slike")
plt.ylabel("m_target - m_check")
plt.title("Razlika magnituda: posmatrana i kontrolna zvezda")
plt.grid(True)
plt.savefig("target_check.png", dpi=300)
plt.show()

# Grafik: poredbena - kontrolna
plt.figure(figsize=(9, 5))
plt.plot(x, diff_comp_check, ".", markersize=4)
plt.xlabel("Redni broj slike")
plt.ylabel("m_comparison - m_check")
plt.title("Razlika magnituda: poredbena i kontrolna zvezda")
plt.grid(True)
plt.savefig("comparison_check.png", dpi=300)
plt.show()
