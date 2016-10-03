import shutil
import shlex

from .Log import Log
from . import Utils as U
from .Command import ThreadCommand as Command


class Connection:
    history=None

    def __init__(self, name, options, settings={}):

        self.cli = settings.get('cli')[options['type']]
        cli_path = shutil.which(self.cli)

        if cli_path is None:
            Log((
                "'{0}' could not be found by Sublime Text.\n\n" +
                "Please set the '{0}' path in your SQLTools settings " +
                "before continue.").format(self.cli))
            return

        self.settings = settings
        self.rowsLimit = settings.get('show_records', {}).get('limit', 50)
        self.options = options
        self.name = name
        self.type = options['type']
        self.host = options['host']
        self.port = options['port']
        self.username = options['username']
        self.database = options['database']

        if 'encoding' in options:
            self.encoding = options['encoding']

        if 'password' in options:
            self.password = options['password']

        if 'service' in options:
            self.service = options['service']

    def __str__(self):
        return self.name

    def _info(self):
        return 'DB: {0}, Connection: {1}@{2}:{3}'.format(
            self.database, self.username, self.host, self.port)

    def getTables(self, callback):
        query = self.getOptionsForSgdbCli()['queries']['desc']['query']

        def cb(result):
            callback(U.getResultAsList(result))

        Command.createAndRun(self.builArgs('desc'), query, cb)

    def getColumns(self, callback):

        def cb(result):
            callback(U.getResultAsList(result))

        try:
            query = self.getOptionsForSgdbCli()['queries']['columns']['query']
            Command.createAndRun(self.builArgs('columns'), query, cb)
        except Exception:
            pass

    def getFunctions(self, callback):

        def cb(result):
            callback(U.getResultAsList(result))

        try:
            query = self.getOptionsForSgdbCli()['queries'][
                'functions']['query']
            Command.createAndRun(self.builArgs(
                'functions'), query, cb)
        except Exception:
            pass

    def getTableRecords(self, tableName, callback):
        query = self.getOptionsForSgdbCli()['queries']['show records'][
            'query'].format(tableName, self.rowsLimit)
        Command.createAndRun(self.builArgs('show records'), query, callback)

    def getTableDescription(self, tableName, callback):
        query = self.getOptionsForSgdbCli()['queries']['desc table'][
            'query'] % tableName
        Command.createAndRun(self.builArgs('desc table'), query, callback)

    def getFunctionDescription(self, functionName, callback):
        query = self.getOptionsForSgdbCli()['queries']['desc function'][
            'query'] % functionName
        Command.createAndRun(self.builArgs('desc function'), query, callback)

    def execute(self, queries, callback):
        queryToRun = ''

        for query in self.getOptionsForSgdbCli()['before']:
            queryToRun += query + "\n"

        if isinstance(queries, str):
            queries = [queries]

        for query in queries:
            queryToRun += query + "\n"

        queryToRun = queryToRun.rstrip('\n')

        Log("Query: " + queryToRun)

        if Connection.history:
            Connection.history.add(queryToRun)

        Command.createAndRun(self.builArgs(), queryToRun, callback)

    def builArgs(self, queryName=None):
        cliOptions = self.getOptionsForSgdbCli()
        args = [self.cli]

        if len(cliOptions['options']) > 0:
            args = args + cliOptions['options']

        if queryName and len(cliOptions['queries'][queryName]['options']) > 0:
            args = args + cliOptions['queries'][queryName]['options']

        if isinstance(cliOptions['args'], list):
            cliOptions['args'] = ' '.join(cliOptions['args'])

        cliOptions = cliOptions['args'].format(**self.options)
        args = args + shlex.split(cliOptions)

        # Log('Using cli args ' + ' '.join(args))
        return args

    def getOptionsForSgdbCli(self):
        return self.settings.get('cli_options', {}).get(self.type)

    @staticmethod
    def setTimeout(timeout):
        Connection.timeout = timeout
        Log('Connection timeout setted to {0} seconds'.format(timeout))

    @staticmethod
    def setHistoryManager(manager):
        Connection.history = manager
        Log('Connection history defined with max size {0}'.format(manager.getMaxSize()))
