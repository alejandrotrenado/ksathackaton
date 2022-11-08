from app.interfaces import cds_downloader 


if __name__ == "__main__":
    
    downloader = cds_downloader.CDS_downloader(['ammonia','ozone'],"2021-01-01","2021-01-02",[42.6, 0.65, 41.19,2.72])
    # Esto es lo gueno
    # downloader.run_request()
    data = downloader.debug_download()
    print(type(data["time"][0]))
    # data["time"]= data["time"].map(lambda x: str(x)[-8:])
    # print(data["nh3_conc"].max())
    print(data)

