

def ipynb_git_stripper(filenames):
    """

    Function to strip output and prompts from an IPython notebook and stage them in the git repository. Prevents spurious changes in the code when it is re-run and outputs change.

    Takes filenames, a list of files to add. Can also be run from the command prompt with a list of files to add as arguments.

    """
    from IPython.nbformat import current
    import io
    from os import remove, rename
    from shutil import copyfile
    from subprocess import Popen
    from sys import argv

    for filename in filenames:
        # Backup the current file
        backup_filename = filename + ".backup"
        copyfile(filename, backup_filename)

        try:
            # Read in the notebook
            with io.open(filename, 'r', encoding='utf-8') as f:
                notebook = current.reads(f.read(), format="ipynb")

            # Strip out all of the output and prompt_number sections
            for worksheet in notebook["worksheets"]:
                for cell in worksheet["cells"]:
                    cell.outputs = []
                    if "prompt_number" in cell:
                        del cell["prompt_number"]

            # Write the stripped file
            with io.open(filename, 'w', encoding='utf-8') as f:
                current.write(notebook, f, format='ipynb')

            # Run git add to stage the non-output changes
            print("git add", filename)
            Popen(["git", "add", filename]).wait()

        finally:
            # Restore the original file;  remove is needed in case
            # we are running in windows.
            remove(filename)
            rename(backup_filename, filename)


if __name__ == "__main__":
    ipynb_git_stripper(argv[1:])
