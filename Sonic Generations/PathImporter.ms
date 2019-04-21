
/*
Last update: 8-4-2016
In case there are any issues, contact me.
*/

/**************/
/*** Globals ***/
/**************/
global GPI_Debug = false

fn GPI_PrintDebug str =
(
	if (GPI_Debug) then print str
)

/**********************/
/*** Generic helpers ***/
/**********************/
struct UpAxisHelper
(
	fn FlipVectorUp vec =
	(
		return [vec.X, vec.Z * -1, vec.Y]
	),
	
	fn FlipMatrixUp m =
	(
		return m * matrix3 	[1, 0, 0, 0] \
									[0, 0, 1, 0] \
									[0, -1, 0, 0] \
									[0, 0, 0, 1]
	)
)

/*******************************/
/*** .NET Xml class wrappers ***/
/*******************************/
DotNet.LoadAssembly "System.Xml"

struct XMLAttribute
(
	Name,
	Value
)

struct XMLNode
(
	/* Private members */
	m_init = false,
	m_node,
	
	/* Static method */
	fn Create dnNode = 
	(
		try (m_init) catch ("Can't use this method through an instance reference.")
		
		local newNode = XMLNode()
		newNode.m_node = dnNode
		newNode.m_init = true
		
		return newNode
	),
	
	-- Attributes
	fn GetAttributes = 
	(
		local ret = #()
		local attribs = m_node.Attributes
		for i = 0 to (attribs.Count - 1) do
		(
			local t = XMLAttribute()
			local item = (attribs.ItemOf i)
			t.Name = item.Name
			t.Value = item.Value
			append ret t
		)
		return ret
	),
	
	fn GetInnerText = 
	(
		return m_node.InnerText
	), 
	
	fn SetInnerText txt = 
	(
		m_node.InnerText = txt
	),
	
	fn GetLocalName =
	(
		return m_node.LocalName
	),
	
	fn SetLocalName txt =
	(
		m_node.LocalName = txt
	),
	
	fn GetName = 
	(
		return m_node.Name
	),
	
	fn SetName txt = 
	(
		m_node.Name = txt
	),
	
	fn GetAttribute attribute = 
	(
		m_node.GetAttribute attribute
	),
	
	fn SetAttribute attribute value = 
	(
		m_node.SetAttribute attribute value
	),
	
	fn RemoveAttribute attribute =
	(
		m_node.RemoveAttribute attribute
	),
	
	fn HasAttribute attribute =
	(
		m_node.HasAttribute attribute
	),
	
	fn AppendNode newNode = 
	(
		if classof newNode == XMLNode then
		(
			m_node.AppendChild newNode.m_node
			return True
		)
		else
		(
			return false
		)
	),
	
	fn GetChild index = 
	(
		local dNode = m_node.ChildNodes.ItemOf index
		
		if dNode.Name != "#text" then
		(
			newNode = XMLNode.Create dNode
			return newNode
		)
		else
		(
			return False
		)
	),
	
	fn GetChild name = 
	(
		for i = 0 to (m_node.ChildNodes.Count - 1) do
		(
			local dNode = m_node.ChildNodes.ItemOf i
			
			if dNode.LocalName == name then
			(
				local newNode = XMLNode.Create dNode
				return newNode
			)
		)
		
		throw ("Child with name " + name + " not found")
	),
	
	fn GetChildren = 
	(
		local nodes = #()
		for i = 0 to (m_node.ChildNodes.Count - 1) do(
			local dNode = m_node.ChildNodes.ItemOf i
			local newNode = XMLNode.Create dNode
			append nodes newNode
		)
		return nodes
	),
	
	fn RemoveChild childNode = 
	(
		if (classof childNode == XMLNode) then 
		(
			m_node.RemoveChild childNode.DotNetNode
			return true
		)
		else
		(
			return false
		)
	),
	
	fn GetParentNode =
	(
		return m_node.ParentNode
	)
)

