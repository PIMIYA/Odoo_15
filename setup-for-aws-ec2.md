# Install Office Odoo 15 on Ubuntu 20.04(focal)
# installing without docker
```bash
sudo apt-get update
sudo apt-get upgrade -y

sudo mkdir /etc/odoo
sudo mkdir /opt/odoo
sudo mkdir /opt/odoo-addons
sudo mkdir /var/lib/odoo

# Create odoo user
sudo adduser --system --home=/opt/odoo --group odoo
sudo chown odoo:odoo /opt/odoo -R
sudo chown odoo:odoo /var/lib/odoo -R
sudo chown odoo:odoo /opt/odoo-addons -R

# Install packages
apt-get install -y --no-install-recommends \
  git \
  wget \
  curl \
  python3 \
  python3-pip \
  python3-num2words \
  python3-pdfminer \
  python3-pip \
  python3-phonenumbers \
  python3-pyldap \
  python3-qrcode \
  python3-renderpm \
  python3-setuptools \
  python3-slugify \
  python3-vobject \
  python3-watchdog \
  python3-xlrd \
  python3-xlwt \
  xz-utils \
  gdebi \
  ttf-wqy-zenhei \
  ttf-wqy-microhei \
  xfonts-75dpi

# install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install nodejs
sudo npm install -g rtlcss

# Install wkhtmltopdf
wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.focal_amd64.deb
# Maybe check sha1sum first?
sudo apt-get install -y ./wkhtmltox_0.12.6-1.focal_amd64.deb
sudo cp /usr/local/bin/wkhtmltoimage /usr/bin/wkhtmltoimage
sudo cp /usr/local/bin/wkhtmltopdf /usr/bin/wkhtmltopdf

sudo mkdir /var/log/odoo
sudo chown odoo:odoo /var/log/odoo

# Install Odoo
wget https://nightly.odoo.com/15.0/nightly/deb/odoo_15.0.20220126_all.deb
echo "06fd2afdaa200f8a59a8e9682fcdba1f8f525ca7 odoo_15.0.20220126_all.deb" | sha1sum -c -
apt-get update
apt-get -y install ./odoo_15.0.20220126_all.deb

# Install Odoo requirements
sudo su - odoo -s /bin/bash
pip3 install pypeg2
pip3 install ecpay_invoice3

# Back to root
exit

# Clone Odoo addons
git clone https://github.com/PIMIYA/Odoo_15.git

# Setting Odoo config
sudo vim /etc/odoo/odoo.conf

sudo service odoo restart
```

## odoo.conf

使用 git clone 內的 odoo.conf，再將下列內容加入修改

```ini
addons_path = /usr/lib/python3/dist-packages/odoo/addons, cd addons
data_dir = /opt/odoo
```
