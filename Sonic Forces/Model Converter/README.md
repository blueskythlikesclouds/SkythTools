Drag and drop a FBX/DAE file to get your model/material files.

Sonic Team included metadata at the start of model files, which tells the game to do certain things. I'm going to call them properties. You can add them by adding tags to meshes. Applying to any mesh will apply to the whole model.

Example: `chr_sonic@PRP(ShadowCa, true)@PRP(ShadowRe, true)`  
`ShadowCa` makes model cast shadows and `ShadowRe` makes model receive shadows.  
In some cases though, they hardcode properties to models so they always apply even if it doesn't exist in model file, such as Sonic's player model.

They also used a different way of swapping mouths. Instead of swapping mouths by bone, they swapped them by mesh, using their names. This is also supported by the program.  
You need to have left and right mouth as separate meshes and assign names to them.  
In this case, left mouth should be named `Mesh_Mouth_L` and right mouth should be named `Mesh_Mouth_R`.  
Example: `mouthR@NAME(Mesh_Mouth_R)`