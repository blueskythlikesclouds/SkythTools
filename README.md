# SkythTools

Almost every program here works with drag and drop.

## Common

- PackCpk
	- A program that allows you to extract or create a CPK file.
- terrain2fbx
	- A program that allows you to convert terrain models inside a folder to an FBX file.
	- To have a full conversion, please ensure that you've included everything. You need:
		- .terrain-model
		- .terrain-instanceinfo
		- .material
		- .dds
- terrain2fbx-png
	- Modified version of terrain2fbx to search for PNG textures instead of DDS.

## Sonic Generations

- AnimationExport
	- A Havok Content Tools 2010 options file that allows you to export animations for Sonic Generations.
	- Provided by TwilightZoney.
- BscPack
	- A program that allows you to unpack or create LZ4 compressed archives for the [PBR Shaders](https://gamebanana.com/mods/288953) mod. It also supports unpacking archives from the original game, but archives created using this program are only going to work with the mod enabled.
- cropGIA
	- A program that crops GI textures from a folder of uncompressed gia-###.ar files.
- TransformGensStage
	- A program that allows you to translate, rotate and scale a stage.
- FxPipelineResolutionChanger
	- A program that allows you to change the shadowmap resolution of the FxPipeline Renderer.
- PathImporter
	- A maxscript that allows you to import a .path.xml file.
	- Made by TGE.
- ImportLightList
	- A maxscript that allows you to import light files or a light list file.
	- Made by TwilightZoney.
- SeparateGIA
	- A program that separates lightmap and shadowmap texture from a complete GI map.
- ar0pack
	- A program that allows you to create AR archives with its corresponding ARL file from a folder.
- ar0unpack
	- A program that allows you to extract AR or PFD files.
- collision2fbx
	- A program that converts a .phy.hkx file to an FBX file.
- evsxml
	- A program that converts an EVS file to an XML, and vice versa.
- pfdpackUnleashed
	- A program that creates a PFD file with its corresponding PFI file from a folder to work with Sonic Unleashed.
- ShaderDB
	- A shader database for SonicGLvl 0.5.7 which contains every shader from Sonic Generations and Sonic Unleashed.
	- If you don't want the database to be reset by the editor, make it read-only.
- slwModel2Gens
	- A program that converts a Sonic Lost World model file to a Sonic Generations one.
- TuringFixer
	- A program that regenerates triangle strip data for every model in a stage to fix the crash on Nvidia Turing GPUs. (RTX/GTX 1660 Series)
	- Drag and drop the Packed stage folder that contains the .ar.00/.pfd files. (eg. disk/bb/Packed/ghz200)
- PostRender
	- This is a replacement for Post Render mode in GIAtlasConverter. Conversion is significantly faster.
	- Place your lightmap/shadowmap files in a folder which is named after your stage but with -HedgeGI suffix, for example:
		- ghz200 (contains stage assets)
		- ghz200-HedgeGI (contains lightmap/shadowmap files)
	- You can afterwards drag and drop the Packed stage folder that contains the .ar.00/.pfd files. (in this example's case, ghz200)
	- **Note:** [HedgeGI](https://github.com/blueskythlikesclouds/HedgeGI) is already capable of packing lightmaps into stages. However, you can still use this tool for packing of GI textures generated through other software.
- TerrainBlockGenerator
	- A program that generates terrain block data for a stage to significantly improve the performance.
	- Drag and drop the Packed stage folder that contains the .ar.00/.pfd files. (eg. disk/bb/Packed/ghz200)
	- **Note:** Latest [Hedgehog Converter](https://github.com/DarioSamo/libgens-sonicglvl) is already capable of generating terrain block data. However, you can still use this tool for stages generated with SonicGLvl 0.5.7 or old versions of Hedgehog Converter.
- Unleashed2Generations
	- A program that converts .model, .terrain-model and .material files from Sonic Unleashed to Sonic Generations format.
- UV2Mapper
	- A program that generates lightmap UV2 channel for every terrain model in a stage. This can be used for baking with [HedgeGI](https://github.com/blueskythlikesclouds/HedgeGI).
	- Drag and drop the Packed stage folder that contains the .ar.00/.pfd files. (eg. disk/bb/Packed/ghz200)
	- You can also use this program on individual .terrain-model files. If you want to process all of them at once, make a .bat file. For example:
		- `for %%f in (*.terrain-model) do UV2Mapper "%%f"`
	- **Note**: This tool is available as an option in [HedgeGI](https://github.com/blueskythlikesclouds/HedgeGI) under Tools -> Generate Lightmap UVs.
- YeetVertexColor
	- A program that removes vertex colors from every terrain model in a stage.
	- Drag and drop the Packed stage folder that contains the .ar.00/.pfd files. (eg. disk/bb/Packed/ghz200)
	- **Note:** This tool is available as an option in [HedgeGI](https://github.com/blueskythlikesclouds/HedgeGI) under Tools -> Remove Vertex Colors.

## Sonic Unleashed

- Parameter Dumps
	- A folder containing every .prm.xml file dumped from Sonic Unleashed memory while in Windmill Isle Act 1.

## Sonic Forces

- AnimationExport
	- A Havok Content Tools 2012 options file that allows you to export animations for Sonic Forces and Sonic Lost World.
	- Provided by ĐeäTh.
- sonicForcesHkxConverter
	- A script that converts a .skl.hkx or .anm.hkx file to a Sonic Generations one.
- PathImporter
	- A maxscript that imports .path files.
	- Original script made by arukibree. 
	- Modifications made by Radfordhound.
- PathExporter
	- A maxscript that exports .path files.
	- Splines should be named like this:
		- grpath001_GR
		- svpath001_SV
		- objpath_001
	- Original script made by arukibree.
	- Modifications made by Radfordhound.
- HedgeEdit Templates
	- A folder that contains object templates to be used with HedgeEdit.
- EnableMultiTangentSpace
	- A program that enables multi tangent space option in a material file, thus possibly fixing the flickering which was caused by a stage port.
- EnableShadow
	- A program that enables shadow cast and receive options in a model file.
- ModelOptimizer
	- A program that optimizes a model file, thus greatly decreasing its file size and improving in-game performance.
- SFPac
	- A script that allows you to extract or create PAC files.
- TagTools
	- A script that allows you to manipulate HKX files.

## Sonic Frontiers

- NeedleTextureStreamingPackage
	- This program restores the \*.dds files by loading their respective texture data from the \*.ntsp archives located within the texture_streaming directory.
		- Ensure that needle_texture_streaming_path.txt contains the path to the texture_streaming directory in your game data (e.g. ./SonicFrontiers/image/x64/raw/texture_streaming/).
		- To use this program, simply drag and drop a standalone \*.dds file or folder containing \*.dds files into it.

## Sonic Lost World

- collision2fbx
	- A program that converts a .phy.hkx file to an FBX file.
- gensMaterial2Slw
	- A program that tries to fix crashes that are caused by a material that is directly taken from previous games.
- hhdxml
	- A program that converts an HHD file to an XML, and vice versa.
- Shadow Model Converter
	- A program that converts a FBX file to a shadow model file. Refer to README.md located in the folder for details.

## Sonic '06

- XNO Converter
	- A program that converts a 3D model file to an XNO file.
- 06set2xml
	- A program that converts an '06 set file to a Sonic Generations .set.xml file.
- xno2dae
	- A program that converts an XNO or XNM file to a DAE file. The variations of the formats are also supported. (like GNO, ZNO, INO etc.)

## Sonic Colors

- PathImporter
	- A maxscript that allows you to import a .path.bin file.
	- Original script made by arukibree.
	- Modifications made by SKmaric.
- col2fbx
	- A program that converts a _col.orc file to an FBX file.
- llightConverter
	- A program that converts a _llight.orc file to a Sonic Generations light list file with its corresponding light files.
- orc2xml
	- A program that converts a set .orc file to a Sonic Generations .set.xml file.

## Misc

- AcbFinder
	- A program that searches for ACB and corresponding AWB files in a folder (and subfolders).
	- Useful for games like Dragalia Lost that distribute ACB and AWB files with random file names.
- AMBPack
	- A program that allows you to extract or create an AMB file.
- BayonettaDx
	- A program that converts a BDX/SDX file to an ACB, and vice versa.
- ConvertSpecularToAlpha
	- A program that places the grayscale of a specular image to its alpha channel.
- PlatinumDat
	- A program that extracts or creates a little endian DAT file. (mainly for Bayonetta)
- WemRipper
	- A program that extracts little endian WEM files from any file.

## Credits

A good amount of tools in this repository heavily make use of DarioSamo's [LibGens](https://github.com/DarioSamo/libgens-sonicglvl).

Everything is made by me unless otherwise specified in the list above.