struct XMLDocument 
( 
	/* Private members */
	m_dom = dotNetObject "System.Xml.XmlDocument",
	m_init = false,
	
	/* Properties */
	RootNode,
	
	/* Static method */
	fn LoadFromXml pathToXml =
	(
		try (m_init) catch ("Can't use this method through an instance reference.")
		
		-- create xml object
		local xml = XMLDocument()
		xml.LoadXml pathToXml
		
		return xml
	),
	
	fn LoadXml pathToXml =
	(
		m_dom = dotNetObject "System.Xml.XmlDocument"
		m_dom.Load pathToXml
		m_init = true
		
		-- set the rootnode
		RootNode = XMLNode.Create m_dom.DocumentElement
	),
	
	fn SaveXml pathToXml = 
	(
		if (m_init) then
		(
			m_dom.Save pathToXml
			return true
		)
		else
		(
			return false
		)
	),
	
	fn CreateElement tag = 
	(
		local dNode = m_dom.CreateElement tag
		return XMLNode.Create dNode
	),
	
	fn AppendChild newNode = 
	(
		if classof newNode == XMLNode then
		(
			m_dom.AppendChild newNode.DotNetNode
			return true
		)
		else
		(
			return false
		)
	),
	
	fn SaveFormattedXml pathToXml = 
	(
		if (not m_init) then
		(
			return false
		)
		
		-- get writer settings
		local writerSettings = dotNetObject "System.Xml.XmlWriterSettings"
		writerSettings.Indent = true
		
		-- get writer class
		local writerClass = dotNetClass "System.Xml.XmlTextWriter"
		
		-- create writer instance, and write content to it
		local writer = writerClass.Create pathToXml writerSettings
		(
			m_dom.WriteContentTo writer
		)
		writer.Close()
		
		return true
	)
)

struct XMLHelper
(
	fn NodeToVector xmlNode =
	(
		local floatStrings = FilterString (xmlNode.GetInnerText()) " "
		
		if (floatStrings.Count == 0) then
		(
			return 0.0f
		)
		else if (floatStrings.Count == 1) then
		(
			return floatStrings[1] as float
		)
		else if (floatStrings.Count == 2) then
		(
			return [floatStrings[1] as float, floatStrings[2] as float]
		)
		else if (floatStrings.Count == 3) then
		(
			return [floatStrings[1] as float, floatStrings[2] as float, floatStrings[3] as float]
		)
		else if (floatStrings.Count == 4) then
		(
			return [floatStrings[1] as float, floatStrings[2] as float, floatStrings[3] as float, floatStrings[4] as float]
		)
	)
)

/************************/
/*** SonicPath structs ***/
/************************/

struct SonicPathKnot
(
	Type 		= "",			-- auto, corner, bezier, bezier_corner
	InVec 		= [0, 0, 0],
	OutVec 		= [0, 0, 0],
	PointVec	= [0, 0, 0],
	
	/* Static */
	fn LoadFromXmlNode splineNode =
	(
		local objInst = SonicPathKnot()
		
		objInst.Type = splineNode.GetAttribute "type"
		objInst.InVec = XMLHelper.NodeToVector (splineNode.GetChild "invec")
		objInst.OutVec = XMLHelper.NodeToVector (splineNode.GetChild "outvec")
		objInst.PointVec = XMLHelper.NodeToVector (splineNode.GetChild "point")
		
		return objInst
	)
)

struct SonicPathSpline
(
	Knots = #(),
	
	/* Static */
	fn LoadFromXmlNode splineNode =
	(
		local objInst = SonicPathSpline()
		
		local knotNodes = splineNode.GetChildren()
		
		for knotNode in knotNodes do
		(
			if (knotNode.GetLocalName() != "knot") then
			(
				throw "Not a valid path file.\nUnexpected xml element in spline3d element."
			)
			
			append objInst.Knots (SonicPathKnot.LoadFromXmlNode knotNode)
		)
		
		return objInst
	)
)

