import logging
	import sys
	from juju import loop         # python asyncio
	from juju.relation import *
	from juju.model import Model
	from juju.client.connection import Connection
	from juju.client.client import ClientFacade  # 
	from juju import loop
	# \\ This example deploys OAI EPC in current juju controller and collect statstics 
	####################  tox -e example -- examples/add_service_oai_epc.py       ##########################
	async def deploy():
	# Connect to the currently active Juju model
	    model = Model()
	    await model.connect_current()

	    try:
		applications=['oai-hss','oai-mme','oai-spgw','mysql']
		for apps in  range (len(applications)):
			service=application[app]
		         # Deploy a unit oai-hss
			add_epc_app = await model.deploy(
			  'cs:~navid-nikaein/xenial/oai-hss-16',
			  application_name=service',
			  series='xenial',
			  channel='stable',
			)
		        # optionally block until the application is ready
			if '--wait' in sys.argv:       
			    await model.block_until(lambda: add_epc_app.status == 'active')

		# Adding relation
		if '--wait' in sys.argv:
		    await model.block_until(lambda: add_epc_app.status == 'active')
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
		await model.disconnect()   # Disconnect from the api server and cleanup.

	def main():
	    logging.basicConfig(level=logging.INFO)
	    ws_logger = logging.getLogger('websockets.protocol')
	    ws_logger.setLevel(logging.DEBUG)
	    loop.run(deploy())

	if __name__ == '__main__':
	    main()
