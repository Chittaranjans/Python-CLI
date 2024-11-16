import cmd
import os

class VirtualFileSystem(cmd.Cmd):
    intro = 'Welcome to the virtual file system. Type help or ? to list commands.\n'
    prompt = '(vfs) '

    def __init__(self):
        super().__init__()
        self.current_path = '/'

        # Initialize a simple in-memory file system
        self.file_system = {
            '/': {},
        }

    def do_ls(self, arg):
        """List files and directories in the current directory."""
        current_dir = self.file_system.get(self.current_path, {})
        print(" ".join(current_dir.keys()))

    def do_cd(self, arg):
        """Change directory."""
        if arg in self.file_system.get(self.current_path, {}):
            self.current_path = os.path.join(self.current_path, arg)
        else:
            print(f"No such directory: {arg}")

    def do_mkdir(self, arg):
        """Create a new directory."""
        if arg not in self.file_system.get(self.current_path, {}):
            self.file_system[self.current_path][arg] = {}
            print(f"Directory '{arg}' created.")
        else:
            print(f"Directory '{arg}' already exists.")

    def do_touch(self, arg):
        """Create a new file."""
        if arg not in self.file_system.get(self.current_path, {}):
            self.file_system[self.current_path][arg] = None
            print(f"File '{arg}' created.")
        else:
            print(f"File '{arg}' already exists.")

    def do_exit(self, arg):
        """Exit the virtual file system."""
        print('Goodbye!')
        return True

if __name__ == '__main__':
    VirtualFileSystem().cmdloop()

