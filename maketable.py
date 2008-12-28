import markup
from markup import oneliner as e

def MakeTable(TableDict):
    class RowData:
        def opentag(self):
            self.Table.tr.open()
            self.Table.td.open()
        def closetag(self):
            self.Table.td.close()
            self.Table.tr.close()

    RD = RowData()
    Table = markup.page(case='upper')
    Table.table.open(width='50%', border='2')
    RD.opentag
    Table.b('Manufacturer')
    Table.td.close()
    Table.td.open()
    Table.b(TableDict['manuf'])
    RD.closetag
    RD.opentag
    Table.b("Model:")
    Table.td.close()
    Table.td.open()
    Table.b(TableDict['model'])
    RD.closetag
    RD.opentag
    Table.b("Serialnumber:")
    Table.td.close()
    Table.td.open()
    Table.b(TableDict['sn'])
    RD.closetag
    Table.table.close()
    return Table

TableDict = {"manuf":"Schroff","model":"SLE105","sn":"12345"}

print MakeTable(TableDict)
