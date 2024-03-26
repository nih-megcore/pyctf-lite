
import os
import textwrap

def writeClassFile(fname_out):       

    file_content = f"""\
    PATH OF DATASET:
    {fname_out}

    
    NUMBER OF CLASSES:
    1


    CLASSGROUPID:
    3
    NAME:
    BAD
    COMMENT:

    COLOR:
    Red
    EDITABLE:
    Yes
    CLASSID:
    1
    NUMBER OF TRIALS:
    0
    LIST OF TRIALS:
    TRIAL NUMBER


    """

    file_content = textwrap.dedent(file_content)

    # Write the file content to a file
    with open(f"{fname_out}/ClassFile.cls", "w") as file:
        file.write(file_content)



def checkClassFile(fname):

    ''' 
    Load ClassFile.cls. 
    Check and return if "Aborted" class is found in file
    
    Parameters
    ----------
    fname : str
        Path String.

    '''
    was_aborted = False
    
    # Open the file
    with open(os.path.join(fname,'ClassFile.cls'), "r") as file:
        # Initialize variables to store class information
        number_of_class = None
        names = []

        # Read the file line by line
        for line in file:
            # Strip whitespace characters from the beginning and end of each line
            line = line.strip()

            # Check if the line contains "NUMBER OF CLASSES"
            if line.startswith("NUMBER OF CLASSES:"):
                # The actual number is on the next line
                number_of_class = int(next(file).strip())
            # Check if the line contains "NAME"
            elif line.startswith("NAME:"):
                # The actual name is on the next line
                names.append(next(file).strip())
                if "Aborted" in names:
                    was_aborted = True
                # Break the loop if all names are collected
                if len(names) == number_of_class:
                    break

    return was_aborted 