import logging
import os
from collections import namedtuple
from PySide2.QtCore import Qt, QObject, Slot, Signal
from mailprep.model.qt_edit_types import QtEditTypes
from mailprep.model.property_model import PropertyModel
from utils.logging_decorators import log_call


log = logging.getLogger(__name__)


PROPERTY_GROUP = 'group'
PROPERTY_EDITOR = 'editor'
PROPERTY_DEFAULT = 'default'

JobProperty = namedtuple('JobProperty', ['group', 'editor', 'default'])

job_properties = {
    'Customer': JobProperty('Customer Information', QtEditTypes.Str, None),
    'Department': JobProperty('Customer Information', QtEditTypes.Str, None),
    'Use Custom Campus': JobProperty('Merge Settings', QtEditTypes.Bool, False),
    'Custom Campus Path': JobProperty('Merge Settings', QtEditTypes.Str, None),
}


class JobController:

    def __init__(self, job_file_path, settings):
        self.job_file_path = job_file_path
        self.settings = settings  # JobSettings instance
        self.modified_properties = []

    def get_all_property_names():
        return self.properties.keys()

    def get_property(self, key):
        # Currently returns a value if the property is not listed in properties, but exists in
        # settings (i.e. was set in the .mpjob file). Don't know yet if this should be suppressed
        # Throws key error if property is unsupported
        return self.settings.get(key, self.properties[key][PROPERTY_DEFAULT])

    def set_property(self, key, value):
        if self.settings.set_property(key, value):
            # Mark the field as being modified
            pass
        self.properties[key] = value

    def __repr__(self):
        return f"JobController<job_file_path={self.job_file_path},settings={self.settings}>"


def are_equals(obj1, obj2):
    """Equality check override handing None values to be equal to empty strings"""
    if obj1 == obj2:
        return True
    return (obj1 is None and obj2 == "") or (obj1 == "" and obj2 is None)


class PropertyState(QObject):

    property_state_changed = Signal(bool)

    def __init__(self, value):
        super().__init__()
        self.saved = value
        self.value = value

    def is_changed(self):
        log.debug(f"is_changed: <self.saved={self.saved}> != <self.value={self.value}>")
        return not are_equals(self.saved, self.value)

    def save(self):
        self.saved = self.value

    def set_value(self, value):
        if value != self.value:
            self.value = value
            self.property_state_changed.emit(self.is_changed())

    def get_value(self):
        return value

# I LIKE THIS ONE -- KEEP WORKING ON THIS
class JobManager(QObject):

    job_is_changed = Signal(bool)

    def __init__(self, job_file_path, initial_settings):
        super().__init__()
        self.file_path = job_file_path
        self.directory, self.file_full_name = os.path.split(self.file_path)
        self.file_base_name = os.path.splitext(self.file_full_name)[0]
        self.files = {}
        self.property_states = {}
        self.is_changed = False

        self.property_model = PropertyModel()
        for prop_name, prop_settings in job_properties.items():
            # Get initial value: Either from initial settings or the property default value
            initial_value = initial_settings.get_property(prop_name, prop_settings.default)
            # Set the Qt model that allows properties to be editable
            self.property_model.add_property(
                prop_settings.group, prop_name, prop_settings.editor, initial_value)
            # Create property state instances
            self.property_states[prop_name] = PropertyState(initial_value)
            self.property_states[prop_name].property_state_changed.connect(
                self.on_property_state_changed)

        self.property_model.itemChanged.connect(self.property_changed)

    @Slot()
    def on_property_state_changed(self, is_changed):  # is_changed: bool
        # Short circuit as we know that the overall job state is changed if the emitting property
        # state was changed, otherwise have to loop through all to know for sure
        self.is_changed = is_changed or any([x.is_changed() for x in self.property_states.values()])
        self.job_is_changed.emit(self.is_changed)

    @Slot()
    def property_changed(self, item):  # item: QStandardItem
        """When a property is manually set or updated, set property metadata"""
        property_name = self.get_item_property_name(item)
        if property_name is not None:
            self._set_property_value(property_name, item.data(Qt.DisplayRole))

    @log_call(log)
    def _set_property_value(self, property_name, value):
            self.property_states[property_name].set_value(value)

    def get_item_property_name(self, item):
        property_parent = item.parent()
        row_index = item.index().row()
        if property_parent is not None and property_parent.hasChildren():
            # Child of the changed items parent at column 0 is the property key
            return property_parent.child(row_index, 0).data(Qt.DisplayRole)
        return None

    def __repr__(self):
        return f"JobManager<file_path={self.file_path}>"
