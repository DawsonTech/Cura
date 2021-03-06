from UM.Application import Application

import re

class PrintInformationPatches():
    def __init__(self, print_information):
        self._print_information = print_information
        self._print_information._setAbbreviatedMachineName = self._setAbbreviatedMachineName

    ##  Created an acronymn-like abbreviated machine name from the currently active machine name
    #   Called each time the global stack is switched
    #   Copied verbatim from PrintInformation._setAbbreviatedMachineName, with a minor patch to set the abbreviation from settings
    def _setAbbreviatedMachineName(self):
        global_container_stack = Application.getInstance().getGlobalContainerStack()
        if not global_container_stack:
            self._print_information._abbr_machine = ""
            return

        ### START PATCH: construct prefix from variant & material
        definition_container = global_container_stack.getBottom()
        if definition_container.getId() == "blackbelt":
            extruder_stack = Application.getInstance().getMachineManager()._active_container_stack
            if not extruder_stack:
                return

            gantry_angle = global_container_stack.getProperty("blackbelt_gantry_angle", "value")
            nozzle_size = str(global_container_stack.getProperty("machine_nozzle_size", "value")).replace(".", "")
            material_type = extruder_stack.material.getMetaDataEntry("material")
            self._print_information._abbr_machine = "%s_%s_%s" % (gantry_angle, nozzle_size, material_type)
            return
        ### END PATCH

        active_machine_type_name = global_container_stack.definition.getName()

        abbr_machine = ""
        for word in re.findall(r"[\w']+", active_machine_type_name):
            if word.lower() == "ultimaker":
                abbr_machine += "UM"
            elif word.isdigit():
                abbr_machine += word
            else:
                stripped_word = self._print_information._stripAccents(word.upper())
                # - use only the first character if the word is too long (> 3 characters)
                # - use the whole word if it's not too long (<= 3 characters)
                if len(stripped_word) > 3:
                    stripped_word = stripped_word[0]
                abbr_machine += stripped_word

        self._print_information._abbr_machine = abbr_machine
