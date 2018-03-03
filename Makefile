node_version:=$(shell node -v)
npm_version:=$(shell npm -v)
timeStamp:=$(shell date +%Y%m%d%H%M%S)
app_context:="./docker"

.PHONY: show install_npm build_ui archive_ui test_ui install_py run_api clean cleanprod deploy

show:
	@ echo Timestamp: $(timeStamp)
	@ echo Node Version: $(node_version)
	@ echo npm_version: $(npm_version)

clean:
	echo "cleaning the dist directory"
	@ rm -rf dist
	@ rm -rf dist.tar.gz
	@ rm -rf release/*.tar.gz

install_npm:
	@ npm install --max-old-space-size=400

build_ui:
	echo "building in production mode"
	@ npm run build --prod --max-old-space-size=400

archive_ui:
	@ mkdir -p release
	@ cd dist && tar -czvf ../release/pys3viewerui-$(timeStamp).tar.gz . && cd ..

test_ui:
	echo "test the app"
	@ npm run test

install_py:
    echo "Installing python modules"
    @ sudo yum install gcc openssl-devel bzip2-devel
    @ cd /usr/src
    @ udo wget https://www.python.org/ftp/python/3.6.4/Python-3.6.4.tgz
    @ sudo tar xzf Python-3.6.4.tgz
    @ cd Python-3.6.4
    @ sudo ./configure --enable-optimizations
    @ sudo make altinstall
    @ sudo rm /usr/src/Python-3.6.4.tgz
    @ cd /usr/src/
    @ sudo wget https://pypi.python.org/packages/d4/0c/9840c08189e030873387a73b90ada981885010dd9aea134d6de30cd24cb8/virtualenv-15.1.0.tar.gz#md5=44e19f4134906fe2d75124427dc9b716
    @ sudo /usr/local/bin/pip3.6 install virtualenv-15.1.0.tar.gz

run_api:
    @ echo "Running backend API"
    @ mkdir -p /tmp/pys3viewer
    @ cd /tmp/pys3viewer
    @ git clone https://github.com/amitthk/pys3viewer.git ./
    @ cd /tmp/pys3viewer/
    @ sudo /usr/local/bin/python3.6 setup.py install
    @ /usr/local/bin/python3.6 -m virtualenv pys3venv -p /usr/local/bin/python3.6
    @ source pys3venv/bin/activate
    @ pip install -r requirements.txt
    @ python -m pys3viewerapi.main

cleanprod:
	echo "cleaning the prod directory"
	@ rm -rf $(app_context)/app
	@ cd ./docker && docker-compose stop pys3viewerui

deploy:
	@ mkdir $(app_context)/app
	@ cp ./release/pys3viewerui*.tar.gz $(app_context)/app/
	@ tar -xzvf $(app_context)/app/pys3viewerui*.tar.gz -C $(app_context)/app
	@ echo this command runs under $(this_user) user
	@ cd ./docker && docker-compose up -d --build pys3viewerui

INFO := @bash -c '\
  printf $(YELLOW); \
  echo "=> $$1"; \
  printf $(NC)' SOME_VALUE