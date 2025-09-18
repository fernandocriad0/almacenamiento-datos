import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# -----------------------------
# Título e introducción
# -----------------------------
st.title("📑 Informe de Soluciones de Almacenamiento")
st.markdown("""
Este informe compara **HDD, SSD, Cinta y Nube** bajo criterios de negocio y tecnología:
velocidad, coste, fiabilidad, consumo, seguridad y escalabilidad.

Incluye tablas, gráficos y simulaciones para apoyar decisiones.
""")

# -----------------------------
# 1. Tabla comparativa
# -----------------------------
st.header("🔹 Comparación de Tecnologías")

data = {
    "Tecnología": ["HDD", "SSD", "Cinta", "Nube"],
    "Velocidad Lectura (MB/s)": [200, 2000, 350, 300],
    "Velocidad Escritura (MB/s)": [150, 1800, 300, 250],
    "Capacidad (TB)": [16, 8, 30, 1000],
    "Costo por GB (USD)": [0.025, 0.15, 0.007, 0.05],
    "Fiabilidad (MTBF horas)": [1.2e6, 1.5e6, 2e6, 1.5e6],
    "Consumo (W)": [8, 5, 3, 0],  # nube no aplica directamente
    "Seguridad (1-5)": [3, 4, 2, 5],
    "Escalabilidad (1-5)": [3, 4, 2, 5],
}

df = pd.DataFrame(data)
st.dataframe(df)

# -----------------------------
# 2. Gráfico: Velocidad
# -----------------------------
st.header("📊 Velocidades de Lectura")
fig1, ax1 = plt.subplots()
ax1.bar(df["Tecnología"], df["Velocidad Lectura (MB/s)"])
ax1.set_ylabel("MB/s")
st.pyplot(fig1)

st.header("📊 Velocidades de Escritura")
fig2, ax2 = plt.subplots()
ax2.bar(df["Tecnología"], df["Velocidad Escritura (MB/s)"])
ax2.set_ylabel("MB/s")
st.pyplot(fig2)

# -----------------------------
# 3. Gráfico: Coste
# -----------------------------
st.header("📊 Costo por GB (USD)")
fig3, ax3 = plt.subplots()
ax3.bar(df["Tecnología"], df["Costo por GB (USD)"])
ax3.set_ylabel("USD")
st.pyplot(fig3)

# -----------------------------
# 4. Gráfico radar cualitativo
# -----------------------------
st.header("🕸️ Radar de Fiabilidad, Seguridad y Escalabilidad")

labels = ["Fiabilidad", "Seguridad", "Escalabilidad"]
num_vars = len(labels)

angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
angles += angles[:1]

fig4, ax4 = plt.subplots(subplot_kw=dict(polar=True))

for i, row in df.iterrows():
    values = [row["Fiabilidad (MTBF horas)"]/1e6, row["Seguridad (1-5)"], row["Escalabilidad (1-5)"]]
    # Normalizamos fiabilidad para 1–5 (muy simple)
    values[0] = min(5, values[0])  
    values += values[:1]
    ax4.plot(angles, values, label=row["Tecnología"])
    ax4.fill(angles, values, alpha=0.1)

ax4.set_xticks(angles[:-1])
ax4.set_xticklabels(labels)
ax4.set_yticks(range(1, 6))
ax4.set_yticklabels(map(str, range(1, 6)))
ax4.legend(loc="upper right")
st.pyplot(fig4)

# -----------------------------
# 5. Simulación de crecimiento
# -----------------------------
st.header("🔮 Simulación de Crecimiento y Rendimiento")

vol_inicial = 100  # TB
crecimiento = 0.3  # 30% anual
horizonte = 5      # años

años = list(range(1, horizonte + 1))
volumenes = [vol_inicial * ((1 + crecimiento) ** (a - 1)) for a in años]

sim_data = []
for i, v in enumerate(volumenes):
    fila = {"Año": i + 1, "Volumen (TB)": round(v, 2)}
    for _, row in df.iterrows():
        tiempo = (v * 1024) / row["Velocidad Lectura (MB/s)"]  # tiempo en segundos
        fila[row["Tecnología"]] = round(tiempo, 1)
    sim_data.append(fila)

df_sim = pd.DataFrame(sim_data)
st.dataframe(df_sim)

st.markdown("⚠️ Modelo simplificado: calcula tiempo de lectura secuencial de todo el volumen.")

# -----------------------------
# Conclusión
# -----------------------------
st.header("✅ Conclusiones")
st.write("""
- **SSD**: máximo rendimiento, pero mayor coste inicial.  
- **HDD**: opción equilibrada en coste, limitado en velocidad.  
- **Cinta**: barata, pero poco práctica en acceso rápido.  
- **Nube**: flexible y escalable, depende de la conectividad y tarifas del proveedor.  

👉 Recomendación: **arquitectura híbrida** (SSD para transaccional + Nube para backups y escalabilidad).
""")
