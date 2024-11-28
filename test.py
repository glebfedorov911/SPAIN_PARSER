data = """⚡️¡Cita encontrada!

📍Provincia: Barcelona

Oficinas:
🔹CNP COMISARIA SABADELL, BATLLEVELL, 115, SABADELL

📄Servicio: POLICIA- EXPEDICIÓN/RENOVACIÓN DE DOCUMENTOS DE SOLICITANTES DE ASILO

🔗Haz clic en el enlace para registrarte, ¡date prisa! (https://icp.administracionelectronica.gob.es/icpplustieb/citar?p=8&locale=es)

‼️Importante: Cuando tengas la cita, no olvides tomar una captura de pantalla de los datos, porque a veces no llegan los correos de confirmación. Si no pudiste tomar la cita, haz clic en el botón de abajo para resuscribirte a las notificaciones."""

solve = data.split("\n")

provincia = solve[2].split(":")[1][1:]
mesto1 = solve[5][1:]
mesto2 = solve[7][1:]

# HOST=brd.superproxy.io
# PORT=33335
# USER=brd-customer-hl_068e0beb-zone-datacenter_proxy1-country-es
# PASS=nv7t84x2wgps
# API_KEY=1f9de02beecb632ce18e2f657a573a8a

