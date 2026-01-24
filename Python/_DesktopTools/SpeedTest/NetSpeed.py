# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆
# ☆ Author: ☆ MelodyHSong ☆
# ☆ Language: Python
# ☆ File Name: NetSpeed.py
# ☆ Date: 2026-01-24
# ☆
# ☆ Description: Measures download, upload, and ping using Speedtest.net API.
# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆

import speedtest

def run_speed_test():
    try:
        print("☆ Initializing Speed Test... Please wait.")
        st = speedtest.Speedtest()
        
        # Finding the best server based on ping
        st.get_best_server()
        
        print("☆ Testing Download Speed...")
        download_speed = st.download() / 1_000_000  # Convert bits to Mbps
        
        print("☆ Testing Upload Speed...")
        upload_speed = st.upload() / 1_000_000    # Convert bits to Mbps
        
        ping = st.results.ping
        
        print("\n" + "☆" * 20)
        print(f"☆ Ping: {ping:.2f} ms")
        print(f"☆ Download: {download_speed:.2f} Mbps")
        print(f"☆ Upload: {upload_speed:.2f} Mbps")
        print("☆" * 20)
        
    except Exception as e:
        print(f"☆ Error: {e}")

if __name__ == "__main__":
    run_speed_test()
