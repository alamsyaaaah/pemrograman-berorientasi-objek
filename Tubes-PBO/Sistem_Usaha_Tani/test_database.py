from database import setup_database

if setup_database():
    print("Database berhasil dibuat!")
else:
    print("Database gagal dibuat!")