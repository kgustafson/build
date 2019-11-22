FROM mysql

# Copy the database schema to the /data directory
COPY files/epcis_schema.sql /data/epcis_schema.sql
COPY acronym_schema.sql /docker-entrypoint-initdb.d/acronym_schema.sql 
#COPY acronym_schema.sql /data/acronym_schema.sql 
# Change the working directory
WORKDIR data

RUN mysql -u $MYSQL_USER -p $MYSQL_PASSWORD $MYSQL_DATABASE < epcis_schema.sql
#RUN mysql -u $MYSQL_USER -p $MYSQL_PASSWORD $MYSQL_DATABASE < acronym_schema.sql
