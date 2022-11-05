from app.interfaces import cds_downloader 

if __name__ == "__main__":
    downloader = cds_downloader.CDS_downloader(['ammonia','ozone'],"2021-01-01","2021-01-02",)
    downloader.run_request()
