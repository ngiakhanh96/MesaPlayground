import xlsxwriter
import os

from xlsxwriter.worksheet import Worksheet

class Report():
    def __init__(self, agv_agent_statistics_collection_dict, person_agent_list):
        self.agv_agent_statistics_collection_dict = agv_agent_statistics_collection_dict
        self.person_agent_list = person_agent_list
        self.export_dir = 'reports'
        self.export_file_name = 'report.xlsx'
        self.path_to_file = os.path.join(self.export_dir, self.export_file_name)

    def export(self):
        self.prepare_path_and_file()

        self.workbook = xlsxwriter.Workbook(self.path_to_file)

        self.export_summary_sheet('Overall summary')
        self.export_person_agent_working_time_sheet('Detailed agent processing time')
        self.export_person_agent_waiting_time_sheet('Detailed agent waiting time')

        self.workbook.close()

    def prepare_path_and_file(self):
        if not os.path.exists(self.export_dir):
            os.mkdir(self.export_dir)
        else:
            if os.path.exists(self.path_to_file):
                os.remove(self.path_to_file)

    def prepare_worksheet(self, sheet_name, first_col=0, last_col=3, col_width=30):
        worksheet = self.workbook.add_worksheet(sheet_name)
        worksheet.set_column(first_col, last_col, col_width)
        return worksheet

    def write_header(self, row, col, content, worksheet: Worksheet):
        header_format = self.workbook.add_format({'border': 1, 'bold': True, 'align': 'center'})
        worksheet.write(row, col, content, header_format)

    def write_cell(self, row, col, content, worksheet: Worksheet, align_right = True, bold = False):
        cell_format = self.workbook.add_format({'border': 1})
        if (align_right == True):
            cell_format.set_align('right')
        if (bold == True):
            cell_format.set_bold(True)
        worksheet.write(row, col, content, cell_format)

    def export_summary_sheet(self, sheet_name):
        worksheet = self.prepare_worksheet(sheet_name, 0, 3, 50)

        # Write data headers.
        self.write_header(0, 1, 'Total processing time at all stations (seconds)', worksheet)
        self.write_header(0, 2, 'Total waiting time (seconds)', worksheet)
        self.write_header(0, 3, 'Total moving time (seconds)' , worksheet)

        # Start from the first cell below the headers.
        row = 1
        col = 0

        # Iterate over the person_agent_list and write it out row by row.
        for person_agent in self.person_agent_list:
            self.write_cell(row, col    , 'Worker ' + person_agent.name        , worksheet, False, True)
            self.write_cell(row, col + 1, person_agent.total_working_step_count, worksheet)
            self.write_cell(row, col + 2, person_agent.total_waiting_step_count, worksheet)
            self.write_cell(row, col + 3, person_agent.total_moving_step_count , worksheet)
            row += 1

        for agv_name, agv_agent_statistics in self.agv_agent_statistics_collection_dict.items():
            self.write_cell(row, col    , 'AGV ' + agv_name, worksheet, False, True)
            self.write_cell(row, col + 1, 'N/A'            , worksheet)
            self.write_cell(
                row, 
                col + 2, 
                'N/A' 
                if agv_agent_statistics['waiting_step_count'] is None else agv_agent_statistics['waiting_step_count'], 
                worksheet)
            self.write_cell(
                row, 
                col + 3, 
                'N/A' 
                if agv_agent_statistics['moving_step_count']  is None else agv_agent_statistics['moving_step_count'], 
                worksheet)
            row += 1

    def export_person_agent_working_time_sheet(self, sheet_name):
        spot_id_list = self.person_agent_list[0].working_step_count_dict.keys()
        worksheet = self.prepare_worksheet(sheet_name, 0, len(spot_id_list), 15)

        row = 0
        col = 1

        # Write data headers.
        for spot_id in spot_id_list:
            self.write_header(row, col, 'Station ' + spot_id, worksheet)
            col += 1

        row = 1
        col = 0

        # Iterate over the person_agent_list and write it out row by row.
        for person_agent in self.person_agent_list:
            internal_col = col
            self.write_cell(row, internal_col    , 'Worker ' + person_agent.name        , worksheet, False, True)
            internal_col += 1
            for spot_id, working_step_count in person_agent.working_step_count_dict.items():
                self.write_cell(row, internal_col, working_step_count, worksheet)
                internal_col += 1
            row += 1

    def export_person_agent_waiting_time_sheet(self, sheet_name):
        spot_id_list = self.person_agent_list[0].working_step_count_dict.keys()
        worksheet = self.prepare_worksheet(sheet_name, 0, len(spot_id_list), 15)

        row = 0
        col = 1

        # Write data headers.
        for spot_id in spot_id_list:
            self.write_header(row, col, 'Station ' + spot_id, worksheet)
            col += 1

        row = 1
        col = 0

        # Iterate over the person_agent_list and write it out row by row.
        for person_agent in self.person_agent_list:
            internal_col = col
            self.write_cell(row, internal_col    , 'Worker ' + person_agent.name        , worksheet, False, True)
            internal_col += 1
            for spot_id, waiting_step_count in person_agent.waiting_step_count_dict.items():
                self.write_cell(row, internal_col, waiting_step_count, worksheet)
                internal_col += 1
            row += 1