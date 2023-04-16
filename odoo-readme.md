# Odoo Setup

## Install apps

- agriculture_app
- sale_management
- l10n_tw

## Enable development mode

1. `Ctrl+k` 搜尋 `debug`
2. enable debug mode

## Setup

### 銷售

進入 `設定(Settings)` > `銷售(Sales)` > 開啟 `交貨方式(Delivery Methods)`

- 進入 `銷售(Sales)` > `寄送方式(Shipping Methods)` 增加交貨方式
  - 黑貓宅急便
  - 宅配通

### 黑貓

進入 `設定(Settings)` > `Agriculture Settings` > `BlackCatLogisticConfig`，填入下列資訊

- `BlackCat Customer Id`
- `BlackCat API Base URL`
- `BlackCat API Token`

### 宅配通

- `ECAN Customer Id`
- `ECAN API Base URL`
- `ECAN API Token` 為預留暫關閉

### 公司資訊

- 公司地址
- 公司電話(手機或市話)