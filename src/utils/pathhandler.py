import os
import yaml
import platform

class PathHandler:
    def __init__(self, env_type='dev'):
        self.os_type = platform.system()  # 'Darwin' for MacOS, 'Windows' for Windows

        if self.os_type == 'Darwin':
            self.env_type = 'stage'
        else:
            self.env_type = env_type

        print(f'Environment type set to: "{self.env_type}"')

        # Load from config.yaml
        with open('app/config.yaml', 'r') as f:
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

    def print_output_path(self, attribute, path):
        print(f'{attribute} set to: "{path}"')
        print(f'Canonical string representation of `{attribute}` set to: "{repr(path)}"')

    def set_output_paths(self):
        home_dir = self.config['home_dir'].format(username=self.config['username'])
        self.print_output_path('home_dir', home_dir)

        excel_tail_dir = self.format_excel_tail_dir()
        self.print_output_path('excel_tail_dir', excel_tail_dir)


        json_build_tail_dir = self.config['json_build_tail_dir']
        self.print_output_path('json_build_tail_dir', json_build_tail_dir)


        self.excel_output_file_path = self.normalize_path(os.path.join(home_dir, excel_tail_dir))
        self.print_output_path('self.excel_output_file_path', self.excel_output_file_path)

        self.json_build_file_path = self.normalize_path(os.path.join(home_dir, json_build_tail_dir))
        self.print_output_path('self.json_build_file_path', self.json_build_file_path)

# if __name__ == '__main__':
#     # Example usage
#     path_handler = PathHandler(env_type='dev')
#     path_handler.set_output_paths()