struct SonicPathGeometry
(
	ID			= "",
	Name 	= "",
	Splines 	= #(),
	Width 	= 0,
	
	/* Static */
	fn LoadFromXmlNode geometryNode =
	(
		local objInst = SonicPathGeometry()
	
		objInst.ID = geometryNode.GetAttribute "id"
		objInst.Name = geometryNode.GetAttribute "name"
		
		local splinesNode = geometryNode.GetChild "spline"
		
		objInst.Splines = SonicPathGeometry.LoadSplines splinesNode
		objInst.Width = splinesNode.GetAttribute "width"
		
		return objInst
	),
	
	/* Static */
	fn LoadSplines splinesNode =
	(
		local splineNodes = splinesNode.GetChildren()
		local splineList = #()
		
		for splineNode in splineNodes do
		(
			if (splineNode.GetLocalName() != "spline3d") then
			(
				throw "Not a valid path file.\nUnexpected xml element in splines element."
			)
			
			append splineList (SonicPathSpline.LoadFromXmlNode splineNode)
		)
		
		return splineList
	)
)

struct SonicPathNode
(
	ID 						= "",
	Name 					= "",
	TranslationVec		= [0, 0, 0],
	ScaleVec				= [0, 0, 0],
	RotationVec			= quat 0 0 0 1,
	InstanceURL			= "",					-- url, hashtag prefix pointing to a SonicPathGeometry
	
	/* Static */
	fn LoadFromXmlNode xmlNode =
	(
		local objInst = SonicPathNode()
		
		objInst.ID = xmlNode.GetAttribute "id"
		objInst.Name = xmlNode.GetAttribute "name"
		objInst.TranslationVec = XMLHelper.NodeToVector (xmlNode.GetChild "translate")
		objInst.ScaleVec = XMLHelper.NodeToVector (xmlNode.GetChild "scale")
		
		-- cheap way to get the quat out
		local quatRot = XMLHelper.NodeToVector (xmlNode.GetChild "rotate")
		objInst.RotationVec.X = quatRot.X
		objInst.RotationVec.Y = quatRot.Y
		objInst.RotationVec.Z = quatRot.Z
		objInst.RotationVec.W = quatRot.W
		
		objInst.InstanceURL = (xmlNode.GetChild "instance").GetAttribute "url" 
		
		return objInst
	)
)

