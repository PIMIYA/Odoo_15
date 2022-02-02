python版本 3.9

postgresql版本 13

## Pull images from docker hub ##

### odoo ###

`docker push pimiya/odoo`

### postgres ###

`docker push pimiya/postgres`

## Start an Odoo instance ##

in directory /odoo/

`docker-compose up -d`

You can find the detail in docker-compose.yml file.

#### once you start the odoo instance, the addons and config folder will be created. ####

You can start to create custom addons and interactive with it.



