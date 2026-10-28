from flask import Flask, request
import requests, os
from datetime import datetime

app = Flask(__name__)

# Ambil dari Render Environment Variables
API_KEY = os.environ.get("ca45dd4dbf839eed87c009e01ebc0869ab9add23719a6902e1abf1c69f604313", "")
TOKEN_FONNTE = os.environ.get("RBJzZanVcDgcMamnHqUY", "")

def get_jadwal_bola():
    tgl = datetime.now().strftime("%Y-%m-%d")
        url = f"https://apiv3.apifootball.com/?action=get_events&from={tgl}&to={tgl}&APIkey={API_KEY}"
            try:
                    r = requests.get(url, timeout=20)
                            data = r.json()
                                    if isinstance(data, dict) and 'error' in str(data).lower():
                                                return f"⚠️ Limit API habis bro, coba besok. Error: {data}"
                                                        if not data or len(data) == 0:
                                                                    return f"📭 Hari ini {tgl} gak ada jadwal bola bro"
                                                                            
                                                                                    teks = f"*🔥 JADWAL BOLA HARI INI {tgl}*\n\n"
                                                                                            for m in data[:15]:
                                                                                                        jam = m.get('match_time','??:??')
                                                                                                                    home = m.get('match_hometeam_name','Home')
                                                                                                                                away = m.get('match_awayteam_name','Away')
                                                                                                                                            league = m.get('league_name','')
                                                                                                                                                        teks += f"⏰ {jam} - {home} vs {away}\n   _{league}_\n\n"
                                                                                                                                                                teks += "\nKetik *prediksi [tim]* buat prediksi!"
                                                                                                                                                                        return teks
                                                                                                                                                                            except Exception as e:
                                                                                                                                                                                    return f"Error ambil bola: {e}"

                                                                                                                                                                                    @app.route('/')
                                                                                                                                                                                    def home():
                                                                                                                                                                                        return "BOT BOLA WA ON! ✅"

                                                                                                                                                                                        @app.route('/webhook', methods=['POST'])
                                                                                                                                                                                        def webhook():
                                                                                                                                                                                            data = request.get_json(silent=True) or {}
                                                                                                                                                                                                # Fonnte format beda-beda
                                                                                                                                                                                                    sender = data.get('sender') or data.get('number') or data.get('from') or ""
                                                                                                                                                                                                        message = data.get('message') or data.get('text') or data.get('msg') or ""
                                                                                                                                                                                                            
                                                                                                                                                                                                                if not sender:
                                                                                                                                                                                                                        return "ok", 200

                                                                                                                                                                                                                            message_lower = message.lower()
                                                                                                                                                                                                                                
                                                                                                                                                                                                                                    if "bola" in message_lower or "jadwal" in message_lower:
                                                                                                                                                                                                                                            balasan = get_jadwal_bola()
                                                                                                                                                                                                                                                elif "halo" in message_lower or "hai" in message_lower or "p" in message_lower:
                                                                                                                                                                                                                                                        balasan = "Halo bro! 👋 Ketik *bola* buat liat jadwal hari ini"
                                                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                                                    balasan = get_jadwal_bola()

                                                                                                                                                                                                                                                                        # Kirim balik via Fonnte
                                                                                                                                                                                                                                                                            try:
                                                                                                                                                                                                                                                                                    requests.post("https://api.fonnte.com/send",
                                                                                                                                                                                                                                                                                                headers={"Authorization": TOKEN_FONNTE},
                                                                                                                                                                                                                                                                                                            json={"target": sender, "message": balasan},
                                                                                                                                                                                                                                                                                                                        timeout=15
                                                                                                                                                                                                                                                                                                                                )
                                                                                                                                                                                                                                                                                                                                    except Exception as e:
                                                                                                                                                                                                                                                                                                                                            print(f"Gagal kirim: {e}")
                                                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                                    return "ok", 200

                                                                                                                                                                                                                                                                                                                                                    if __name__ == '__main__':
                                                                                                                                                                                                                                                                                                                                                        app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))