struct SonicPath
(
	Geometries 	= #(),	-- list of SonicPathGeometry structs
	Nodes 			= #(),	-- stored as a scene graph
	
	/* Static */
	fn LoadFromXml pathToXml =
	(
		GPI_PrintDebug "Loading xml file.."
		
		local xmlDoc = undefined
		local geometriesNode = undefined
		local sceneNode = undefined
		
		/* Load the xml file */
		try (xmlDoc = XMLDocument.LoadFromXml pathToXml) catch 
		(
			"Not a valid path file.\nFailed to load xml."
		)
		
		/* Verify the contents */
		if (xmlDoc.RootNode.GetLocalName() != "SonicPath") then
		(
			throw "Not a valid path file.\nRoot node tag name is not \"SonicPath\"."
		)
	
		try (geometriesNode = xmlDoc.RootNode.GetChild "library") catch
		(
			"Not a valid path file.\nGeometry library node is not present."
		)
		
		try (sceneNode = xmlDoc.RootNode.GetChild "scene") catch
		(
			"Not a valid path file.\nScene node is not present."
		)
		
		GPI_PrintDebug "Xml content verified successfully."
		
		/* Build the instance */
		local objInst = SonicPath()
		objInst.Geometries = SonicPath.LoadGeometries geometriesNode
		objInst.Nodes = SonicPath.LoadNodes sceneNode
		
		return objInst
	),
	
	/* Static */
	fn LoadGeometries geometriesNode =
	(
		GPI_PrintDebug "Loading spline geometry.."
		
		geometryNodes = geometriesNode.GetChildren()
		geometryList = #()
		
		for geometryNode in geometryNodes do
		(
			if (geometryNode.GetLocalName() != "geometry") then
			(
				throw "Not a valid path file.\nUnexpected xml element in geometry library."
			)
			
			append geometryList (SonicPathGeometry.LoadFromXmlNode geometryNode)
		)
		
		GPI_PrintDebug "Done loading spline geometry."
		
		return geometryList
	),
	
	/* Static */
	fn LoadNodes sceneNode =
	(
		GPI_PrintDebug "Loading spline nodes.."
		
		sceneNodes = sceneNode.GetChildren()
		splineNodes = #()
		
		for sceneNode in sceneNodes do
		(
			if (sceneNode.GetLocalName() != "node") then
			(
				throw "Not a valid path file.\nUnexpected xml element in scene graph."
			)
			
			append splineNodes (SonicPathNode.LoadFromXmlNode sceneNode)
		)
		
		GPI_PrintDebug "Done loading spline nodes."
		
		return splineNodes
	),
	
	/* Static */
	fn LoadIntoMaxScene sonicPath flipUp =
	(
		GPI_PrintDebug "Loading splines into scene.."
		
		for splineNode in sonicPath.Nodes do
		(
			-- Find the geometry instance
			splineGeo = undefined
			for geo in sonicPath.Geometries do
			(
				if ("#" + geo.ID == splineNode.InstanceURL) then
				(
					splineGeo = geo
				)
			)
			
			-- create the spline shape
			local splineMaxShape = SplineShape name:splineNode.Name
			
			for spline in splineGeo.Splines do
			(
				local splineIdx = addNewSpline splineMaxShape
				
				for knot in spline.Knots do
				(					
					pointVec = knot.PointVec
					inVec = knot.InVec
					outVec = knot.OutVec
					
					local knotType = undefined
					local outType = undefined
					
					case knot.Type of 
					(
						"auto":				(	knotType = #smooth; 			outType = #line		)
						"corner":				( 	knotType = #corner; 			outType = #line		)
						"bezier":				( 	knotType = #bezier; 			outType = #curve	)
						"bezier_corner":	( 	knotType = #bezierCorner; 	outType = #curve	)
					)
					
					addKnot splineMaxShape splineIdx knotType outType pointVec inVec outVec
				)
			)
			
			local tfm = (scalematrix splineNode.ScaleVec) * ((inverse splineNode.RotationVec) as matrix3)
			tfm.row4 = splineNode.TranslationVec
			
			if (flipUp) then
			(
				tfm = UpAxisHelper.FlipMatrixUp tfm
			)

			splineMaxShape.transform = tfm 
			
			updateshape splineMaxShape
		)
		
		GPI_PrintDebug "Done loading splines into scene."
	)
)

utility GenerationsSplineImporter "GenerationsSplineImporter" width:162 height:175
(
	label lbl1 "Pick a file to open:" pos:[16,44] width:108 height:15
	editText pathText "" pos:[10,67] width:140 height:20
	checkBox enableFlip "Enable Y-Z flip" pos:[18,12]
	button importButton "Import" pos:[20,131] width:116 height:23 enabled:true
	button browseButton "Browse" pos:[20,99] width:116 height:23 enabled:true
	
	global GPI_FilePath = ""
	global GPI_PathValid = false

	on browseButton pressed do
	(
		GPI_FilePath = getOpenFileName caption:"Pick an XML file to load" types:"XML File|*.xml"
		
		if (GPI_FilePath != undefined) then 
		(
			pathText.Text = GPI_FilePath
			GPI_PathValid = true
		) 
		else
		(
			GPI_PathValid = false
		)
	)
	
	on importButton pressed do
	(
		gc()
		
		if (GPI_Debug) then
		(
			clearlistener()
		)
		
		if (not GPI_PathValid) then 
		(
			messageBox("Please select a file to load")
		)
		else
		(
			local pathFile = undefined
			
			disableSceneRedraw()
			
			try
			(
				pathFile = SonicPath.LoadFromXml GPI_FilePath
				SonicPath.LoadIntoMaxScene pathFile enableFlip.checked
			)
			catch
			(
				messagebox (getCurrentException())
			)
			
			enableSceneRedraw()
		)
		
		gc()
	) 
)

