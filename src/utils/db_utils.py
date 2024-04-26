# Build of keyvalue pair list (aka dictionnary) from sqlalchemy row
def row2dict(row):
    dictionnary = {}
    for column in row.__table__.columns:
        dictionnary[column.name] = str(getattr(row, column.name))

    return dictionnary
