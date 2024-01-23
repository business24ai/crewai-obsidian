from langchain.tools import tool
import datetime
import os


class CustomTools():

    @tool("Write File with content")
    def store_note_to_obsidian(content: str) -> str:
        """Useful to write a note to the note taking app obsidian.
           The input to this tool should be a markdown text and 
           is the content of the file you will store on disk.
           
           :param content: str, content to be stored as a note
           """
        try:
            # Path to Obsidian vault
            obsidian_dir = r'C:/temp/'
        
            # Get the current date and time
            current_datetime = datetime.datetime.now()

            # Format the date in the desired format (YYYY-MM-DD_HH-MM-SS)
            formatted_date = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

            # Combine the prefix and formatted date to create the filename
            filename = f"crewai_note_{formatted_date}.md"
                
            # full path prefix obsidian_dir to filename
            full_path = os.path.join(obsidian_dir, filename)
            
            # Write content to file
            with open(full_path, 'w') as file:
                file.write(content)
            
            # return the filename
            return f"File written to {filename}."
        except Exception:
            return "Error with the input for the tool."