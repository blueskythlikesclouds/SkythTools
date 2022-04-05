# Usage
`ShadowModelConverter [source FBX file] [associated model file] [destination shadow model file]`
  
If you leave the destination empty, it's automatically going to be assumed from input.

# Example
`ShadowModelConverter chr_Sonic_shadow_model.fbx chr_Sonic.model chr_Sonic.shadow-model`

# Remarks 
* The shadow model should be an edge manifold mesh, that is, all edges should have a single neighbor and the mesh should have no holes. A non edge manifold mesh is going to have heavy visual artifacts in game.
* The associated model file usually has the same file name as the shadow model. In Sonic's case, they are chr_Sonic.model and chr_Sonic.shadow\-model.