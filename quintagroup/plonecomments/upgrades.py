from Products.GenericSetup.registry import _import_step_registry


def cleanup_old_importsteps(setuptool):
    """ remove import steps from global registry """

    qgcomments_steps = ['quintagroup.plonecomments.install',
                        'quintagroup.plonecomments.uninstall']
    registry_tool = setuptool.getImportStepRegistry()
    global_steps = _import_step_registry.listSteps()
    steps = registry_tool.listSteps()

    # check and remove steps duplicate
    double_steps = [step for step in steps if step in global_steps]
    for step in qgcomments_steps:
        if step in double_steps:
            del registry_tool._registered[step]
