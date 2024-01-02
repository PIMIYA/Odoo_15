python 版本 3.9

postgresql 版本 13

## Start an Odoo instance

`docker-compose up -d`

## Setup

1. 進入 `docker` 安裝 `pypeg2` 與其他綠界電子發票相關套件

以 `root` 身分進入 Container

```sh
docker exec -it --user root {image id} /bin/bash
```

進入後安裝必要套件

```sh
apt-get update
pip install pypeg2
pip install pycryptodome
pip install ecpay_invoice3
apt-get install ttf-wqy-zenhei ttf-wqy-microhei -y
```

2. Odoo install `Dolimi Agriculture`
5. Odoo install `ecpay_invoice_tw`

* 角色管理中，將綠界電子發票的角色設定為 `綠界電子發票管理員`。



## Tips


  
