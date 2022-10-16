CREATE TABLE IF NOT EXISTS contact_form ( id Integer PRIMARY KEY,
  name varchar(100) NOT NULL,
  email varchar(100) NOT NULL,
  number varchar(11) NOT NULL,
  date datetime NOT NULL UNIQUE,
  picture,
  app_status BOOLEAN
);