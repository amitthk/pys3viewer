git clone https://github.com/amitthk/pys3viewer.git
yum install gcc openssl-devel bzip2-devel
sudo yum install gcc openssl-devel bzip2-devel
cd /usr/src
wget https://www.python.org/ftp/python/3.6.4/Python-3.6.4.tgz
sudo wget https://www.python.org/ftp/python/3.6.4/Python-3.6.4.tgz
tar xzf Python-3.6.4.tgz 
sudo tar xzf Python-3.6.4.tgz 
cd Python-3.6.4
sudo ./configure --enable-optimizations
sudo make altinstall
sudo rm /usr/src/Python-3.6.4.tgz
mkdir -p /tmp/pys3viewer/
cd /tmp/pys3viewer/
cd /usr/src/
sudo wget https://pypi.python.org/packages/d4/0c/9840c08189e030873387a73b90ada981885010dd9aea134d6de30cd24cb8/virtualenv-15.1.0.tar.gz#md5=44e19f4134906fe2d75124427dc9b716
sudo /usr/local/bin/pip3.6 install virtualenv-15.1.0.tar.gz 
cd /tmp/pys3viewer/
sudo /usr/local/bin/python3.6 setup.py install
/usr/local/bin/python3.6 -m virtualenv pys3venv -p /usr/local/bin/python3.6
source pys3venv/bin/activate
pip install -r requirements.txt
python -m pys3viewerapi.main