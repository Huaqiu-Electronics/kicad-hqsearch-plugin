import sys
import wx
import wx.dataview as dv

#----------------------------------------------------------------------

# This model class provides the data to the view when it is asked for.
# Since it is a list-only model (no hierarchical data) then it is able
# to be referenced by row rather than by item object, so in this way
# it is easier to comprehend and use than other model types.  In this
# example we also provide a Compare function to assist with sorting of
# items in our model.  Notice that the data items in the data model
# object don't ever change position due to a sort or column
# reordering.  The view manages all of that and maps view rows and
# columns to the model's rows and columns as needed.
#
# For this example our data is stored in a simple list of lists.  In
# real life you can use whatever you want or need to hold your data.
# 定义列的最大数量
MAX_COLS = 2

class PartDetailsModel(dv.DataViewIndexListModel):
    def __init__(self, data ):
        dv.DataViewIndexListModel.__init__(self, len(data))
        self.data = data

        # self.log = log

    # This method is called to provide the data object for a
    # particular row,col
    def GetValueByRow(self, row, col):
        
        if col < 0 or col >= MAX_COLS:
            return None 
        try:
            return self.data[row][col]
        
        except IndexError as e:
            print(f"Error: Row index {row} is out of range. {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None
    
    
    def GetAttrByRow(self, row, col, attr):
        # print('GetAttrByRow: (%d, %d)' % (row, col))
        if col == 0 and self.data[row][col] == _("Show more"):
            attr.SetColour('blue')  
            return True

        return False

    # This method is called when the user edits a data item in the view.
    def SetValueByRow(self, value, row, col):
        if 0 <= col < len(self.data[row]):
            self.data[row][col] = value
            self.RowChanged(row)
            return True
        return False

    # Report how many columns this model provides data for.
    def GetColumnCount(self):
        return MAX_COLS  

    # Specify the data type for a column
    def GetColumnType(self, col):
        return "string" 
    
    # Report the number of rows in the model
    def GetCount(self):
        #self.log.write('GetCount')
        return len(self.data)


    # This is called to assist with sorting the data in the view.  The
    # first two args are instances of the DataViewItem class, so we
    # need to convert them to row numbers with the GetRow method.
    # Then it's just a matter of fetching the right values from our
    # data set and comparing them.  The return value is -1, 0, or 1,
    # just like Python's cmp() function.
    def Compare(self, item1, item2, col, ascending):
        row1 = self.GetRow(item1)
        row2 = self.GetRow(item2)
        if col == 0:
            return (self.data[row1][0] > self.data[row2][0]) - (self.data[row1][0] < self.data[row2][0]) if ascending else -1 * ((self.data[row1][0] > self.data[row2][0]) - (self.data[row1][0] < self.data[row2][0]))
        else:
            return 0
       
    def DeleteRows(self, rows):
        rows = list(rows)
        # use reverse order so the indexes don't change as we remove items
        rows.sort(reverse=True)

        for row in rows:
            if row < 0 or row >= self.GetCount():
                print(f"Delete Error: Row index {row} is out of range. It must be between 0 and {self.GetCount() - 1}.")
                continue

            # notify the view(s) using this model that it will be removed
            self.RowDeleted(row)

        for row in rows:
            try:
                del self.data[row]
            except IndexError:
                print(f"Delete Error: Row index {row} is out of range for data structure.")
                continue

    def DeleteAll( self ):
        total_rows = self.GetCount()
        self.data = []
        for row in range(total_rows - 1, -1, -1):
            self.RowDeleted(row)

    def AddRow(self, value):
        # update data structure
        self.data.append(value)
        # notify views
        self.RowAppended()

    def AddRows(self, values):
        for row_index, new_value in enumerate(values):
                self.data.append(new_value)
                self.RowAppended()
