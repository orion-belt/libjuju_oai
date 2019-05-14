# libjuju_oai

Simple program to deploy LTE EPC (OAI) with python libjuju library in lxc local cloud with the help of Juju NFVO.

Prerequisite-<br/>
- [Setup of Juju cloud](https://old-docs.jujucharms.com/2.5/en/clouds-lxd) <br/>
- sudo apt install tox


1. Clone libjuju library

`git clone https://github.com/juju/python-libjuju.git`

2. Clone libjuju_oai and copy this example to library example directory

`git clone https://github.com/kharade-rohan/libjuju_oai.git`

`cp libjuju_oai/add_service_oai_epc.py python-libjuju/examples/`

3. Deploy oai-epc

`tox -e example -- examples/add_service_oai_epc.py`

Here you are ready to play with LTE EPC


