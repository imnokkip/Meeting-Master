
DB_USR_URL = "sqlite:///./db/sql_usrs.db"


usr_engine = create_engine(DB_USR_URL, connect_args={"check_same_thread": False})




Base.metadata.create_all(bind=usr_engine)


Session_usr = sessionmaker(autoflush=False, bind=usr_engine)
