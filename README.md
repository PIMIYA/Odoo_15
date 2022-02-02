## Pull images from docker hub ##

odoo

`docker push pimiya/odoo`

postgres

`docker push pimiya/postgres`

## start an Odoo instance ##

`docker-compose up -d`

## Mount custom addons ##

`docker run -v /path/to/addons:/mnt/extra-addons -p 8069:8069 --name odoo --link db:db -t odoo`

