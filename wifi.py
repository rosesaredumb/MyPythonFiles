import speedtest, os, platform, subprocess


#class esse:
    #def __init__(self):
        #pass

#def speed_test(self):



def get_wifi_speed():
    st = speedtest.Speedtest()

    print("Getting best server...")
    st.get_best_server()

    print("Testing download speed...")
    download_speed_mbps = st.download() / 1_000_000  # Convert from bits to Mbps
    download_speed_MBps = download_speed_mbps / 8    # Convert Mbps to MBps

    print("Testing upload speed...")
    upload_speed_mbps = st.upload() / 1_000_000  # Convert from bits to Mbps
    upload_speed_MBps = upload_speed_mbps / 8    # Convert Mbps to MBps

    return (download_speed_mbps, download_speed_MBps), (upload_speed_mbps, upload_speed_MBps)

#(download_mbps, download_MBps), (upload_mbps, upload_MBps) = get_wifi_speed()
#print(f"Download Speed: {download_mbps:.2f} Mbps ({download_MBps:.2f} MBps)")
#print(f"Upload Speed: {upload_mbps:.2f} Mbps ({upload_MBps:.2f} MBps)")

def get_wifi_name():
    system = platform.system()

    try:
        if system == "Windows":
            # Windows command to get WiFi name
            result = subprocess.check_output(
                ["netsh", "wlan", "show", "interfaces"], encoding="utf-8", stderr=subprocess.STDOUT
            )
            for line in result.splitlines():
                if "SSID" in line and "BSSID" not in line:
                    return line.split(":")[1].strip()

        elif system == "Darwin":  # macOS
            # macOS command to get WiFi name
            result = subprocess.check_output(
                ["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-I"],
                encoding="utf-8"
            )
            for line in result.splitlines():
                if " SSID" in line:
                    return line.split(":")[1].strip()

        elif system == "Linux":
            # Linux command to get WiFi name
            result = subprocess.check_output(["nmcli", "-t", "-f", "active,ssid", "dev", "wifi"], encoding="utf-8")
            for line in result.splitlines():
                if line.startswith("yes"):
                    return line.split(":")[1].strip()

    except Exception as e:
        return f"Error fetching WiFi name: {e}"

    return "WiFi name could not be determined"

wifi_name = get_wifi_name()
print(f"Connected WiFi Name: {wifi_name}")