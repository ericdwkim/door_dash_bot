import pandas as pd

class ExcelFormatter:
    def __init__(self, xlsxwriter, sheet_name, df):
        self.workbook = xlsxwriter.book
        self.worksheet = xlsxwriter.sheets[sheet_name]
        self.df = df

        # Create common formats upfront
        self.wrap_txt_format = self.workbook.add_format({
            'text_wrap': True,
            'align': 'center',
            'valign': 'vcenter',
            'font_size': 36,
        })

        self.bold_wrap_format = self.workbook.add_format({
            'text_wrap': True,
            'bold': True,
            'align': 'center',
            'valign': 'vcenter',
            'font_size': 36,
        })

    def set_format(self, start_col, end_col, cell_format):
        """Set format for a range of columns."""
        self.worksheet.set_column(start_col, end_col, None, cell_format)

    def find_max_lengths(self):
        """Find the maximum string lengths for each column in a DataFrame."""
        max_lengths = {}
        for col in self.df.columns:
            max_lengths[col] = max(self.df[col].astype(str).apply(len).max(),
                                    len(str(col)))
        return max_lengths

    def apply_column_formats(self):
        """Apply column formatting and widths based on content length."""
        max_lengths = self.find_max_lengths()
        for idx, col in enumerate(max_lengths.keys()):
            col_width = max_lengths[col] + 1  # Add 1 for a bit of padding
            self.set_format(idx + 1, idx + 1, self.wrap_txt_format)
            self.worksheet.set_column(idx + 1, idx + 1, col_width)

    def apply_first_column_format(self):
        """Apply formatting to the first column and adjust its width."""
        index_as_series = pd.Series(self.df.index.astype(str))
        index_length = max(index_as_series.apply(len).max(),
                           len(str(self.df.index.name)))
        col_width = index_length + 1
        self.set_format(0, 0, self.bold_wrap_format)
        self.worksheet.set_column(0, 0, col_width)

    def apply_sheet_formats(self):
        """Apply sheet formats."""
        self.apply_column_formats()
        self.apply_first_column_format()


