CREATE TABLE can_ho (
    ma_can_ho INT PRIMARY KEY,
    tang      SMALLINT       ,
	stt       SMALLINT       , -- so thu tu cua can ho theo tang
    dien_tich NUMERIC(4,2)   , -- m2
    ghi_chu   TEXT
);

CREATE TABLE cam_bien (
	ma_can_ho INT         NOT NULL,
    thoi_gian TIMESTAMPTZ NOT NULL,
    nhiet_do  REAL, -- °C
	do_am     REAL, -- %RH
	pm10      REAL, -- µg/m³
	pm25      REAL, -- µg/m³
    co        REAL, -- ppm
    lpg       REAL, -- ppm
    co2       REAL, -- ppm
    o2        REAL, -- %vol
    no2       REAL, -- ppm
    muc_nuoc  REAL  -- cm
);

CREATE TABLE su_kien (
    ma_su_kien       BIGSERIAL   PRIMARY KEY       ,
	ma_can_ho        INT         NOT NULL          ,
    bat_dau          TIMESTAMPTZ NOT NULL          ,
    ket_thuc         TIMESTAMPTZ                   , -- NULL neu con dang dien ra 
    loai_su_co       SMALLINT    NOT NULL          , -- 1 toi 3: 'ngap_nuoc' | 'ro_ri_gas' | 'chay'   
    muc_nguy_hiem    SMALLINT    NOT NULL          , -- 0 toi 3: 'khong_nguy_hiem' | 'canh_bao' | 'nguy_hiem' | 'khan_cap_tinh_mang'
    trang_thai_xu_li SMALLINT    NOT NULL DEFAULT 0, -- 0 toi 3: 'moi' | 'da_xac_nhan'  | 'da_xu_ly' | 'bao_dong_nham'
    nguon_phat_hien  SMALLINT                      , -- dung so thu tu dinh danh giong 3 cot tren, ten model/rule da phat hien, vd 'isolation_forest_v1'
    ghi_chu          TEXT
);

ALTER TABLE    cam_bien
ADD CONSTRAINT fk_cam_bien_can_ho 
FOREIGN KEY    (ma_can_ho)
REFERENCES     can_ho(ma_can_ho)      ,
ADD CONSTRAINT pk_cam_bien_primary_key
PRIMARY KEY    (ma_can_ho, thoi_gian) ;

ALTER TABLE    su_kien
ADD CONSTRAINT fk_su_kien_can_ho
FOREIGN KEY    (ma_can_ho)
REFERENCES     can_ho(ma_can_ho)      ;

SELECT create_hypertable('cam_bien', 'thoi_gian');

