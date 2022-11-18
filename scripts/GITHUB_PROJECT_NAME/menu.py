import maya.cmds as cmds
import maya.mel as mel

from PySide2 import QtGui

NAME_WIDGET = 'GITHUB_PROJECT_NAME_name'
RADIUS_WIDGET = 'GITHUB_PROJECT_NAME_radius'
NEW_BIND_MESH_WIDGET = 'GITHUB_PROJECT_NAME_newbindmesh'
BIND_FILE_WIDGET = 'GITHUB_PROJECT_NAME_bindfile'

BORDER_DDL = "GITHUB_PROJECT_NAME_border_ddl"
REPROJ_CHK = "GITHUB_PROJECT_NAME_reproj_chk"
REPROJ_SLD = "GITHUB_PROJECT_NAME_reproj_sld"

WIDGET_NAMES = (
    BORDER_DDL,
    REPROJ_CHK,
    REPROJ_SLD,
)
MENU_ITEMS = []


def create_menuitems():
    global MENU_ITEMS
    if MENU_ITEMS:
        # Already created
        return
    for menu in ['mainDeformMenu', 'mainRigDeformationsMenu']:
        # Make sure the menu widgets exist first.
        mel.eval('ChaDeformationsMenu MayaWindow|{0};'.format(menu))
        items = cmds.menu(menu, query=True, itemArray=True)
        for item in items:
            if cmds.menuItem(item, query=True, divider=True):
                section = cmds.menuItem(item, query=True, label=True)
            menu_label = cmds.menuItem(item, query=True, label=True)
            if menu_label == 'Delta Mush':
                if section == 'Create':
                    GITHUB_PROJECT_NAME_item = cmds.menuItem(
                        label="GITHUB_PROJECT_NAME",
                        command=create_GITHUB_PROJECT_NAME,
                        sourceType='python',
                        insertAfter=item,
                        parent=menu,
                    )
                    GITHUB_PROJECT_NAME_options = cmds.menuItem(
                        command=display_GITHUB_PROJECT_NAME_options,
                        insertAfter=GITHUB_PROJECT_NAME_item,
                        parent=menu,
                        optionBox=True,
                    )
                    MENU_ITEMS.append(GITHUB_PROJECT_NAME_item)
                    MENU_ITEMS.append(GITHUB_PROJECT_NAME_options)
            elif menu_label == 'Delta Mush' and section == 'Paint Weights':
                item = cmds.menuItem(
                    label="GITHUB_PROJECT_NAME",
                    command=paint_GITHUB_PROJECT_NAME_weights,
                    sourceType='python',
                    insertAfter=item,
                    parent=menu,
                )
                MENU_ITEMS.append(item)


def create_GITHUB_PROJECT_NAME(*args, **kwargs):
    cmds.loadPlugin('GITHUB_PROJECT_NAME', quiet=True)
    nodes = cmds.deformer(type="GITHUB_PROJECT_NAME")
    kwargs = get_create_command_kwargs()
    for node in nodes:
        for attr, value in kwargs.items():
            cmds.setAttr("{0}.{1}".format(node, attr), value)


def get_create_command_kwargs():
    """Gets the GITHUB_PROJECT_NAME command arguments either from the option box widgets or the saved
    option vars.  If the widgets exist, their values will be saved to the option vars.
    @return A dictionary of the kwargs to the GITHUB_PROJECT_NAME command."""
    kwargs = {}

    if cmds.optionMenu(BORDER_DDL, exists=True):
        # The index is 1-based
        val = cmds.optionMenu(BORDER_DDL, query=True, select=True) - 1
        kwargs['borderBehavior'] = val
        cmds.optionVar(intValue=(BORDER_DDL, val))
    else:
        kwargs['borderBehavior'] = cmds.optionVar(query=BORDER_DDL)

    if cmds.checkBoxGrp(REPROJ_CHK, exists=True):
        val = cmds.checkBoxGrp(REPROJ_CHK, query=True, value1=True)
        kwargs['reproject'] = bool(val)
        cmds.optionVar(intValue=(REPROJ_CHK, int(val)))
    else:
        kwargs['reproject'] = bool(cmds.optionVar(query=REPROJ_CHK))

    if cmds.floatSliderGrp(REPROJ_SLD, exists=True):
        val = cmds.floatSliderGrp(REPROJ_SLD, query=True, value=True)
        kwargs['reprojectDivs'] = val
        cmds.optionVar(floatValue=(REPROJ_SLD, val))
    else:
        kwargs['reprojectDivs'] = cmds.optionVar(query=REPROJ_SLD)

    return kwargs



