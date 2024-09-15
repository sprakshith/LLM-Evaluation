import os


class Prompts:
    def __init__(self):
        self.dir_path = os.path.dirname(os.path.realpath(__file__))

    def _read_file(self, path):
        file_path = os.path.join(self.dir_path, path)
        with open(file_path, 'r') as file:
            return file.read()


class SystemArchitectPrompts(Prompts):
    def __init__(self):
        super().__init__()
        self.DB_REQ_SYSTEM_MESSAGE = self._read_file('SystemArchitect/DB-Requirements/DB-Req-System-Message.prompt')
        self.DB_REQ_HUMAN_MESSAGE = self._read_file('SystemArchitect/DB-Requirements/DB-Req-Human-Message.prompt')
        self.TABLE_CREATION_SYSTEM_MESSAGE = self._read_file('SystemArchitect/DB-Requirements/Table-Creation-System-Message.prompt')
        self.TABLE_CREATION_HUMAN_MESSAGE = self._read_file('SystemArchitect/DB-Requirements/Table-Creation-Human-Message.prompt')
        self.ENDPOINTS_EXTRACTION_SYSTEM_MESSAGE = self._read_file('SystemArchitect/Backend-Requirements/Endpoints-Extraction-System-Message.prompt')
        self.ENDPOINTS_EXTRACTION_HUMAN_MESSAGE = self._read_file('SystemArchitect/Backend-Requirements/Endpoints-Extraction-Human-Message.prompt')


class DatabaseArchitectPrompts(Prompts):
    def __init__(self):
        super().__init__()
        self.TABLE_CREATION_SYSTEM_MESSAGE = self._read_file('DatabaseArchitect/Table-Creation/Table-Creation-System-Message.prompt')
        self.TABLE_CREATION_HUMAN_MESSAGE = self._read_file('DatabaseArchitect/Table-Creation/Table-Creation-Human-Message.prompt')


class BackendDeveloperPrompts(Prompts):
    def __init__(self):
        super().__init__()
        self.ENDPOINT_CREATION_SYSTEM_MESSAGE = self._read_file('BackendDevprompts/Backend-System-Message.prompt')
        self.ENDPOINT_CREATION_HUMAN_MESSAGE = self._read_file('BackendDev/Backend-Human-Message.prompt')
