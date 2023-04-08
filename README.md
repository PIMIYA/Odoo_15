python版本 3.9

postgresql版本 13

## Pull images from docker hub ##

### odoo ###

`docker pull pimiya/odoo`

### postgres ###

`docker pull pimiya/postgres`

## Start an Odoo instance ##

in directory /odoo/

`docker-compose up -d`

You can find the detail in docker-compose.yml file.

已移除使用secret file, 可視情況補上。

## Setup

1. 進入 `docker` 安裝 `pypeg2`
  ```sh
  pip install pypeg2
  ```
  ```sh
  pip install ecpay_invoice3
  ```
  ```sh
  apt-get install ttf-wqy-zenhei -y
  ```
  ```sh
  apt-get install ttf-wqy-microhei -y
  ```
2. Odoo install `Dolimi Agriculture`

## docker compose config
```
version: '3.1'
services:
  web:
    image: pimiya/odoo:latest
    depends_on:
      - db
    ports:
      - "8069:8069"
    volumes:
      - odoo-web-data:/var/lib/odoo
      - ./config:/etc/odoo
      - ./addons:/mnt/extra-addons    
  db:
    image: pimiya/postgres:latest
    environment:
      - POSTGRES_DB=postgres
      - POSTGRES_PASSWORD=odoo
      - POSTGRES_USER=odoo
      - PGDATA=/var/lib/postgresql/data/pgdata
    volumes:
      - odoo-db-data:/var/lib/postgresql/data/pgdata
volumes:
  odoo-web-data:
  odoo-db-data:
```


#### once you start the odoo instance, the addons and config folder will be created. ####

You can start to create custom addons and interactive with it.

## list of new tasks for 2nd stage ##
- [ ] 宅配通API出單串接
- [ ] 綠界invoice電子發票
- [ ] 銷售流程簡化與收穀部分借貸與會計整合
- [ ] 轉穀流程討論與開發（暫定）




