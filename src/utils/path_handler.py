import os
import yaml
import platform
# import logging  # todo: re-enable once logging output issue is resolved

class PathHandler:
    def __init__(self, env_type='dev'):
        # @dev: enable for testing purposes
        # self.json_build_file_path = None
        # self.excel_output_file_path = None
        self.os_type = platform.system()  # 'Darwin' for MacOS, 'Windows' for Windows

        # self.os_type = 'Windows'  # @dev: only for testing purposes on mac; be sure to manually change `self.path_handler = PathHandler(env_type=<env_to_test>)` in main.py

        if self.os_type == 'Darwin':
            self.env_type = 'dev'
        else:
            self.env_type = env_type

        print(f'| Operating System: {self.os_type} | Environment: {self.env_type} |')

        # logging.info(f'| Operating System: {self.os_type} | Environment: {self.env_type} |')

        # Load from config.yaml
        with open('config.yaml', 'r') as f:
            self.config = yaml.safe_load(f)[self.env_type]

    def normalize_path(self, path):
        if self.os_type == 'Windows':
            return os.path.normpath(path)
        return path

    def format_excel_tail_dir(self):
        try:
            return self.config['excel_tail_dir'].format(drive=self.config['drive'])
        except KeyError:  # If 'drive' is not in self.config
            return self.config['excel_tail_dir']

    @staticmethod
    def print_output_path(attribute, path):
        print(f'\n| {attribute} | {path} |')
        print(f'Canonical string representation | {repr(path)} |')

    def set_output_paths(self):
        home_dir = self.config['home_dir'].format(username=self.config['username'])
        # self.print_output_path('home_dir', home_dir)
        json_build_tail_dir = self.config['json_build_tail_dir']
        # self.print_output_path('json_build_tail_dir', json_build_tail_dir)

        if self.env_type == 'prod':
            drive = self.config['drive']
            # self.print_output_path('drive', drive)

            excel_tail_dir = self.format_excel_tail_dir()
            # self.print_output_path('excel_tail_dir', excel_tail_dir)

            self.excel_output_file_path = f'{drive}{excel_tail_dir}'

        else:
            excel_tail_dir = self.format_excel_tail_dir()
            # self.print_output_path('excel_tail_dir', excel_tail_dir)

            self.excel_output_file_path = f'{home_dir}{excel_tail_dir}'

        self.json_build_file_path = f'{home_dir}{json_build_tail_dir}'

        self.print_output_path('self.excel_output_file_path', self.excel_output_file_path)
        self.print_output_path('self.json_build_file_path', self.json_build_file_path)


# @dev: only for testing purposes
# if __name__ == '__main__':
#     # Example usage
#     path_handler = PathHandler(env_type='dev')
#     path_handler.set_output_paths()
