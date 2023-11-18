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
* Preview PDF File:
  debug mode:
  - Setting/Technical/Reporting/Reports
  - Search Report(PDF) Name
  - Config Report Type from PDF to HTML
  
  Example:
  
  ![image](https://github.com/PIMIYA/Odoo_15/assets/52248840/f7cf5ad2-d134-458e-ace8-084d0611ce06)

* Pdf report options (Third Party Module)
  Download Link: https://apps.odoo.com/apps/modules/15.0/report_pdf_options/
  
  Example:
  
  ![image](https://github.com/PIMIYA/Odoo_15/assets/52248840/871cde4b-cb25-492d-adaa-8005b2549a1a)

  
