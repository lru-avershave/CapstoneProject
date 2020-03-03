from .serverside_table import ServerSideTable
from .table_schemas import SERVERSIDE_TABLE_COLUMNS

class TableBuilder(object):

    def collect_data_clientside(self):
        return {'data': self.data}

    def collect_data_serverside(self, request, data):
        columns = SERVERSIDE_TABLE_COLUMNS
        return ServerSideTable(request, data, columns).output_result()