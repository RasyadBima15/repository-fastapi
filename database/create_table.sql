-- SQLBook: Code
CREATE TABLE data_dokumen (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nip VARCHAR(10),
    type_dokumen VARCHAR(50),
    nama_dokumen VARCHAR(100),
    nama_file VARCHAR(100),
    FOREIGN KEY (nip) REFERENCES data_dosen(nip) ON DELETE SET NULL
);

CREATE TABLE data_dosen (
    nip VARCHAR(10) PRIMARY KEY,
    nama_lengkap VARCHAR(100),
    prodi_id INT,
    FOREIGN KEY (prodi_id) REFERENCES data_prodi(id) ON DELETE SET NULL
);

CREATE TABLE data_prodi (
    id INT AUTO_INCREMENT PRIMARY KEY,
    kode_prodi VARCHAR(10),
    nama_prodi VARCHAR(100)
);

CREATE TABLE users (
    id int AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(10) NOT NULL,
    hashed_password VARCHAR(100) NOT NULL
)