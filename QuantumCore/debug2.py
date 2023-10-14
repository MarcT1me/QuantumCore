from dataclasses import dataclass
import time
import os
from loguru import logger


class SkipDebug:
    def __init__(self, *args, **kwargs): pass
    def events(self, key): pass


class Debugging:

    @dataclass
    class PSize:

        p_size: dict

        @staticmethod
        def format_project_size(p_bytes) -> str:
            units = ['bytes', 'KB', 'MB', 'GB']
            unit_index = 0

            while p_bytes >= 1024 and unit_index < len(units) - 1:
                p_bytes /= 1024
                unit_index += 1

            return f"{p_bytes:.3f} {units[unit_index]}"

        @property
        def format_size(self) -> str:
            return f"lines = {self.p_size['lines']}, bytes = {self.format_project_size(self.p_size['bytes'])}"

    def __init__(self, *, dir_name=None) -> None:
        self.directory = dir_name if dir_name is not None else os.path.dirname(__file__)  # project directory

        # project size variable
        self.__except_dirs, self.__except_exts, self.__verified_files, self.__str_len, self._proj_size =\
            None,  None,  None,  None,  None,

        current_time = time.time()
        self.__time_list = {
            'start': current_time,
            'get PSize': current_time,
        }

    def __check_dir_size(self, dir_name) -> None:
        """ Recursive function for checking the length of a directory """

        for root, dirs, files in os.walk(dir_name):

            # file length counting
            for file in files:
                _, file_ext = os.path.splitext(file)
                path = os.path.join(root, file)

                if file not in self.__verified_files:
                    # print(f"{' '*self.str_len} '{file}'")

                    if file_ext[1:] not in self.__except_exts:

                        try:
                            with open(path, mode='r', encoding='utf8') as f:
                                f_len = len(f.readlines())
                                # print(f"   length = {f_len}", end=' ,')
                                self._proj_size['lines'] += f_len

                        except UnicodeDecodeError:
                            logger.error(f"\n ERROR: can`t calculate file lines;\n"
                                         f"   {root=} {file=}, {file_ext=}\n"
                                         f" LineCalculateError: try change 'except_dirs' or 'except_exts'")

                    f_size = os.path.getsize(path)
                    # print(f"   size = {f_size}")
                    self._proj_size['bytes'] += f_size

                self.__verified_files.add(file)

            # exclusion of selected directories
            dirs[:] = [directory for directory in dirs
                       if not any(except_dir in directory for except_dir in self.__except_dirs)]

            # recursive directory check call
            for directory in dirs:
                # print(f"\n{' '*self.str_len}----- {directory} -----")
                self.__str_len += 3

                abs_directory = os.path.abspath(os.path.join(root, directory))
                self.__check_dir_size(abs_directory)

                self.__except_dirs.add(directory)

                self.__str_len -= 3

    def get_proj_size(self, except_dirs=None, except_exts=None, except_files=None) -> dict:
        """ Checking the length of files in the selected directory (in the lines)

        note:
          * except_dirs - argument for writing an ARRAY with directories that must be excluded during verification
          * except_texts - an argument for writing an ARRAY with file types that should be excluded during validation
          * except_files - an argument for writing an ARRAY with files that should be excluded during validation

        relief:
          1. write an empty string to except_dirs to skip all directories and read-only files
        """

        # reset variables
        self._proj_size: dict = {
            'lines': 0,
            'bytes': 0
        }
        self.__str_len: int = 0

        self.__verified_files = set()
        [self.__verified_files.add(except_file) for except_file in except_files]\
            if except_files is not None else None

        # directories that are excluded during the check
        self.__except_dirs: set = {'.idea', '__pycache__', 'venv', '.git'}
        [self.__except_dirs.add(except_dir) for except_dir in except_dirs]\
            if except_dirs is not None else None

        # files with extensions that are skipped during verification
        self.__except_exts: set = {'jpg', 'png', 'mp3', 'ogg', 'obj', 'docx',  # various formats
                                   'rar', 'zip',
                                   'pyc', 'pyz', 'pkg',
                                   'ico', 'lnk', 'bin', 'exe', 'dll'}
        [self.__except_exts.add(except_ext) for except_ext in except_exts]\
            if except_exts is not None else None

        # first call recursive function
        self.__check_dir_size(self.directory)

        return self._proj_size

    # def events(self, key):
    #     """ Debug events """
    #     if key == pygame.K_QUOTE:
    #         current_time = time.time()
    #         if current_time >= self.time_list['get PSize'] + 1:
    #             size: Debugging.PSize = Debugging.PSize(self.get_proj_size(
    #                 except_dirs=['build', 'dist']
    #             ))
    #             logger.info(f"\n\nQuantumCore project size = {size.format_size}\n")
    #             self.time_list['get PSize'] = current_time
                

if __name__ == '__main__':
    size = Debugging.PSize(Debugging(dir_name=r'').get_proj_size(
        except_dirs=["build", "dist"])).format_size
    logger.info(f'\n\n{size}\n')
    input()  #mainloop
