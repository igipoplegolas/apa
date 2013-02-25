from sqlalchemy import create_engine, MetaData, Table, Column
from sqlalchemy import Float, String, Integer

# create engine
engine = create_engine("postgresql://postgres:postgres@localhost/sandbox")
metadata = MetaData(bind=engine)

# define table recipients
recipients = Table("recipients", metadata,
    Column("source_EU", Float),
    Column("source_SK", Float),
    Column("paid_amount", Float),
    Column("currency", String),
    Column("fund", String),
    Column("beneficiary", String),
    Column("zip", String),
    Column("city", String),
    Column("year", Integer)
)

metadata.drop_all();
metadata.create_all()