def display_GITHUB_PROJECT_NAME_options(*args, **kwargs):
    cmds.loadPlugin('GITHUB_PROJECT_NAME', qt=True)
    layout = mel.eval('getOptionBox')
    cmds.setParent(layout)
    cmds.columnLayout(adj=True)

    for widget in WIDGET_NAMES:
        # Delete the widgets so we don't create multiple controls with the same name
        try:
            cmds.deleteUI(widget, control=True)
        except RuntimeError:
            pass

    if not cmds.optionVar(exists=BORDER_DDL):
        init_option_vars()

    pinBehaviors = ["None", "Pin", "Slide"]
    cmds.optionMenu(BORDER_DDL, label="Border Behavior")
    for b in pinBehaviors:
        cmds.menuItem(label=b, parent=BORDER_DDL)
    cmds.optionMenu(
        BORDER_DDL, edit=True, value=pinBehaviors[cmds.optionVar(query=BORDER_DDL)]
    )

    cmds.checkBoxGrp(
        REPROJ_CHK,
        numberOfCheckBoxes=1,
        label='reproject',
        value1=cmds.optionVar(query=REPROJ_CHK),
    )

    cmds.floatSliderGrp(
        REPROJ_SLD,
        label='Reproject Divs',
        field=True,
        minValue=0,
        maxValue=3,
        fieldMinValue=0,
        fieldMaxValue=3,
        step=1,
        precision=0,
        value=cmds.optionVar(query=REPROJ_SLD),
    )

    mel.eval('setOptionBoxTitle("GITHUB_PROJECT_NAME Options");')
    mel.eval('setOptionBoxCommandName("GITHUB_PROJECT_NAME");')
    apply_close_button = mel.eval('getOptionBoxApplyAndCloseBtn;')
    cmds.button(apply_close_button, edit=True, command=apply_and_close)
    apply_button = mel.eval('getOptionBoxApplyBtn;')
    cmds.button(apply_button, edit=True, command=create_GITHUB_PROJECT_NAME)
    reset_button = mel.eval('getOptionBoxResetBtn;')
    # For some reason, the buttons in the menu only accept MEL.
    cmds.button(
        reset_button,
        edit=True,
        command='python("import GITHUB_PROJECT_NAME.menu; GITHUB_PROJECT_NAME.menu.reset_to_defaults()");',
    )
    close_button = mel.eval('getOptionBoxCloseBtn;')
    cmds.button(close_button, edit=True, command=close_option_box)
    save_button = mel.eval('getOptionBoxSaveBtn;')
    cmds.button(
        save_button,
        edit=True,
        command='python("import GITHUB_PROJECT_NAME.menu; GITHUB_PROJECT_NAME.menu.get_create_command_kwargs()");',
    )
    mel.eval('showOptionBox')


def apply_and_close(*args, **kwargs):
    """Create the GITHUB_PROJECT_NAME deformer and close the option box."""
    create_GITHUB_PROJECT_NAME()
    mel.eval('saveOptionBoxSize')
    close_option_box()


def close_option_box(*args, **kwargs):
    mel.eval('hideOptionBox')


def reset_to_defaults(*args, **kwargs):
    """Reset the GITHUB_PROJECT_NAME option box widgets to their defaults."""
    cmds.optionMenu(BORDER_DDL, edit=True, value="Pin")
    cmds.checkBoxGrp(REPROJ_CHK, edit=True, value1=False)
    cmds.floatSliderGrp(REPROJ_SLD, edit=True, value=1)


def init_option_vars():
    """Initialize the option vars the first time the ui is run"""
    cmds.optionVar(intValue=(BORDER_DDL, 1))
    cmds.optionVar(intValue=(REPROJ_CHK, 0))
    cmds.optionVar(floatValue=(REPROJ_SLD, 1.0))


def get_wrap_node_from_object(obj):
    """Get a wrap node from the selected geometry."""
    if cmds.nodeType(obj) == 'GITHUB_PROJECT_NAME':
        return obj
    history = cmds.listHistory(obj, pdo=0) or []
    wrap_nodes = [node for node in history if cmds.nodeType(node) == 'GITHUB_PROJECT_NAME']
    if not wrap_nodes:
        raise RuntimeError('No GITHUB_PROJECT_NAME node found on {0}.'.format(obj))
    if len(wrap_nodes) == 1:
        return wrap_nodes[0]
    else:
        # Multiple wrap nodes are deforming the mesh.  Let the user choose which one
        # to use.
        return QtGui.QInputDialog.getItem(
            None, 'Select GITHUB_PROJECT_NAME node', 'GITHUB_PROJECT_NAME node:', wrap_nodes
        )


def get_wrap_node_from_selected():
    """Get a wrap node from the selected geometry."""
    sel = cmds.ls(sl=True) or []
    if not sel:
        raise RuntimeError('No GITHUB_PROJECT_NAME found on selected.')
    return get_wrap_node_from_object(sel[0])


def destroy_menuitems():
    """Remove the GITHUB_PROJECT_NAME items from the menus."""
    global MENU_ITEMS
    for item in MENU_ITEMS:
        cmds.deleteUI(item, menuItem=True)
    MENU_ITEMS = []


def paint_GITHUB_PROJECT_NAME_weights(*args, **kwargs):
    """Activates the paint GITHUB_PROJECT_NAME weights context."""
    sel = cmds.ls(sl=True)
    if not sel:
        return
    wrap_node = get_wrap_node_from_selected()
    if not wrap_node:
        return
    mel.eval(
        'artSetToolAndSelectAttr("artAttrCtx", "GITHUB_PROJECT_NAME.{0}.weights");'.format(
            wrap_node
        )
    )
