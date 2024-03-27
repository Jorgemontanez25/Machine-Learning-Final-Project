# Crea el directorio .streamlit si no existe
import os
if not os.path.exists('.streamlit'):
    os.makedirs('.streamlit')

# Crea o abre el archivo config.toml
with open('.streamlit/config.toml', 'w') as f:
    f.write("""
[theme]
base = 'light'
    """)
