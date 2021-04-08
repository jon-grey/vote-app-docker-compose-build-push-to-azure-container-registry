from flask import Flask, request, render_template
import pydocumentdb
import pydocumentdb.document_client as document_client
import os
import socket
import sys

app = Flask(__name__)

# Initialize Cosmos DB
def cosmosdb(client):

    # Check for database - quick hack /fix up proper
    try:
        db = next((data for data in client.ReadDatabases() if data['id'] == COSMOS_DB_DATABASE))
    # Create if missing
    except:
        db = client.CreateDatabase({'id': COSMOS_DB_DATABASE})

    # Check for collection - quick hack /fix up proper
    try:
        collection = next((coll for coll in client.ReadCollections(db['_self']) if coll['id'] == COSMOS_DB_COLLECTION))
    # Create if missing
    except:
        options = {
            'offerEnableRUPerMinuteThroughput': True,
            'offerVersion': "V2",
            'offerThroughput': 400
        }

        # Create a collection
        collection = client.CreateCollection(db['_self'], {'id': COSMOS_DB_COLLECTION}, options)

    # Return collection
    return collection

# Query Cosmos DB
def cosmosQuery(value, client):
    query = { 'query': "SELECT * FROM server s WHERE s['value'] = '" + value + "'" }
    options = {}
    result_iterable = client.QueryDocuments(collection['_self'], query, options)
    results = list(result_iterable);
    return len(results)

# Delete vote records
def cosmosDelete(client):
    query = { 'query': "SELECT * FROM server s" }
    options = {}
    result_iterable = client.QueryDocuments(collection['_self'], query, options)
    results = list(result_iterable);

    for result in results:
        client.DeleteDocument('dbs/' + COSMOS_DB_DATABASE + '/colls/' + COSMOS_DB_COLLECTION + '/docs/' + result['id'], options=options)

# Load configurations from environment or config file
app.config.from_pyfile('config_file.cfg')

# Set UI and vote values
if ("VOTE1VALUE" in os.environ and os.environ['VOTE1VALUE']):
    button1 = os.environ['VOTE1VALUE']
else:
    button1 = app.config['VOTE1VALUE']

if ("VOTE2VALUE" in os.environ and os.environ['VOTE2VALUE']):
    button2 = os.environ['VOTE2VALUE']
else:
    button2 = app.config['VOTE2VALUE']

if ("TITLE" in os.environ and os.environ['TITLE']):
    title = os.environ['TITLE']
else:
    title = app.config['TITLE']

# Set Cosmos DB configurations
if ("COSMOS_DB_ENDPOINT" in os.environ and os.environ['COSMOS_DB_ENDPOINT']):
    COSMOS_DB_ENDPOINT = os.environ['COSMOS_DB_ENDPOINT']
else:
    COSMOS_DB_ENDPOINT = app.config['COSMOS_DB_ENDPOINT']

if ("COSMOS_DB_MASTERKEY" in os.environ and os.environ['COSMOS_DB_MASTERKEY']):
    COSMOS_DB_MASTERKEY = os.environ['COSMOS_DB_MASTERKEY']
else:
    COSMOS_DB_MASTERKEY = app.config['COSMOS_DB_MASTERKEY']

if ("COSMOS_DB_DATABASE" in os.environ and os.environ['COSMOS_DB_DATABASE']):
    COSMOS_DB_DATABASE = os.environ['COSMOS_DB_DATABASE']
else:
    COSMOS_DB_DATABASE = app.config['COSMOS_DB_DATABASE']

if ("COSMOS_DB_COLLECTION" in os.environ and os.environ['COSMOS_DB_COLLECTION']):
    COSMOS_DB_COLLECTION = os.environ['COSMOS_DB_COLLECTION']
else:
    COSMOS_DB_COLLECTION = app.config['COSMOS_DB_COLLECTION']

# Set Title
if app.config['SHOWHOST'] == "true":
    title = socket.gethostname()

# Build Cosmos DB client
client = document_client.DocumentClient(COSMOS_DB_ENDPOINT, {'masterKey': COSMOS_DB_MASTERKEY})

# Initalize Cosmos DB
collection = cosmosdb(client)

@app.route('/', methods=['GET', 'POST'])
def index():

    # How can I remove this from here?
    client = document_client.DocumentClient(COSMOS_DB_ENDPOINT, {'masterKey': COSMOS_DB_MASTERKEY})

    # Vote tracking
    vote1 = 0
    vote2 = 0

    if request.method == 'GET':

        # Get vote results
        vote1 = cosmosQuery(button1, client)
        vote2 = cosmosQuery(button2, client)

        # Return index with values
        return render_template("index.html", value1=vote1, value2=vote2, button1=button1, button2=button2, title=title)

    elif request.method == 'POST':

        if request.form['vote'] == 'reset':
            cosmosDelete(client)
            # Vote tracking
            vote1 = 0
            vote2 = 0

        else:

            # Insert vote result into DB
            vote = request.form['vote']
            client.CreateDocument(collection['_self'],
            {
                'value': vote,
            })

            # Get vote results
            vote1 = cosmosQuery(button1, client)
            vote2 = cosmosQuery(button2, client)

        # Return results
        return render_template("index.html", value1=vote1, value2=vote2, button1=button1, button2=button2, title=title)

if __name__ == "__main__":
    app.run()