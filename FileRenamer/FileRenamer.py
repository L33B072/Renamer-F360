import adsk.core
import adsk.fusion
import traceback
from .commands import RenameFilesCommand

# Global list to keep all event handlers in scope
handlers = []

def run(context):
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        
        # Create the command definition
        RenameFilesCommand.create_command_definition(ui)
        
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def stop(context):
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        
        # Clean up the UI
        RenameFilesCommand.destroy_command_definition(ui)
        
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))