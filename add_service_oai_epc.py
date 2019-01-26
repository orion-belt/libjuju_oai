import logging
import sys

from juju import loop         # python asyncio
from juju.relation import *
from juju.model import Model
from juju.client.connection import Connection
from juju.client.client import ClientFacade  # 
from juju import loop

###
# \\ This example deploys OAI EPC in current juju controller and collect statstics 
####################  tox -e example -- examples/add_service_oai_epc.py       ##########################

async def deploy():
    # Create a Model instance. We need to connect our Model to a Juju api server before we can use it.
    model = Model()

    # Connect to the currently active Juju model
    await model.connect_current()

    try:
                 # Deploy a unit oai-hss
        add_epc_app = await model.deploy(
          'cs:~navid-nikaein/xenial/oai-hss-16',
          application_name='oai-hss',
          series='xenial',
          channel='stable',
        )
        if '--wait' in sys.argv:
            # optionally block until the application is ready
            await model.block_until(lambda: add_epc_app.status == 'active')

                      # Deploy a unit oai-mme
        add_epc_app = await model.deploy(
            'cs:~navid-nikaein/xenial/oai-mme-18',
            application_name='oai-mme',
            series='xenial',
            channel='stable',
        )

        if '--wait' in sys.argv:
            await model.block_until(lambda: add_epc_app.status == 'active')

                     # Deploy a unit mysql
        add_epc_app = await model.deploy(
            'cs:~navid-nikaein/xenial/oai-mme-18',
            application_name='mysql',
            series='xenial',
            channel='stable',
        )
                     # Deploy a unit spgw   ## TO DO ##
                     # add kvm to juju and deploy service here

        if '--wait' in sys.argv:
            await model.block_until(lambda: add_epc_app.status == 'active')
        # Adding relation
        await model.add_relation(
            'mysql',
            'oai-hss',)
        await model.add_relation(
            'oai-mme',
            'oai-hss',)
        #await model.add_relation(   ## TO DO ##
             'oai-mme',
            'oai-spgw',)

    # Getting Statics
    # Hardcoding parameters currently but need to make generic
    conn = await Connection.connect(endpoint='192.168.1.2:17070', uuid=model.info.uuid, username='admin', password='a495665665314c70bb35839236f77925')
    client = ClientFacade.from_connection(conn)
    patterns = None
    status = await client.FullStatus(patterns)

    
    print('Applications:', list(status.applications.keys()))
    print('Machines:', list(status.machines.keys()))
    print('Relations:', status.relations)
    await conn.close()

    finally:
        # Disconnect from the api server and cleanup.
        await model.disconnect()

def main():
    logging.basicConfig(level=logging.INFO)

    # If you want to see everything sent over the wire, set this to DEBUG.
    ws_logger = logging.getLogger('websockets.protocol')
    ws_logger.setLevel(logging.DEBUG)

    # Run the deploy coroutine in an asyncio event loop, using a helper
    # that abstracts loop creation and teardown.
    loop.run(deploy())


if __name__ == '__main__':
    main()
