drop table if exists entries;
create table surveyresults (
  id SERIAL PRIMARY KEY ,
  email VARCHAR(255) NOT NULL,
  answers VARCHAR(255) NOT NULL
);


CREATE TABLE vendors (
            vendor_id SERIAL PRIMARY KEY,
            vendor_name VARCHAR(255) NOT NULL
        )


INSERT INTO surveyresults (email, answers) VALUES ('test2@gmail.com', 'yes yes yes');
