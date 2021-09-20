### TO DO:
- currently a lot of the components use hardcoded guides, parents, spaces, etc., as it made refactoring a lot easier. Those need to be made to take arguments and use them similar to how the spine, head and most of the limb components work
- add better support for loading/saving deformer weights and blendshapes
- the deformer weights and blendshapes are currently scattered across multiple folders, come up with a convention and write the support around that
- come up with a good place to put all the boilerplate housekeeping code like creating the top control, ctls_grp, rig_grp, etc.
- better way to deal with DEBUG_MODE
