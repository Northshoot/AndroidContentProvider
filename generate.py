import argparse


class Generator():
    def __init__(self, args):
        self.args = args
        self.models = []

    def make_manifest(self):
        pass

    def make_table_columns(self):
        pass

    def make_models(self):
        pass

    def make_wrappers(self):
        #AbstractCursor

        #AbstractContentValuesWrapper

        #AbstractSelection

        #BaseContentProvider

        #BaseModel

        #models
        for model in self.models:
            # Cursor wrapper

            # ContentValues wrapper

            # Selection builder

            # enums appending to one file
            pass

    def make_content_provider(self):
        pass

    def make_sqlite_open_helper(self):
        pass

    def make_generate_sqlite_open_helper_callbacks(self):
        pass

    def make_model_representations(self):
        pass

    def make_model_representer(self):
        pass

    def make_model_change_listner(self):
        pass

    def go(self):
        self.make_table_columns()
        self.make_table_columns()
        self.make_models()
        self.make_wrappers()
        self.make_content_provider()
        self.make_sqlite_open_helper()
        self.make_generate_sqlite_open_helper_callbacks()
        self.make_model_representations()
        self.make_model_representer()
        self.make_model_representer()
        self.make_model_change_listner()




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='This is a demo script by nixCraft.')
    parser.add_argument('-i','--input', help='Input file name',required=True)
    parser.add_argument('-o','--output',help='Output file name', required=True)
    args = parser.parse_args()
    Generator(args).go()
